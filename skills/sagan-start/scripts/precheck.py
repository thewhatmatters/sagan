#!/usr/bin/env python3
"""Dispatch-readiness check over mirrored tickets — the AC gate, as code.

I/O: stdout JSON {tickets, ready, blocked, summary} · stderr human board
     · exit 2 when --require-ac is set and any selected ticket has no AC.

This is the one rule sagan.yaml calls `ac_before_dispatch: required` that a
script can actually enforce: no AC block with real content, no dispatch. Every
other rule in the file is still model-interpreted at v0.
"""
import argparse
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _sagan as S  # noqa: E402

MARK = {True: "✅", False: "⛔"}
ITEM = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")


def content_lines(body):
    return [ln for ln in (body or "").splitlines()
            if ln.strip() and not ln.strip().startswith("<!--")]


def inspect(path, root):
    with io.open(path, encoding="utf-8") as fh:
        text = fh.read()
    fm, _order, body = S.split_frontmatter(text)
    region = S.extract_region(body, S.REPO_START, S.REPO_END)
    blocks = S.blocks_from_region(region if region is not None else body)

    ac_lines = content_lines(blocks.get("ac", ""))
    ac_items = len([ln for ln in ac_lines if ITEM.match(ln)])
    reasons = []
    # Only a MIRRORED file is expected to carry the markers. A legacy local
    # ticket (T-000/T-001, written before the mirror existed) is a perfectly
    # valid ticket read whole — do not tell anyone to "re-run the mirror" on
    # a file the mirror deliberately never touches.
    mirrored = bool(fm.get("mirror_version"))
    if mirrored and region is None:
        reasons.append("mirror file lost its sagan:repo-owned markers — re-mirror")
    if not ac_lines:
        reasons.append("no acceptance criteria")
    elif ac_items == 0:
        reasons.append("AC block has prose but no enumerated items")
    blocked_by = (fm.get("blocked_by") or "").strip()
    if blocked_by:
        reasons.append("blocked by %s" % blocked_by)

    title = fm.get("title", "")
    if not title:  # legacy local ticket — its title is the H1
        m = re.search(r"^#\s+(.+?)\s*$", body, re.M)
        title = m.group(1) if m else ""

    return {
        "id": fm.get("id") or os.path.basename(path)[:-3],
        "title": title,
        "status": fm.get("status", ""),
        "mirrored": mirrored,
        "path": os.path.relpath(path, root),
        "ac_present": bool(ac_lines),
        "ac_items": ac_items,
        "blocked_by": blocked_by or None,
        "builder_id": fm.get("builder_id") or None,
        "verifier_id": fm.get("verifier_id") or None,
        "evidence_sha": fm.get("evidence_sha") or None,
        "fetched_at": fm.get("fetched_at") or None,
        "blocks_present": sorted(blocks.keys()),
        "dispatch_ready": not reasons,
        "reasons": reasons,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=None)
    ap.add_argument("--ticket", default=None,
                    help="comma-separated ids; default = every mirrored ticket")
    ap.add_argument("--require-ac", action="store_true",
                    help="exit 2 if any selected ticket is not dispatch-ready")
    ap.add_argument("--agent", action="store_true")
    a = ap.parse_args()

    root = S.project_root(a.project)
    cfg = S.read_sagan_yaml(S.sagan_yaml(root))
    tdir = S.tickets_dir(root, cfg)
    if not os.path.isdir(tdir):
        print("no tickets dir at %s" % tdir, file=sys.stderr)
        return S.emit({"tickets": [], "ready": [], "blocked": [],
                       "summary": "no tickets directory"}, 0)

    wanted = None
    if a.ticket:
        wanted = {t.strip().upper() for t in a.ticket.split(",") if t.strip()}

    tickets = []
    for fn in sorted(os.listdir(tdir)):
        if not fn.endswith(".md"):
            continue
        info = inspect(os.path.join(tdir, fn), root)
        if wanted and info["id"].upper() not in wanted:
            continue
        tickets.append(info)

    missing = sorted(wanted - {t["id"].upper() for t in tickets}) if wanted else []
    ready = [t["id"] for t in tickets if t["dispatch_ready"]]
    blocked = [t["id"] for t in tickets if not t["dispatch_ready"]]

    print("sagan-start precheck — %d ticket(s)" % len(tickets), file=sys.stderr)
    for t in tickets:
        print("  %s %-10s %s%s" % (
            MARK[t["dispatch_ready"]], t["id"],
            (t["title"][:52] or "(untitled)"),
            ("  — " + "; ".join(t["reasons"])) if t["reasons"] else ""),
            file=sys.stderr)
    for m in missing:
        print("  ⛔ %-10s not mirrored" % m, file=sys.stderr)

    payload = {
        "project": root,
        "tickets": tickets,
        "ready": ready,
        "blocked": blocked,
        "missing": missing,
        "summary": "%d ready, %d blocked, %d not mirrored" % (
            len(ready), len(blocked), len(missing)),
    }
    gate_failed = a.require_ac and (blocked or missing)
    return S.emit(payload, 2 if gate_failed else 0)


if __name__ == "__main__":
    sys.exit(main())

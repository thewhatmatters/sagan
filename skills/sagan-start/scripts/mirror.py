#!/usr/bin/env python3
"""Mirror Linear issues into local ticket markdown — one writer per field.

I/O: Linear issue JSON on **stdin** · stdout JSON {written, refused, summary}
     · stderr human lines · exit 1 on refusal, 2 on unusable input.

The session fetches from Linear (MCP); this script does the deterministic part
so the split is enforced by code rather than remembered by a model:

  Linear-owned  frontmatter (title/status/priority/assignee/url/labels) and the
                `sagan:linear-owned` region  -> REGENERATED on every fetch.
  Repo-owned    frontmatter in _sagan.REPO_OWNED_FM and everything inside the
                `sagan:repo-owned` region    -> CARRIED OVER byte-for-byte.

Fail-closed: if an existing mirror file has repo-owned content this script
cannot locate unambiguously, it REFUSES to write that ticket rather than risk
clobbering an agent's AC or build notes.
"""
import argparse
import datetime
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _sagan as S  # noqa: E402

AC_HEADING = re.compile(r"^##\s+(ac|acceptance criteria)\s*$", re.I | re.M)

# Linear's list_issues returns a SHORTENED description with this marker. A
# mirror built from it would silently drop half the acceptance criteria — the
# workers would then build against a truncated contract. Refuse, and make the
# session re-fetch that issue with get_issue.
TRUNCATED = re.compile(r"\(truncated,\s*use\s*`?get_issue`?", re.I)


def _name(val):
    """Linear fields arrive as a string or an object depending on the call."""
    if val is None:
        return ""
    if isinstance(val, str):
        return val
    if isinstance(val, dict):
        for k in ("name", "displayName", "title", "identifier", "email"):
            if val.get(k):
                return str(val[k])
    return str(val)


def normalize(raw):
    ident = raw.get("identifier") or raw.get("id") or ""
    labels = raw.get("labels") or []
    if isinstance(labels, dict):
        labels = labels.get("nodes") or []
    return {
        "id": str(ident).strip(),
        "title": _name(raw.get("title")).strip(),
        "description": raw.get("description") or "",
        "status": _name(raw.get("state") or raw.get("status")).strip(),
        "priority": _name(raw.get("priorityLabel") or raw.get("priority")).strip(),
        "assignee": _name(raw.get("assignee")).strip(),
        "url": _name(raw.get("url")).strip(),
        "labels": ", ".join(sorted(filter(None, (_name(x) for x in labels)))),
        "parent": _name(raw.get("parentId") or raw.get("parent")).strip(),
        "linear_updated_at": _name(raw.get("updatedAt")).strip(),
    }


def load_issues(stream):
    data = json.load(stream)
    if isinstance(data, dict):
        for key in ("issues", "nodes", "results", "data"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
        else:
            data = [data]
    if not isinstance(data, list):
        raise ValueError("expected a list of issues or {issues:[...]}")
    return [normalize(x) for x in data if isinstance(x, dict)]


def lift_ac(description):
    """On CREATE only: if the Linear description already carries an AC section,
    move it into the repo-owned AC block instead of making someone retype it."""
    m = AC_HEADING.search(description or "")
    if not m:
        return None
    tail = description[m.end():]
    nxt = re.search(r"^##\s+", tail, re.M)
    body = (tail[:nxt.start()] if nxt else tail).strip("\n")
    return body or None


def build(issue, existing_text, blocks):
    """Return (text, action, notes) or raise RefuseWrite."""
    notes = {}
    if TRUNCATED.search(issue["description"] or ""):
        raise RefuseWrite(
            "description is truncated by list_issues — re-fetch this issue with "
            "get_issue and pipe the full record in")
    fm_existing, _order, body_existing = S.split_frontmatter(existing_text or "")

    repo_region = None
    if existing_text:
        repo_region = S.extract_region(body_existing, S.REPO_START, S.REPO_END)
        if repo_region is None:
            # Pre-marker file (hand-written or an older mirror). Migrate from the
            # first `## AC` heading onward; refuse if there is no anchor at all.
            m = AC_HEADING.search(body_existing)
            if m:
                repo_region = "\n" + body_existing[m.start():].rstrip("\n") + "\n"
                notes["migrated"] = True
            elif body_existing.strip():
                raise RefuseWrite(
                    "existing file has content but no sagan:repo-owned markers "
                    "and no '## AC' anchor — refusing to overwrite")

    seeded = {}
    if repo_region is None:
        lifted = lift_ac(issue["description"])
        if lifted:
            # The description above keeps its own copy (it is a verbatim mirror).
            # Say in the artifact which one wins, so an amendment cannot leave
            # two disagreeing AC blocks with no stated precedence.
            seeded["ac"] = (
                "<!-- seeded once from the Linear description on %s. THIS block "
                "is authoritative — amend here, never in the mirrored copy above. -->\n\n%s"
                % (datetime.date.today().isoformat(), lifted))
            notes["ac_seeded_from"] = "linear-description"
        repo_region = S.seed_repo_region(blocks, seeded)

    linear_fm = [
        ("id", issue["id"]),
        ("title", issue["title"]),
        ("status", issue["status"]),
        ("priority", issue["priority"]),
        ("assignee", issue["assignee"]),
        ("labels", issue["labels"]),
        ("parent", issue["parent"]),
        ("url", issue["url"]),
        ("linear_updated_at", issue["linear_updated_at"]),
        ("fetched_at", datetime.datetime.now(datetime.timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ")),
        ("mirror_version", S.MIRROR_VERSION),
    ]
    repo_fm = [(k, fm_existing.get(k, "")) for k in S.REPO_OWNED_FM
               if k in fm_existing or k in S.REPO_FM_ALWAYS]
    if notes.get("ac_seeded_from"):
        repo_fm.append(("ac_seeded_from", notes["ac_seeded_from"]))
    if notes.get("migrated"):
        repo_fm.append(("migrated_at", datetime.date.today().isoformat()))

    text = (
        S.render_frontmatter(linear_fm + repo_fm)
        + "\n" + S.LINEAR_START + "\n\n"
        + (issue["description"].strip("\n") or "_(no description in Linear)_")
        + "\n\n" + S.LINEAR_END + "\n\n"
        + S.REPO_START + "\n" + repo_region.strip("\n") + "\n" + S.REPO_END + "\n"
    )

    if not existing_text:
        action = "created"
    elif _ignoring_fetched_at(existing_text) == _ignoring_fetched_at(text):
        action = "unchanged"
    else:
        action = "updated"
    return text, action, notes


def _ignoring_fetched_at(text):
    return re.sub(r"^fetched_at:.*$", "", text or "", flags=re.M)


class RefuseWrite(Exception):
    pass


def ac_present(text):
    region = S.extract_region(text, S.REPO_START, S.REPO_END) or ""
    body = S.blocks_from_region(region).get("ac", "")
    return bool([ln for ln in body.splitlines()
                 if ln.strip() and not ln.strip().startswith("<!--")])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--agent", action="store_true")
    a = ap.parse_args()

    root = S.project_root(a.project)
    cfg = S.read_sagan_yaml(S.sagan_yaml(root))
    blocks_raw = (cfg.get("ticket.blocks") or "").strip("[] ")
    blocks = tuple(x.strip() for x in blocks_raw.split(",") if x.strip()) \
        or S.DEFAULT_BLOCKS
    tdir = S.tickets_dir(root, cfg)

    try:
        issues = load_issues(sys.stdin)
    except Exception as exc:
        print("unusable stdin: %s" % exc, file=sys.stderr)
        return S.emit({"error": "bad-input", "detail": str(exc)}, 2)

    written, refused = [], []
    for issue in issues:
        if not issue["id"]:
            refused.append({"id": None, "reason": "issue has no identifier"})
            continue
        path = os.path.join(tdir, "%s.md" % issue["id"])
        existing = None
        if os.path.isfile(path):
            with io.open(path, encoding="utf-8") as fh:
                existing = fh.read()
        try:
            text, action, notes = build(issue, existing, blocks)
        except RefuseWrite as exc:
            refused.append({"id": issue["id"],
                            "path": os.path.relpath(path, root),
                            "reason": str(exc)})
            print("REFUSED %s — %s" % (issue["id"], exc), file=sys.stderr)
            continue
        if a.dry_run:
            action = "would-" + action
        elif action != "unchanged":
            S.atomic_write(path, text)
        written.append({
            "id": issue["id"],
            "path": os.path.relpath(path, root),
            "action": action,
            "ac_present": ac_present(text),
            "notes": notes,
        })
        print("%-9s %s" % (action, os.path.relpath(path, root)), file=sys.stderr)

    payload = {
        "project": root,
        "tickets_dir": os.path.relpath(tdir, root),
        "written": written,
        "refused": refused,
        "summary": "%d mirrored, %d refused, %d without AC" % (
            len(written), len(refused),
            len([w for w in written if not w["ac_present"]])),
    }
    return S.emit(payload, 1 if refused else 0)


if __name__ == "__main__":
    sys.exit(main())

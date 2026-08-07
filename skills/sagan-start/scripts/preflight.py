#!/usr/bin/env python3
"""Readiness check for sagan-start (spec A6).

I/O: stdout JSON {overall, checks, summary} · stderr human board · exit 1 only on `down`.
States per check: ready | degraded | gated | down  (with a gate id).
Keyless, no network. The Linear reachability check is deliberately reported as
`gated`, not guessed: only the session's MCP call can prove the store is live.
"""
import argparse
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _sagan as S  # noqa: E402

MARK = {"ready": "✅", "degraded": "⚠ ", "gated": "🔒", "down": "⛔"}
RANK = {"ready": 0, "degraded": 1, "gated": 2, "down": 3}


def check_overlay(root):
    if not os.path.isdir(S.sagan_dir(root)):
        return ("down", "SAGAN_MISSING",
                "no .sagan/ in %s — run /wire-sagan first" % root)
    if not os.path.isfile(S.sagan_yaml(root)):
        return ("down", "SAGAN_MISSING",
                ".sagan/ exists but sagan.yaml is missing — run /wire-sagan --update")
    return ("ready", None, "overlay present")


def check_git(root):
    ok, _ = S.git(root, "rev-parse", "--git-dir")
    if not ok:
        return ("degraded", None,
                "not a git repo (or git absent) — evidence cannot be SHA-bound")
    sha = S.head_sha(root)
    return ("ready", None, "git repo at %s" % (sha[:7] if sha else "unknown"))


def check_tickets(root, cfg):
    d = S.tickets_dir(root, cfg)
    rel = os.path.relpath(d, root)
    if not os.path.isdir(d):
        return ("degraded", None,
                "%s/ absent — the first mirror will create it" % rel)
    if not os.access(d, os.W_OK):
        return ("down", "TICKETS_UNWRITABLE", "%s/ is not writable" % rel)
    n = len([f for f in os.listdir(d) if f.endswith(".md")])
    return ("ready", None, "%s/ writable (%d existing .md)" % (rel, n))


def check_ledger(root):
    p = S.ledger_path(root)
    d = os.path.dirname(p)
    if not os.path.isdir(d):
        return ("degraded", None, "ledger dir absent — will be created on append")
    if os.path.exists(p) and not os.access(p, os.W_OK):
        return ("down", "LEDGER_UNWRITABLE", "events.jsonl is not writable")
    if not os.access(d, os.W_OK):
        return ("down", "LEDGER_UNWRITABLE", "ledger dir is not writable")
    n = 0
    if os.path.isfile(p):
        with io.open(p, encoding="utf-8") as fh:
            n = sum(1 for line in fh if line.strip())
    return ("ready", None, "events.jsonl appendable (%d events)" % n)


def check_store(cfg):
    store = (cfg.get("ticket.store") or "local-files").split("#")[0].strip()
    if store == "linear":
        return ("gated", "LINEAR_FETCH_UNVERIFIED",
                "store=linear — reachability provable only by the session's "
                "Linear MCP call in Step 2, not from this script")
    return ("ready", None, "store=%s — no external fetch needed" % store)


def check_mirror_hygiene(root, cfg):
    """A live mirror carries private tracker ids into the repo. If mirroring is
    on and the ignore rule is absent, say so — do not silently commit them."""
    store = (cfg.get("ticket.store") or "local-files").split("#")[0].strip()
    if store != "linear":
        return ("ready", None, "no live mirror — nothing to ignore")
    policy = (cfg.get("ticket.mirror.commit") or "ignore").split("#")[0].strip()
    if policy == "commit":
        return ("ready", None,
                "mirror.commit=commit — live tickets are committed by choice")
    gi = os.path.join(root, ".gitignore")
    rel = os.path.relpath(S.tickets_dir(root, cfg), root)
    want = "%s/*-[0-9]*.md" % rel
    text = ""
    if os.path.isfile(gi):
        with io.open(gi, encoding="utf-8") as fh:
            text = fh.read()
    if rel in text and ".md" in text:
        return ("ready", None, "mirror files are gitignored")
    return ("degraded", "MIRROR_NOT_IGNORED",
            "mirror.commit=ignore but .gitignore has no rule — add: %s" % want)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=None)
    ap.add_argument("--agent", action="store_true")
    a = ap.parse_args()

    root = S.project_root(a.project)
    cfg = S.read_sagan_yaml(S.sagan_yaml(root))

    checks = {
        "overlay": check_overlay(root),
        "git": check_git(root),
        "tickets": check_tickets(root, cfg),
        "ledger": check_ledger(root),
        "store": check_store(cfg),
        "mirror_hygiene": check_mirror_hygiene(root, cfg),
    }
    overall = "ready"
    for state, _g, _d in checks.values():
        if RANK[state] > RANK[overall]:
            overall = state

    print("sagan-start readiness — %s" % root, file=sys.stderr)
    for name, (state, gate, detail) in checks.items():
        print("  %s %-15s %s%s" % (MARK[state], name, detail,
                                   (" [%s]" % gate) if gate else ""),
              file=sys.stderr)

    payload = {
        "overall": overall,
        "project": root,
        "store": (cfg.get("ticket.store") or "local-files").split("#")[0].strip(),
        "tickets_dir": os.path.relpath(S.tickets_dir(root, cfg), root),
        "checks": {k: {"status": s, "gate": g, "detail": d}
                   for k, (s, g, d) in checks.items()},
        "summary": "%d checks, overall %s" % (len(checks), overall),
    }
    return S.emit(payload, 1 if overall == "down" else 0)


if __name__ == "__main__":
    sys.exit(main())

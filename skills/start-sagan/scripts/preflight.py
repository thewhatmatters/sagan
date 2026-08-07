#!/usr/bin/env python3
"""Readiness check for start-sagan (spec A6).

Checks the target project is a wired Sagan project: .sagan/ overlay present,
sagan.yaml readable, role specs installed, ledger appendable, git repo.
This skill never installs — SAGAN_MISSING/NO_ROLES point to wire-sagan.

I/O: stdout JSON {overall, checks, summary} · stderr human board · exit 1 only on `down`.
States per check: ready | degraded | gated | down  (with a gate id).
"""
import argparse, json, os, subprocess, sys

MARK = {"ready": "✅", "degraded": "⚠ ", "gated": "🔒", "down": "⛔"}
RANK = {"ready": 0, "degraded": 1, "gated": 2, "down": 3}


def check_overlay(root):
    d = os.path.join(root, ".sagan")
    if not os.path.isdir(d):
        return ("down", "SAGAN_MISSING",
                "no .sagan/ overlay — run wire-sagan first ('wire this project to sagan')")
    return ("ready", None, f".sagan/ present at {d}")


def check_config(root):
    p = os.path.join(root, ".sagan", "sagan.yaml")
    if not os.path.isfile(p):
        return ("down", "SAGAN_MISSING", "sagan.yaml missing from .sagan/")
    try:
        with open(p, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        return ("down", "CONFIG_UNREADABLE", f"sagan.yaml unreadable: {e}")
    if "rules:" not in text:
        return ("degraded", None, "sagan.yaml readable but has no rules: block")
    return ("ready", None, "sagan.yaml readable")


def check_roles(root):
    d = os.path.join(root, ".sagan", "roles")
    try:
        roles = sorted(f[:-3] for f in os.listdir(d) if f.endswith(".md"))
    except OSError:
        roles = []
    if not roles:
        return ("down", "NO_ROLES", "no role specs in .sagan/roles/ — re-run wire-sagan")
    return ("ready", None, "roles: " + ", ".join(roles))


def check_ledger(root):
    d = os.path.join(root, ".sagan", "ledger")
    p = os.path.join(d, "events.jsonl")
    if not os.path.isdir(d):
        return ("down", "LEDGER_UNWRITABLE", "no .sagan/ledger/ directory")
    probe = p if os.path.exists(p) else d
    if not os.access(probe, os.W_OK):
        return ("down", "LEDGER_UNWRITABLE", f"cannot write {probe}")
    return ("ready", None, f"ledger appendable ({p})")


def check_memory(root):
    missing = [n for n in ("MEMORY.md", "memory") if not os.path.exists(os.path.join(root, ".sagan", n))]
    if missing:
        return ("degraded", None, "missing (created on first synthesis): " + ", ".join(missing))
    return ("ready", None, "memory tiers present")


def check_git(root):
    try:
        r = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as e:
        return ("down", "NO_GIT", f"git unavailable: {e}")
    if r.returncode != 0:
        return ("down", "NO_GIT", "not a git repository — evidence cannot bind to a SHA")
    return ("ready", None, f"HEAD {r.stdout.strip()[:12]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    args = ap.parse_args()
    root = os.path.abspath(args.project)

    checks = {
        "overlay": check_overlay(root),
        "config": check_config(root),
        "roles": check_roles(root),
        "ledger": check_ledger(root),
        "memory": check_memory(root),
        "git": check_git(root),
    }
    overall = "ready"
    for s, _g, _d in checks.values():
        if RANK[s] > RANK[overall]:
            overall = s

    print("start-sagan readiness", file=sys.stderr)
    for n, (s, g, d) in checks.items():
        suffix = f"  [{g}]" if g else ""
        print(f"  {MARK[s]} {n:<8} {d}{suffix}", file=sys.stderr)
    print(f"  → overall: {overall}", file=sys.stderr)

    payload = {
        "overall": overall,
        "project": root,
        "checks": {n: {"status": s, "gate": g, "detail": d}
                   for n, (s, g, d) in checks.items()},
        "summary": ", ".join(f"{n}={s}" for n, (s, _g, _d) in checks.items()),
    }
    print(json.dumps(payload, indent=2))
    sys.exit(1 if overall == "down" else 0)


if __name__ == "__main__":
    main()

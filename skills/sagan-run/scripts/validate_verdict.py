#!/usr/bin/env python3
"""Validate a critic verdict envelope against the Sagan v0 contract (spec A4).

Critic contract drift is chronic (observed 3× in real runs); this is the
PM-side stand-in for runtime schema enforcement. Strict: unknown fields are
violations, conditional fields must match the verdict.

I/O: JSON envelope on stdin (or --file PATH) · stdout JSON
{valid, verdict, violations[]} · exit 0 always unless input is unreadable/
unparseable (exit 1) — a *failed validation* is a result, not an error.
"""
import argparse, json, sys

VERDICTS = {"APPROVED", "REVISE", "NEEDS_EVIDENCE", "ESCALATE"}
TOP_KEYS = {"verdict", "findings", "evidence_needed", "escalate_reason"}
FINDING_KEYS = {"severity", "ac_ref", "issue", "where"}
SEVERITIES = {"high", "med", "low"}


def validate(env):
    v = []
    if not isinstance(env, dict):
        return ["envelope is not a JSON object"]

    unknown = sorted(set(env) - TOP_KEYS)
    if unknown:
        v.append(f"unknown top-level field(s): {', '.join(unknown)} — contract drift")

    verdict = env.get("verdict")
    if verdict not in VERDICTS:
        v.append(f"verdict must be one of {sorted(VERDICTS)}, got {verdict!r}")

    findings = env.get("findings", [])
    if not isinstance(findings, list):
        v.append("findings must be a list")
        findings = []
    for i, f in enumerate(findings):
        if not isinstance(f, dict):
            v.append(f"findings[{i}] is not an object")
            continue
        missing = sorted(FINDING_KEYS - set(f))
        extra = sorted(set(f) - FINDING_KEYS)
        if missing:
            v.append(f"findings[{i}] missing: {', '.join(missing)}")
        if extra:
            v.append(f"findings[{i}] unknown field(s): {', '.join(extra)}")
        if f.get("severity") not in SEVERITIES:
            v.append(f"findings[{i}].severity must be one of {sorted(SEVERITIES)}")

    if verdict == "NEEDS_EVIDENCE" and not env.get("evidence_needed"):
        v.append("NEEDS_EVIDENCE requires a non-empty evidence_needed")
    if verdict != "NEEDS_EVIDENCE" and "evidence_needed" in env:
        v.append("evidence_needed present but verdict is not NEEDS_EVIDENCE")
    if verdict == "ESCALATE" and not env.get("escalate_reason"):
        v.append("ESCALATE requires a non-empty escalate_reason")
    if verdict != "ESCALATE" and "escalate_reason" in env:
        v.append("escalate_reason present but verdict is not ESCALATE")
    if verdict == "APPROVED" and any(
            isinstance(f, dict) and f.get("severity") == "high" for f in findings):
        v.append("APPROVED with a high-severity finding is contradictory")
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="read envelope from PATH instead of stdin")
    args = ap.parse_args()
    try:
        raw = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
        env = json.loads(raw)
    except (OSError, json.JSONDecodeError) as e:
        print(f"cannot read/parse envelope: {e}", file=sys.stderr)
        print(json.dumps({"valid": False, "verdict": None,
                          "violations": [f"unparseable input: {e}"]}))
        sys.exit(1)

    violations = validate(env)
    verdict = env.get("verdict") if isinstance(env, dict) else None
    print(json.dumps({"valid": not violations, "verdict": verdict,
                      "violations": violations}, indent=2))


if __name__ == "__main__":
    main()

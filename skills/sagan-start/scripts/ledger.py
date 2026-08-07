#!/usr/bin/env python3
"""Append one event to .sagan/ledger/events.jsonl.

I/O: stdout JSON {event, run_id, line, path} · stderr one human line
     · exit 2 on unusable payload.

Field order matches the existing ledger (`event`, `ticket`/`tickets`, payload…,
`ts` last) and `ts` stays date-only, so this writes the same shape the ledger
already carries rather than a second dialect. Append-only: this script never
rewrites or deletes a line.
"""
import argparse
import datetime
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _sagan as S  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=None)
    ap.add_argument("--event", required=True,
                    help="e.g. run.started, ticket.mirrored, decision.needed")
    ap.add_argument("--ticket", default=None)
    ap.add_argument("--tickets", default=None, help="comma-separated, for sprint scope")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--json", dest="payload", default=None,
                    help="extra fields as a JSON object")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--agent", action="store_true")
    a = ap.parse_args()

    root = S.project_root(a.project)
    extra = {}
    if a.payload:
        try:
            extra = json.loads(a.payload)
            if not isinstance(extra, dict):
                raise ValueError("--json must be an object")
        except Exception as exc:
            print("bad --json: %s" % exc, file=sys.stderr)
            return S.emit({"error": "bad-json", "detail": str(exc)}, 2)

    run_id = a.run_id
    if not run_id and a.event == "run.started":
        run_id = "run-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    event = {"event": a.event}
    if a.ticket:
        event["ticket"] = a.ticket
    if a.tickets:
        event["tickets"] = [t.strip() for t in a.tickets.split(",") if t.strip()]
    if run_id:
        event["run_id"] = run_id
    for k, v in extra.items():
        if k not in ("event", "ts"):
            event[k] = v
    event["ts"] = datetime.date.today().isoformat()

    line = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
    path = S.ledger_path(root)
    if not a.dry_run:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with io.open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    print("%s %s" % ("would append" if a.dry_run else "appended", a.event),
          file=sys.stderr)

    return S.emit({"event": a.event, "run_id": run_id, "line": line,
                   "path": os.path.relpath(path, root),
                   "written": not a.dry_run}, 0)


if __name__ == "__main__":
    sys.exit(main())

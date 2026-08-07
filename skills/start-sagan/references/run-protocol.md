# Run protocol — station contracts and ledger shapes

Loaded by SKILL.md Step 5 before the first dispatch (spec A1). The role
specs in the wired project's `.sagan/roles/` are the per-role source of
truth; this file is the PM's dispatch choreography around them.

## Pointer packs

A dispatch prompt contains only:

- the project root path and ticket id,
- the ticket file path (or, for Linear, a local mirror the PM materializes
  — subagents have no MCP access; the mirror is verbatim, never paraphrase),
- the role spec path the worker must follow,
- artifact paths (critic/verify only).

**Access check before every dispatch:** every pointer must resolve for the
worker receiving it. Auth-gated or JS-walled sources get materialized to a
local (gitignored when third-party) path first; the PM's own reading of a
source supplements the original, never substitutes for it.

## Station contracts

| Station | Isolation | Returns | PM validates |
|---------|-----------|---------|--------------|
| build | subagent; may read repo; never edits AC/QA blocks | build note in ticket `## Frontend` block + retro file | note present; scope confined to AC |
| critique | FRESH subagent; artifact paths + AC block + builder rubric ONLY | one JSON verdict envelope | `validate_verdict.py`; on drift, re-request emission — never hand-fix |
| verify | subagent; never the builder | `evidence.recorded` ledger line + ticket `## QA` summary + retro | SHA matches HEAD; every AC item has PASS/FAIL/NOT-EXECUTABLE; `not_verified` honest |

Verdict envelope (critic):

```json
{
  "verdict": "APPROVED | REVISE | NEEDS_EVIDENCE | ESCALATE",
  "findings": [
    { "severity": "high|med|low", "ac_ref": "<AC item>", "issue": "...", "where": "file:line" }
  ],
  "evidence_needed": "only when NEEDS_EVIDENCE",
  "escalate_reason": "only when ESCALATE"
}
```

APPROVED means verified, not plausible: if judging requires execution the
critic hasn't seen, the honest verdict is NEEDS_EVIDENCE.

## Ledger events (append-only, one JSON line each, as they happen)

```json
{ "event": "run.start",        "ticket": "...", "pm": "claude-code-session", "ts": "YYYY-MM-DD" }
{ "event": "dispatch",         "ticket": "...", "role": "frontend|critic|verify", "worker_id": "...", "round": 1, "pack": ["path", "..."], "ts": "..." }
{ "event": "verdict.returned", "ticket": "...", "round": 1, "verdict": "...", "findings": 2, "ts": "..." }
{ "event": "evidence.recorded","ticket": "...", "sha": "...", "verifier": "...", "checks": [ ... ], "overall": "PASS|FAIL", "not_verified": [], "ts": "..." }
{ "event": "decision.made",    "ticket": "...", "gate": "promote", "decision": "...", "by": "<human>", "ts": "..." }
{ "event": "run.completed",    "ticket": "...", "rounds": 2, "ts": "..." }
```

Evidence media (screenshots, captures) lives under `.sagan/ledger/<ticket>/`
next to its events — committed policy is the project's `.gitignore` call
(wire-sagan default: JSONL committed, media ignored).

## Rounds and breakers

- Read `critique.circuit_breakers` from sagan.yaml: `max_rounds` per lane
  (correctness vs quality) and `same_finding_failures`.
- REVISE → new build round with the findings appended to the pointer pack
  (findings are artifacts, not conversation — isolation holds).
- At a cap, or when the same finding fails `same_finding_failures` times
  (strategy may be wrong): verdict becomes ESCALATE → needs-you question.
  Work never quietly ships.
- Healthy iteration looks like new findings each round; watch for repeats.

## Round-1 predictable evidence

Dispatch verify's standing items with the FIRST build round when the AC
makes them inevitable (render screenshots at required widths, overlay-on
captures, JS-disabled check). A critique that would return NEEDS_EVIDENCE
for predictable evidence is a wasted round.

## PM-direct execution

Legal only when the work requires credentials or infrastructure beyond
worker containment (e.g. an authed deploy). Log the dispatch with
`"worker_id": "pm-direct"` and a `rationale` field. Verify remains a
separate worker — PM-direct never extends to self-verification.

## Ticket-store notes

- **Linear:** save_issue silently ignores a nonexistent project name — no
  error, no auto-create. Verify every mutating response echoes the project
  before claiming success. Mirror the ticket body to a local file for
  worker dispatches; sync block edits (Frontend/QA/Decisions) back after
  each station.
- **Local:** `tickets/<id>.md` is canonical; blocks are edited in place.
- Either way the ticket carries the four blocks: `## AC`, `## Frontend`
  (build notes), `## QA` (evidence summary), `## Decisions` (dated entries:
  builder_id, verifier_id, evidence_sha, amendments, promote decision).

## AC amendments

An amendment mid-run = (1) dated entry in `## Decisions` stating what
changed and why, (2) the `## AC` block edited and marked
"Amended — see Decisions". Never a silent AC edit; never a Decisions-only
note that leaves the AC stale.

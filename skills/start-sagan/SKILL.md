---
name: start-sagan
description: >-
  Start and drive one Sagan run in a project already wired with the .sagan/
  overlay — the PM-side run loop. Reads sagan.yaml, resolves the ticket
  (Linear store or local tickets/), requires an AC block before any dispatch,
  surfaces open decisions as structured questions with recommended defaults,
  logs run.start to the ledger, then drives the circuit: builder → fresh
  artifact-only critic (APPROVED/REVISE/NEEDS_EVIDENCE/ESCALATE) → verifier
  (never the builder, evidence bound to a git SHA) → human promote gate →
  retro synthesis. Also configures the agents a run needs: consent-gated,
  idempotent generation of .claude/agents/sagan-<role>.md from
  .sagan/roles/*.md. Use when the user says "start sagan", "run sagan",
  "do a sagan run", "sagan test run", "run this ticket through sagan",
  "run T-123 / WHA-123 through the loop", or "/start-sagan [ticket]".
  NOT installation — if .sagan/ is missing, stop and point to wire-sagan.
---

# start-sagan

Start and drive one Sagan run: startup checks, agent configuration, and the
build → critique → verify → promote **circuit**, PM-interpreted (v0).

## Leading words

- **circuit** — one ticket's full path: dispatch → build → critique →
  (evidence) → verdict → promote gate. Stations never merge: the builder
  never self-approves, the critic never fixes, verify is never the builder.
- **pointer pack** — a dispatch context of paths + ticket id only, never
  paraphrased content. Every pointer must resolve *for the worker receiving
  it*; materialize anything it can't reach before dispatch.
- **needs-you** — the structured question round: every open decision goes to
  the human as a question set with a recommended default per question
  (AskUserQuestion in the Claude Code binding), never buried in prose.

## How to run

"start sagan", "run this ticket through sagan", or `/start-sagan [ticket-id]`.

## Flags

| Flag | Meaning |
|------|---------|
| `--agent` | non-interactive; no prompts/pauses (spec A7b/A9). Gates cannot be crossed: the run stops at the first needs-you or promote gate and reports what it needs |
| `--ticket=ID` | ticket to run (else: surfaced as a needs-you question over open tickets) |
| `--project=PATH` | wired project root (default: cwd) |
| `--skip-agents` | skip the agent-configuration offer (Step 2) |
| `--dry-run` | run Steps 0–4, print the run plan (stations, pointers, gates); dispatch nothing, write nothing |

## Step 0 — Mode probe

`python3 --version` + `scripts/` present → **SCRIPTS**. Otherwise **NATIVE**:
same checks with built-in file tools (read sagan.yaml directly; validate the
critic envelope by inspection). Announce the mode in one line.

Two session-dependency probes, both modes (model-side):

- **Agent tool absent** (no subagent dispatch available) → STOP honestly.
  Inline PM execution would merge stations and break the isolation
  contract; there is no degraded circuit.
- **`ticket.store: linear` but no Linear MCP connector in this session** →
  needs-you gate: run from a local `tickets/<id>.md` mirror instead, or
  stop until the connector is authorized. Never guess ticket content.

## Step 1 — Preflight

SCRIPTS: `python3 scripts/preflight.py --project=<root>`. Gates:

- `SAGAN_MISSING` (down) — no `.sagan/` overlay. STOP and point to
  wire-sagan ("wire this project to sagan"); this skill never installs.
- `NO_ROLES` (down) — `.sagan/roles/` empty or absent; re-run wire-sagan.
- `LEDGER_UNWRITABLE` (down) — nothing can be recorded; nothing may run.
- `CONFIG_UNREADABLE` (down) — sagan.yaml exists but cannot be read; fix
  permissions/encoding before anything runs.
- `NO_GIT` (down) — not a git repository (or git unavailable); evidence
  cannot bind to a SHA, so the ship requirement is unsatisfiable.
- Missing `MEMORY.md` / `memory/` → degraded (created on first synthesis).

## Step 2 — Configure agents (consent-gated, idempotent)

Probe `.sagan/roles/*.md` against `.claude/agents/sagan-<role>.md` in the
project. For each role lacking an agent definition, offer to generate one
from the role spec per `references/agent-definitions.md` (marker-comment
block, regenerate-safe, role spec stays the source of truth). Consent is
one needs-you question listing exactly what would be written. Declining —
or `--skip-agents` — is fine: dispatch falls back to generic subagents
handed the role-spec path in the pointer pack. `--agent`: never writes;
prints what it would generate.

## Step 3 — Resolve ticket + AC gate

Read `ticket.store` from sagan.yaml. `linear` → fetch by id (quirk: the API
silently ignores a nonexistent project name — verify responses echo the
expected project). `local` → `tickets/<id>.md`. Then the hard gate:
**no AC block, no dispatch.** If AC is missing or ambiguous, draft it with
the human via needs-you questions first. AC amendments later in the run are
a dated entry in the ticket's Decisions block plus the AC block edited and
marked "Amended — see Decisions"; never a silent edit.

## Step 4 — Needs-you round + run.start

Collect every open decision (ticket choice, AC ambiguities, gate policy for
this run) into one structured question set with recommended defaults. Then
append `run.start` to `.sagan/ledger/events.jsonl` and proceed. `--dry-run`
stops here with the run plan.

## Step 5 — Drive the circuit

Per `references/run-protocol.md` (read it before the first dispatch):

1. **Build** — dispatch the builder as a subagent with a pointer pack
   (repo root, ticket path/id, role spec path). Access-check every pointer
   first. PM-direct execution is legal only for credentialed infra the
   builder can't reach — log `builder_id: pm-direct` with rationale.
2. **Critique** — fresh subagent, artifact-only inputs (artifact paths, AC
   block, builder rubric; never the builder's conversation). Validate the
   returned envelope: SCRIPTS `python3 scripts/validate_verdict.py`;
   NATIVE by inspection. Drifted envelopes go back for re-emission —
   contract drift is chronic.
3. **Verify** — on NEEDS_EVIDENCE or the standing ship requirement:
   a third subagent (never the builder) executes, binds evidence to
   `git rev-parse HEAD`, stores media under `.sagan/ledger/<ticket>/`,
   appends `evidence.recorded`. Ship predictable evidence with round 1
   (renders, screenshots) to save a critique round.
4. **Rounds** — REVISE loops back to build within `critique.circuit_breakers`
   caps from sagan.yaml; at cap, or on the same finding failing
   `same_finding_failures` times, the verdict becomes ESCALATE → needs-you.
   Every dispatch and verdict is a ledger event as it happens.

## Step 6 — Promote gate

Per-ticket human gate, always: present the verdict, evidence summary, and
SHA as a needs-you question (promote / send back / abandon). Append
`decision.made`; update the ticket's QA and Decisions blocks; close the
ticket in its store only on promote.

## Step 7 — Retro + synthesis

Confirm workers wrote `.sagan/memory/<ticket>-<role>.md` retros; synthesize
durable lessons into `.sagan/MEMORY.md`, prune the scratch files, append
`run.completed`. Report honestly (spec A12): verdicts by round, evidence
recorded vs not-executable, gates crossed, anything skipped.

## Conventions this skill follows

- Spec is `~/.claude/skills/skill-architecture.md`.
- Scripts: JSON stdout / diagnostics stderr / graceful failure (spec A4).
- Keyless; no network beyond the ticket store the project already uses.
- Enforcement is PM-interpreted at v0 (sagan.yaml `enforced: []` is honest);
  the runtime tier is tracked separately (WHA-134).

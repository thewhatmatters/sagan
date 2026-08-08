---
name: sagan-run
description: >-
  Drive one Sagan run through the circuit in a project already wired with
  the .sagan/ overlay — the PM-side dispatch loop that picks up where
  /sagan-start's run brief ends. Requires an AC-gated ticket, surfaces open
  decisions as structured questions with recommended defaults, then drives:
  builder dispatch with pointer packs → fresh artifact-only critic
  (APPROVED/REVISE/NEEDS_EVIDENCE/ESCALATE, envelope validated) → verifier
  (never the builder, evidence bound to a git SHA) → human promote gate →
  retro synthesis, every event ledgered. Also configures the agents a run
  needs: consent-gated, idempotent generation of .claude/agents/
  sagan-<role>.md from .sagan/roles/*.md. Use when the user says "run
  sagan", "do a sagan run", "sagan test run", "drive the circuit", "run
  this ticket / the brief through sagan", "dispatch WHA-123 through the
  loop", or "/sagan-run [ticket]". NOT the run opener (ticket mirroring,
  AC authoring, scope — that's /sagan-start) and NOT installation (missing
  .sagan/ → sagan-wire).
---

# sagan-run

Drive one Sagan run: agent configuration and the build → critique → verify
→ promote **circuit**, PM-interpreted (v0). Opener is `/sagan-start`; this
skill consumes its run brief and owns everything from first dispatch to
`run.completed`.

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

"run sagan", "drive the circuit on this brief", or `/sagan-run [ticket-id]`.
Normal sequence: `/sagan-start` produces the run brief → this skill runs it.

## Flags

| Flag | Meaning |
|------|---------|
| `--agent` | non-interactive; no prompts/pauses (spec A7b/A9). Gates cannot be crossed: the run stops at the first needs-you or promote gate and reports what it needs |
| `--brief=PATH` | run brief from sagan-start (default: newest `.sagan/ledger/*/run-brief.md`) |
| `--ticket=ID` | shortcut without a brief — legal only when the ticket already carries an AC block |
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
  sagan-wire ("wire this project to sagan"); this skill never installs.
- `NO_ROLES` (down) — `.sagan/roles/` empty or absent; re-run sagan-wire.
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

## Step 3 — Load the brief + AC gate

Load the run brief (`--brief`, else the newest
`.sagan/ledger/*/run-brief.md`); it names the ticket mirror(s) at
`tickets/<ID>.md`. No brief and no `--ticket` → point to `/sagan-start` and
stop. With `--ticket` alone, read the mirror directly. Either way, re-check
the hard gate before dispatch: **no AC block, no dispatch** — sagan-start
gates AC at open time, but the mirror may have changed since. AC amendments
mid-run are a dated entry in the ticket's Decisions block plus the AC block
edited and marked "Amended — see Decisions"; never a silent edit. Writeback
of repo-owned blocks to Linear goes through `/sagan-start --writeback=ID`
(verbatim), never ad-hoc API edits.

## Step 4 — Needs-you round + run.start

Collect every open decision left by the brief (AC ambiguities, gate policy
for this run, round-cap overrides) into one structured question set with
recommended defaults. If sagan-start already logged this run's `run.start`,
do not double-log — append `dispatch` events from here on. Otherwise append
`run.start` now. `--dry-run` stops here with the run plan.

## Step 5 — Drive the circuit

Per `references/run-protocol.md` (read it before the first dispatch):

1. **Build** — read the ticket's `## Method` block first: items shape the
   dispatch, lane picks the round cap, round-1 evidence goes to verify's
   standing list, reference (if any) feeds the critic's comparative bar.
   Then dispatch the builder as a subagent with a pointer pack (repo
   root, ticket path/id, role spec path). Access-check every pointer
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

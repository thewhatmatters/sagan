# agent-fleet — test bed for the agent-org v3.3 design

## What this project is

A minimal test bed for the PM-hub / SME-fleet orchestration design
(vault: `ideas/agent-org-pm-sme-fleet.md`, v3.3). The goal is to exercise
the contract-shaped parts of the design — role specs, AC-before-dispatch,
the critique/verify/evidence loop, ESCALATE behavior, and the memory
tiers — with files and subagents, before any Conan runtime work exists.

## Working agreements (v0)

- The PM (the interactive Claude Code session) reads `.agent/fleet.yaml`
  and enforces its rules by hand. **Known v0 limitation: enforcement is
  model-interpreted, not runtime code.** This is acceptable only because a
  human supervises every run.
- No work is dispatched before the ticket's Acceptance Criteria block is
  written. Critic without AC is opinion; critic against AC is a contract.
- Builders never self-approve. The critic never fixes. Verify is never the
  builder.
- Critic verdicts: `APPROVED | REVISE | NEEDS_EVIDENCE | ESCALATE`.
  APPROVED means verified, not plausible — user-visible artifacts need
  execution evidence recorded at a git SHA before they count as done.
- Every dispatch, verdict, and evidence record is appended to
  `.agent/ledger/events.jsonl`.
- Retros: each worker writes what went well/wrong to `.agent/memory/`;
  the PM synthesizes into `.agent/MEMORY.md` and prunes the scratch.
- The PM surfaces outstanding decisions to the human as a structured
  question set with recommended defaults (the Needs-you queue) — at
  gates, at run end, and whenever decisions accumulate. This is a PM
  role requirement across any provider binding, not a Claude Code
  feature.

## Layout

| Path | What |
|------|------|
| `.agent/fleet.yaml` | wiring: bindings, critique policy, caps, gates |
| `.agent/roles/*.md` | provider-neutral role specs |
| `.agent/memory/` | per-task retro scratch (pruned after synthesis) |
| `.agent/MEMORY.md` | rolling project learnings |
| `.agent/ledger/events.jsonl` | poor-man's event store |
| `tickets/` | local ticket files (Linear stand-in for v0) |
| `src/` | build output |

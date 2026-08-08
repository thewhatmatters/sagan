# sagan — reference implementation and test bed for the agent-org design

## What this project is

A minimal test bed for the PM-hub / SME-fleet orchestration design
(vault: `ideas/agent-org-pm-sme-fleet.md`, v3.4). The goal is to exercise
the contract-shaped parts of the design — role specs, AC-before-dispatch,
the critique/verify/evidence loop, ESCALATE behavior, and the memory
tiers — with files and subagents, before any Conan runtime work exists.

## The toolkit (three skills, one per phase)

`sagan-wire` installs the `.sagan/` overlay; `sagan-start` opens a run
(mirror the ticket store, script-enforced AC gate, scope question, run
brief); `sagan-run` drives the circuit (dispatch → critique → verify →
promote gate → retro synthesis). Skills live in `skills/` in this repo —
the installed copies under `~/.claude/skills/` are symlinks into it.

## Working agreements (v0)

- The PM (the interactive Claude Code session) reads `.sagan/sagan.yaml`
  and enforces its rules by hand. **Known v0 limitation: enforcement is
  model-interpreted, not runtime code** — the one exception is
  `ac_before_dispatch`, enforced by `sagan-start`'s precheck exit code.
  This is acceptable only because a human supervises every run.
- The human briefs in plain prose (what / how / what done means, plus a
  closing "can't hit one? stop and say why" line). The PM compiles that
  brief into the ticket's contract — the prose stays as the description
  verbatim; the how-paragraph becomes `## Method` (items, lane, round-1
  evidence, reference); each done-clause becomes one `## AC` item — and
  the human confirms the compile at a gate before any dispatch. Anything
  the brief leaves open is proposed at the gate, never guessed.
- No work is dispatched before the ticket's Acceptance Criteria block is
  written. Critic without AC is opinion; critic against AC is a contract.
- An adjective is never a criterion: quality bars name a reference or a
  concrete craft check and are judged blind by the critic on verify's
  evidence.
- Builders never self-approve. The critic never fixes. Verify is never the
  builder.
- Critic verdicts: `APPROVED | REVISE | NEEDS_EVIDENCE | ESCALATE`.
  APPROVED means verified, not plausible — user-visible artifacts need
  execution evidence recorded at a git SHA before they count as done.
- Every dispatch, verdict, and evidence record is appended to
  `.sagan/ledger/events.jsonl`.
- Retros: each worker writes what went well/wrong to `.sagan/memory/`;
  the PM synthesizes into `.sagan/MEMORY.md` and prunes the scratch.
- The PM surfaces outstanding decisions to the human as a structured
  question set with recommended defaults (the Needs-you queue) — at
  gates, at run end, and whenever decisions accumulate. This is a PM
  role requirement across any provider binding, not a Claude Code
  feature.
- Role specs: the `sagan-wire` template (`skills/sagan-wire/assets/
  template/roles/`) is the source of truth; `.sagan/roles/` is synced
  from it, never hand-forked.

## Layout

| Path | What |
|------|------|
| `.sagan/sagan.yaml` | wiring: bindings, critique policy, caps, gates, ticket store + mirror |
| `.sagan/roles/*.md` | provider-neutral role specs (synced from the sagan-wire template) |
| `.sagan/memory/` | per-task retro scratch (pruned after synthesis) |
| `.sagan/MEMORY.md` | rolling project learnings |
| `.sagan/ledger/events.jsonl` | poor-man's event store (evidence media per ticket, gitignored) |
| `tickets/` | ticket mirrors (tracker-owned + repo-owned regions); `T-000-example.md` is the worked sample |
| `skills/` | sagan-wire · sagan-start · sagan-run (distributed from this repo) |
| `site/` | sagan.run (Astro, static; brand spec served at /design.md) |
| `src/` | build output |

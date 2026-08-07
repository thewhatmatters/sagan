# start-sagan

**What it is:** Start and drive one Sagan run in a wired project — startup
checks, agent configuration, and the build → critique → verify → promote
circuit, PM-interpreted.

## What you get

- One ticket driven through the full Sagan circuit with every dispatch,
  verdict, and evidence record appended to `.sagan/ledger/events.jsonl`.
- Evidence bound to a git SHA (media under `.sagan/ledger/<ticket>/`) and a
  human promote decision before anything closes.
- Optional generated agent definitions (`.claude/agents/sagan-<role>.md`)
  derived from your `.sagan/roles/*.md` specs.

## How to run

Say "start sagan" or "run WHA-123 through sagan", or `/start-sagan WHA-123`.

## What it needs

A project already wired by **wire-sagan** (a `.sagan/` directory with
`sagan.yaml`, role specs, and a ledger). If that's missing, this skill stops
and points you to wire-sagan — it never installs.

## How it works (high level)

1. Checks the overlay is present and the ledger is writable.
2. Offers to generate per-role agent definitions from the role specs
   (consent-gated; skippable).
3. Fetches the ticket from the store sagan.yaml names (Linear or local
   `tickets/`) and refuses to dispatch until an Acceptance Criteria block
   exists.
4. Surfaces every open decision to you as structured questions with
   recommended defaults, logs `run.start`, then drives builder → fresh
   critic → verifier rounds within the configured caps.
5. Stops at the promote gate — you decide; then it synthesizes retros into
   `.sagan/MEMORY.md` and logs `run.completed`.

## Where to look next

- `SKILL.md` — operating instructions Claude follows.
- `handoff.md` — design decisions and the "why".
- `references/run-protocol.md` — per-station dispatch contracts and ledger
  event shapes.
- `references/agent-definitions.md` — how agent files are generated from
  role specs.

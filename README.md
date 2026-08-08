# Sagan

**Evidence-based multi-agent orchestration.** Named for Carl Sagan's rule:
*extraordinary claims require extraordinary evidence.* In Sagan, `APPROVED`
means verified — not plausible.

One accountable PM agent dispatches stateless specialist workers (frontend,
backend, research, …) against tickets whose acceptance criteria are written
*before* any work starts. Every boundary-crossing artifact faces a fresh,
isolated critic that can demand execution evidence instead of approving on a
read — and nothing user-visible ships without a non-builder verifier
recording commands, exit codes, and screenshots at a git SHA. It installs as
a self-contained `.sagan/` directory in any existing project; humans stay in
the loop through per-ticket promote gates and structured decision queues.

This repo is the **reference implementation**: the overlay, the role specs,
and a complete evidenced ticket run.

## The loop

```mermaid
flowchart LR
    AC[Ticket + AC\nwritten first] --> B[Builder\nrole-bound worker]
    B -->|artifact @ digest| C{Critic\nfresh · artifact-only}
    C -->|NEEDS_EVIDENCE| V[Verify\nexecutes · never the builder]
    V -->|evidence @ SHA| C
    C -->|APPROVED| G[Promote gate\nhuman decision]
    C -->|REVISE| B
    C -->|ESCALATE| H[Needs-you queue]
    G --> S[Shipped\nlineage in ledger]
```

Every dispatch, verdict, and evidence record lands in
`.sagan/ledger/events.jsonl` — the audit trail answers *which attempt
produced this, who judged it, against what evidence, and why it was
accepted.*

## The rules

| Rule | Meaning |
|---|---|
| AC before dispatch | Critic without AC is opinion; critic against AC is a contract |
| Adjectives are not criteria | Quality bars name a reference and are judged blind by the critic — mechanical or comparative, never "looks great" |
| Flags, never fixes | The critic judges; the builder fixes; nobody self-approves |
| Builder ≠ verifier | Structural, not cultural — the verifier is never the builder |
| Reading is not judging | `NEEDS_EVIDENCE` exists so render/runtime claims require execution output |
| APPROVED = verified | Ship requires critic approval **and** non-builder evidence at a git SHA |
| Caps are circuit breakers | Round limits → `ESCALATE` to a human, never silent approval |
| Decisions surface structurally | The PM presents open decisions as batched questions with recommended defaults — never buried in prose |

Verdicts: `APPROVED | REVISE | NEEDS_EVIDENCE | ESCALATE`.

## What's in the overlay

```
.sagan/
  sagan.yaml      # wiring: bindings, critique policy, round caps, gates,
                  #   your project's real test/typecheck/build commands
  roles/          # provider-neutral role specs (mission, inputs,
                  #   output contract, rubric)
  tickets/        # the work contracts (AC + per-role blocks + decisions)
  memory/         # per-task retros (pruned after synthesis)
  MEMORY.md       # rolling project learnings
  ledger/         # events.jsonl + evidence (screenshots, check records)
```

One directory to add; delete it to un-wire.

## Tickets are mirrored, not paraphrased

Context packs are **pointers** — a path and a ticket id, never a retyped copy.
That only works if the pointer resolves for the worker receiving it, so when
the ticket store is a tracker, Sagan mirrors each ticket to `tickets/<ID>.md`
and hands workers the file. Two things fall out of it: the acceptance criteria
sit in git at the same commit as the evidence, and no agent ever reads a
ticket that a PM retyped from memory.

The mirror has exactly **one writer per field**:

| | Owns | On fetch |
|---|---|---|
| **Tracker** | title, status, priority, assignee, description | regenerated |
| **Repo** | AC, Frontend, QA, Decisions, `builder_id`, `verifier_id`, `evidence_sha` | never touched |

Two writable copies of one field have no merge algorithm, so no field has two
writers. Going back the other way, repo blocks return to the tracker **word for
word** with the git SHA — a summarized write-back would reintroduce, at the
sync boundary, exactly the paraphrase the pointer rule exists to prevent.

Sprint scope batches the *planning* — AC authoring and the decision round
across several tickets at once — and still builds one ticket at a time.
Concurrent builders need worktrees, a file-disjointness check, and a
sprint-level round cap; none of those exist yet, and nothing at v0 would catch
two agents editing the same file.

## Worked example: T-001

This repo ran its own first ticket. The trail is committed:

- [`tickets/T-001.md`](tickets/T-001.md) — AC written before dispatch;
  builder, verifier, and evidence SHA recorded on the ticket.
- Round 1: the critic returned `NEEDS_EVIDENCE` — it refused to approve
  375px legibility and dark-mode rendering from reading source, and caught
  an AC clause it couldn't judge from inside its isolation set.
- Verify bound evidence to commit `03f2d22`:
  [screenshots at both widths in both color schemes](.sagan/ledger/T-001/),
  a measured `scrollWidth` (no horizontal scroll), and quoted attestations.
- Round 2: a second fresh critic reviewed artifact **plus** evidence —
  `APPROVED`, zero findings. Human promoted at the gate.
- Every step: [`.sagan/ledger/events.jsonl`](.sagan/ledger/events.jsonl).

## Using it in your project

Sagan v0 is files + protocol — any capable coding agent session can act as
the PM by reading `sagan.yaml` and the role specs.

- **With the installer** (a [Claude Code](https://claude.com/claude-code)
  skill, `sagan-wire`): probes your project's entry point (CLAUDE.md /
  AGENTS.md), captures your real gate commands into `sagan.yaml`, installs
  the overlay, and wires one consent-gated marker block so future sessions
  are Sagan-aware. Supports `--update` resync with local-edit detection.
- **Manually:** copy `.sagan/` from this repo, empty the ledger and
  tickets, set your gate commands in `sagan.yaml`, and point your agent's
  project context at it.

Then: copy `tickets/T-000-example.md`, write the AC, and run it through the
loop with the two run skills — tickets can live as files in your repo or in
Linear.

The toolkit is three skills, one per phase:

- **`sagan-wire` installs** (above).
- **`sagan-start` opens.** The startup sequence in order: read
  `sagan.yaml`, mirror the ticket store into local markdown, check every
  ticket's AC (no criteria → non-zero exit, not a reminder), ask whether
  this is one ticket or a sprint, log `run.started`, and hand back a
  dispatch-ready brief. `--writeback=<ID>` sends a ticket's repo blocks
  back to the tracker verbatim.
- **`sagan-run` drives.** It consumes the brief and owns the circuit:
  dispatches the builder with pointer packs, a fresh artifact-only critic
  (verdict envelope schema-validated), a verifier that is never the
  builder and binds evidence to a git SHA, round caps that escalate
  instead of quietly shipping — and stops at the promote gate, which is
  yours. Retros synthesize into `.sagan/MEMORY.md` when the run closes.

### What a ticket looks like

One markdown file per ticket, frontmatter split by owner, two regions —
the tracker's and the repo's. The repo-owned blocks follow a
What → How → Bar spine: the description says what, `## Method` says how
*this* ticket gets built (item decomposition, correctness-or-quality lane,
round-1 evidence, a comparison reference when the bar is comparative),
and `## AC` is the bar — mechanical criteria, or a blind comparison
against a named reference for quality-shaped work. Never adjectives.
Abridged from WHA-151, the run that shipped the site's footer link (full
anatomy: [`tickets/T-000-example.md`](tickets/T-000-example.md)):

```markdown
---
id: WHA-151
title: Footer design.md link on sagan.run
status: Done
# repo-owned — set by the run, carried across every fetch
builder_id: frontend-claude-r1
verifier_id: verify-claude-r1     # never the builder
evidence_sha: d4e6fc9             # proof binds to this commit
---

<!-- sagan:linear-owned:start — regenerated on every fetch -->
The description, mirrored verbatim from the tracker.
<!-- sagan:linear-owned:end -->

<!-- sagan:repo-owned:start — agents write here; a fetch never touches it -->
## AC
1. Exact visible label `design.md`, href `/design.md`, placed after
   the sagan.run link, using the row's existing separator idiom.
2. `npm run build` exits 0; dist contains `href="/design.md"`.
3. At 375px and 1280px: all three links, no horizontal overflow.

## Method
items: footer row · lane: correctness
round-1 evidence: 375/1280px captures, JS-disabled render

## Frontend
r1 build note — what was built, key choices, nothing self-approved.

## QA
r1 verify — per-AC PASS/FAIL with evidence at `d4e6fc9`.

## Decisions
2026-08-07 — promote gate (human): promote.
<!-- sagan:repo-owned:end -->
```

## Status — v0, honest

- ✅ Validated: the contract-shaped loop (AC-first, isolated critique,
  evidence-bound verification, promote gates, memory tiers) — proven by
  the T-001 run, and re-proven skill-driven end to end by WHA-151 (the
  first `sagan-start` → `sagan-run` circuit: round-1 APPROVED on real
  evidence, with a schema-clean critic envelope).
- ⚠️ Mostly not built yet: **runtime enforcement.** Round caps, critic
  isolation and gates are still interpreted by the PM model, not enforced by
  code. The one exception is `ac_before_dispatch`: when a run opens through
  `sagan-start`, a ticket with no enumerated acceptance criteria fails with a
  non-zero exit code rather than a reminder. Dispatch by hand and nothing
  checks it. That asymmetry is the point of the roadmap item — nothing
  safety-critical should depend on a model remembering to stop.
- Roadmap: enforced tier (caps, isolation, containment floors as code),
  provider-heterogeneous bindings (Claude / Codex / Grok / Kimi with
  per-binding containment levels), event-store + team surface.

The design behind this survived three adversarial review rounds (QA,
product/architecture, driver-level code review) before v0 was built.

---

*A fleet of small vessels, steered by evidence.* — sagan.run

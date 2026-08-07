# sagan-run — Handoff & decisions

Living record of what this skill is, the decisions behind it, and any
non-obvious constraints (spec A12).

Created: 2026-08-07  ·  Generator: generate-skill @ CC 2.1.223

## 1. Purpose

Start and drive one Sagan run in a wired project — startup checks, agent
configuration, and the build → critique → verify → promote circuit,
PM-interpreted.

## 2. Reusable patterns (link to spec A1..A15)

This skill follows `~/.claude/skills/skill-architecture.md` patterns A1–A15;
deliberate notes:

- Three-skill split: **wire-sagan installs, sagan-start opens (mirror +
  AC gate + scope + brief), sagan-run drives (dispatch → circuit →
  promote → retro).** Missing overlay is a hard stop with a pointer, never
  an inline install (single-responsibility, and wire-sagan's consent
  choreography must not be duplicated); missing brief points to
  /sagan-start the same way.
- Leading words (spec A14): **circuit**, **pointer pack**, **needs-you** —
  chosen to match the vocabulary already used in `.sagan/` and the fleet
  design doc so ledger entries, role specs, and skill reasoning agree.
- Agent-definition generation copies wire-sagan's marker-block idiom:
  consent first, idempotent regeneration, source of truth stays in
  `.sagan/roles/*.md` (the generated file says so in its marker).

## 3. Decision log

- 2026-08-07: renamed start-sagan → sagan-run after a concurrent-session
  collision: another session shipped `sagan-start` (run opener: ticket
  mirror with one-writer-per-field, script-enforced AC gate, scope
  question, run brief; v1 deliberately stops before dispatch) minutes
  before this skill landed. The two split cleanly — opener vs driver —
  so this skill dropped its duplicated opener steps (ticket fetch, AC
  authoring) and now consumes sagan-start's run brief. Trigger modes
  differ deliberately: sagan-start is user-invoked (/sagan-start);
  sagan-run stays model-invoked so "do a sagan run" routes here, and its
  Step 3 redirects to /sagan-start when no brief exists.
- 2026-08-07: scaffolded by generate-skill, codifying the startup sequence
  recorded in `.sagan/MEMORY.md` ("read sagan.yaml → fetch ticket → check
  AC/blockers/gates → surface decisions as structured questions → log run
  start → dispatch with pointer packs") plus the run lessons from T-001 and
  the sagan.run site run.
- 2026-08-07: model-invoked (A14) despite being side-effectful, following
  the wire-sagan precedent: every write inside the run is either
  ledger-append (the skill's core contract) or consent-gated (agent files,
  promote, ticket close). The run itself is human-supervised by design —
  the promote gate cannot be crossed under `--agent`.
- 2026-08-07: verdict-envelope validation gets a script
  (`validate_verdict.py`) because critic contract drift was chronic in real
  runs (3× a stray `notes` field); PM-side validation is the v0 stand-in
  for runtime schema enforcement (WHA-134).
- 2026-08-07: post-audit fixes (skill-auditor, 0 critical/high, 2 medium):
  added model-side session-dependency probes to Step 0 (Agent tool absent →
  honest stop, isolation cannot degrade; linear store without the Linear
  MCP connector → needs-you gate to a local mirror), documented the
  `CONFIG_UNREADABLE`/`NO_GIT` down gates the script already emitted, and
  dropped preflight.py's dead `--agent` flag.
- 2026-08-07: folded-in run lessons — dispatch access check (pointers must
  resolve for the receiving worker); AC amendments are dated Decisions
  entries + an AC block marked Amended, never silent edits; Linear
  save_issue silently ignores nonexistent project names (verify the echo);
  ship predictable evidence with round 1; `builder_id: pm-direct` only for
  credentialed infra, with rationale.

## 4. Known limitations / environment caveats

- v0 enforcement is PM-interpreted: this skill *procedurally* honors round
  caps, isolation, and gates, but nothing at runtime prevents a
  misbehaving session from ignoring them. `sagan.yaml` says the same.
- The Linear binding assumes the session has the Linear MCP connector;
  local `tickets/` is the keyless fallback and the only store `--agent`
  can use non-interactively.
- Verify's render checks degrade honestly when Playwright is unavailable
  (documented as NOT verified, never claimed).

## 5. Audit rubric coverage

See `skill-architecture.md` §B; this skill targets every PASS that applies.

## 6. Notes

Depends on a wire-sagan-installed overlay; ticket store per sagan.yaml
(Linear MCP or local tickets/). Generated while the 2.1.144 → 2.1.223 docs
drift is open (new frontmatter fields background/compatibility/
disallowed-tools/license/metadata); conservative `name` + `description`
set used, valid in both.

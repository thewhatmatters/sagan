# Agent definitions — generating .claude/agents/ from role specs

Loaded by SKILL.md Step 2 only when the user accepts the offer (spec A1).

## Contract

- Source of truth is ALWAYS `.sagan/roles/<role>.md`. The generated agent
  file is a thin binding, regenerated freely; hand edits belong in the role
  spec, not the agent file.
- One file per role: `.claude/agents/sagan-<role>.md` in the wired project.
- Idempotent: regeneration overwrites only files carrying the marker; a
  same-named file WITHOUT the marker is never touched (report it instead).
- Consent: one needs-you question lists every file that would be written,
  before anything lands. `--agent` mode prints; never writes.

## Template

```markdown
---
name: sagan-<role>
description: >-
  Sagan <role> worker for this project. Dispatched by the start-sagan PM
  loop with a pointer pack (ticket path, role spec path, artifact paths).
  Follows .sagan/roles/<role>.md to the letter. Not for ad-hoc use outside
  a Sagan run.
tools: <see per-role table>
---

<!-- start-sagan:generated from .sagan/roles/<role>.md — edit the role spec, then regenerate -->

You are the Sagan **<role>** worker. Read the role spec at
`.sagan/roles/<role>.md` and the ticket's AC block named in your dispatch
BEFORE doing anything else. The role spec's Mission, Inputs, Output
contract, and Boundaries govern; your dispatch prompt only supplies the
pointers. Honor isolation: use only the inputs the role spec allows.

<!-- start-sagan:end -->
```

## Per-role tool sets

| Role | tools | Why |
|------|-------|-----|
| frontend | Read, Edit, Write, Glob, Grep, Bash | builds artifacts; needs the file tools and the project's build commands |
| critic | Read, Glob, Grep | artifact-only judgment; no edit tools (flag, never fix), no Bash (reading is not judging — execution belongs to verify) |
| verify | Read, Bash, Glob, Grep, Write | executes builds/renders and writes evidence + ledger lines; never edits source |

Roles beyond the standard three (installed via wire-sagan `--roles=`): map
tools from the role spec's Output contract — writers get Write, judges
don't, executors get Bash — and note the mapping in the consent question.

## Fallback without generated agents

Dispatch works identically through generic subagents: the pointer pack's
role-spec path carries the contract. Generated definitions add typed tool
restriction (structural isolation instead of prompt-trusted isolation) —
that is their entire value; say so in the consent question so the choice
is informed.

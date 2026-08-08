---
name: sagan-start
disable-model-invocation: true
description: >-
  Start a Sagan run in a wired project — mirror the ticket store into local
  markdown, check every ticket's acceptance criteria, ask the human whether
  this is one ticket or a sprint, log the run, and hand back a dispatch-ready
  brief. Also carries repo-owned ticket blocks back to Linear word for word
  (--writeback). Companion to sagan-wire, which installs the overlay but never
  runs the loop. User-invoked: /sagan-start.
---

# sagan-start

Open a Sagan run: fetch → mirror → gate on AC → scope with the human → log.
**v1 stops before dispatch** (Step 7) — it produces the brief; you read it and
dispatch.

## Leading words

- **mirror** — the local markdown copy of a tracker ticket at
  `tickets/<ID>.md`. Makes the ticket a *resolvable pointer* for every worker,
  so a context pack never has to paraphrase it.
- **one writer per field** — Linear owns the frontmatter and the
  `sagan:linear-owned` region; the repo owns `sagan:repo-owned`. A fetch
  regenerates the first and never touches the second. Enforced in `mirror.py`,
  not remembered.
- **AC gate** — `precheck.py --require-ac` exits non-zero when a selected
  ticket has no enumerated acceptance criteria. This is the one rule in
  `sagan.yaml` that is actually enforced at v0; every other rule is still
  model-interpreted.
- **scope** — `ticket` (one) or `sprint` (batch the *planning*, still build one
  at a time). Sprint scope never means concurrent builders at v0.
- **verbatim write-back** — repo blocks return to Linear as a byte copy, never
  a summary. `writeback.py` composes the payload so there is no paraphrase step.

## How to run

`/sagan-start` in a project with a `.sagan/` overlay. Details of the mirror file
format and field ownership: `references/mirror-format.md`.

## Flags

| Flag | Meaning |
|------|---------|
| `--agent` | non-interactive; no prompts. Scope defaults to `ticket` on the single ready ticket, or ESCALATEs to the Needs-you queue if that is ambiguous |
| `--project=PATH` | project root (default: cwd) |
| `--scope=ticket\|sprint` | skip the scope question |
| `--ticket=ID[,ID]` | explicit selection; skips the scope question |
| `--no-fetch` | work from the existing mirror (offline / tracker down) |
| `--writeback=ID` | secondary mode: post repo-owned blocks back to Linear verbatim, then stop |
| `--dry-run` | plan and report; write nothing, append nothing, post nothing |
| `--out=PATH` | run brief location (default `.sagan/ledger/<run-id>/run-brief.md`) |

## Step 0 — Mode probe

`python3 --version` + `scripts/` present → **SCRIPTS**. Otherwise **NATIVE**:
do the same steps with built-in file tools, and say plainly in the report that
the AC gate ran as judgment rather than as an exit code.

## Step 1 — Preflight

`python3 scripts/preflight.py --project=<path>`. `down` → STOP (no overlay:
suggest `/sagan-wire`). `MIRROR_NOT_IGNORED` is a **Setup Gate**: mirroring a
private tracker into a repo commits its ticket ids. Offer *add the ignore rule
/ commit them deliberately / skip* — under `--agent`, add the rule and record it.
`LINEAR_FETCH_UNVERIFIED` is expected: only Step 2 can prove the store is live.

## Step 2 — Fetch and mirror

Skip under `--no-fetch`. Read `ticket.store` from the preflight JSON.

1. Enumerate with `list_issues`, scoped to `ticket.project` from `sagan.yaml`,
   `fields: [title, description, status, priority, assignee, labels, url,
   updatedAt]` (`id` always comes back, and it carries the `WHA-…` identifier).
2. **`list_issues` truncates long descriptions.** Re-fetch every issue you
   intend to mirror with `get_issue` to get the full text. A truncated
   description would put a half-written AC in front of a builder, so
   `mirror.py` refuses any record still carrying the truncation marker — that
   refusal is the guard working, not a bug to route around.
3. Pipe the full records into `python3 scripts/mirror.py --project=<path>` as
   `{"issues":[…]}`. Do not reformat on the way — the script normalizes.
4. Read the result. `refused` entries are **fail-closed**: either the
   description was truncated (re-fetch) or a mirror file had repo-owned content
   the script could not locate (resolve by hand — never by deleting the file).

A fetch that returns zero issues is a finding, not an empty success — say so.

## Step 3 — Precheck

`python3 scripts/precheck.py --project=<path>`. Gives per-ticket AC presence,
item count, blockers, role ids, and `dispatch_ready`. This output is what makes
Step 4's question answerable — never ask the human to pick scope before it runs.

## Step 4 — Scope (skip under `--agent`, `--scope=`, or `--ticket=`)

One `AskUserQuestion` round, options built from Step 3's real data — never a
bare "one or many?". Name the actual ids and their readiness, e.g.:

- *Just WHA-133* — the one dispatch-ready ticket
- *Sprint: WHA-133 + WHA-134* — plan both now, build in order; WHA-135 excluded (no AC)
- *Author AC for WHA-135 first* — nothing dispatches until it has criteria

Sprint means batched planning and a dependency-ordered queue. It does **not**
mean concurrent builders: `enforced: []` at v0, so nothing but you would catch
two builders editing the same file.

## Step 5 — Surface decisions

A ticket that is still plain prose is never the human's homework. When a
selected ticket has a description but no enumerated AC, the PM **drafts**
the AC and Method blocks from that prose (What → How → Bar: judgeable
criteria, items, lane, round-1 evidence, a comparative bar with a named
reference when the ask is quality-shaped) and presents the draft for
confirmation in this round — the human approves or edits, never authors
blocks from scratch.

Collect every open decision across the selected tickets — drafted AC/Method
awaiting confirmation, AC ambiguities from Step 3, `blocked_by` chains,
unresolved `## Decisions` entries — and put them in
**one** structured question round with a recommended default each. Batching them
is the PM requirement in `sagan.yaml` (`surface_decisions: structured-questions`),
not a convenience. Log each as `decision.needed` via `scripts/ledger.py`.

## Step 6 — Log and brief

`python3 scripts/ledger.py --project=<path> --event=run.started
--tickets=<ids> --json='{"scope":"…","store":"…","pm":"claude-code-session"}'`.
Keep the returned `run_id`. Then write the run brief (`--out`): the request, the
date, scope, selected tickets with AC item counts, decisions asked and answered,
refusals and gates hit, and the `run_id`. The brief is the run's self-contained
artifact — produce it in every mode, including `--agent` and `--dry-run`.

## Step 7 — Report and stop

Report: tickets mirrored (created/updated/unchanged), AC gate result, scope
chosen, decisions outstanding, `run_id`, brief path. Then **stop and hand the
brief back** — v1 does not dispatch builders. Name the next command the human
would run to dispatch, so the boundary is explicit rather than a silent halt.

## Write-back mode (`--writeback=ID`)

1. `python3 scripts/writeback.py --project=<path> --ticket=<ID>` → a finished
   `body` string.
2. `post: false` → stop; nothing changed since the last sync.
3. Otherwise post `body` **exactly as returned** with the Linear MCP
   (`save_comment`, `issueId=<ID>`). Do not edit, trim, or re-word it — if it
   looks wrong, fix the ticket file and re-run, never the payload.
4. On success: re-run with `--record` to stamp the hash so the next run is a
   no-op instead of a duplicate comment.

## Conventions this skill follows

- Spec is `~/.claude/skills/skill-architecture.md`. Scripts: one concern each,
  JSON stdout / diagnostics stderr, graceful failure (A4).
- **User-invoked by design** (A14): it appends to the ledger, writes ticket
  files, and posts to a live tracker. The human picks the moment; keeping the
  description out of every session's context is the trade taken deliberately.
- Keyless and offline except the Linear MCP calls in Steps 2 and write-back —
  which the *session* makes, never a script. No secrets touch these files.
- Composes with sagan-wire (installs the overlay this skill runs against) and
  curate-vault (harvests `.sagan/MEMORY.md` after a run).
- Writes only inside `.sagan/`, the configured `tickets/` dir, and — with
  consent at the Step 1 gate — one `.gitignore` line.

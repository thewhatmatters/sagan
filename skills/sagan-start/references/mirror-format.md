# The ticket mirror — file format and field ownership

Read this when a mirror file looks wrong, a write was refused, or you are
adding a field. The rule the whole format exists to serve: **one writer per
field.** Two systems that can both edit the same field have no merge
algorithm and will drift.

## Anatomy

```markdown
---
id: WHA-133                 ← Linear-owned frontmatter: regenerated every fetch
title: Landing hero
status: In Progress
priority: High
assignee: randy
labels: site, copy
url: https://linear.app/…
linear_updated_at: 2026-08-07T09:00:00.000Z
fetched_at: 2026-08-07T14:29:08Z
mirror_version: 1
builder_id: frontend-claude ← repo-owned frontmatter: carried across a fetch
verifier_id: verify-claude
evidence_sha: 9be4459
---

<!-- sagan:linear-owned:start … -->
(the Linear description, verbatim — regenerated every fetch)
<!-- sagan:linear-owned:end -->

<!-- sagan:repo-owned:start … -->
## AC
## Frontend
## QA
## Decisions
<!-- sagan:repo-owned:end -->
```

## Ownership

| Field | Owner | On fetch |
|---|---|---|
| `id`, `title`, `status`, `priority`, `assignee`, `labels`, `url`, `linear_updated_at` | Linear | overwritten |
| `fetched_at`, `mirror_version` | mirror script | overwritten |
| `builder_id`, `verifier_id`, `evidence_sha`, `blocked_by`, `sagan_status` | repo | preserved |
| `ac_seeded_from`, `migrated_at`, `last_writeback`, `last_writeback_at` | mirror script (once) | preserved |
| `sagan:linear-owned` region | Linear | overwritten |
| `sagan:repo-owned` region (AC / Frontend / QA / Decisions) | repo | **never touched** |

The authoritative list is `REPO_OWNED_FM` in `scripts/_sagan.py`. Adding a
repo-owned frontmatter key means adding it there — nowhere else.

## AC seeding, once

If a ticket is mirrored for the first time and the Linear description already
contains an `## AC` (or `## Acceptance Criteria`) section, `mirror.py` lifts it
into the repo-owned AC block and stamps `ac_seeded_from: linear-description`.
It never lifts again on later fetches.

The description keeps its own copy, because that region is a verbatim mirror.
That would leave two AC blocks with no stated precedence, so the seeded block
carries an HTML comment saying it is the authoritative one. **Amend AC in the
repo block, never in the mirrored description** — and per the house rule, an
amendment is a dated `## Decisions` entry plus an edited AC block marked
"Amended — see Decisions", never a silent edit.

## Refusals are the feature

`mirror.py` exits 1 and writes nothing for a ticket when the existing file has
content but no `sagan:repo-owned` markers and no `## AC` anchor to migrate
from. It cannot tell which bytes an agent wrote, so it declines rather than
guess. Fix by hand: add the markers around the repo-owned content, or move the
file aside if it is genuinely stale. Never "resolve" a refusal by deleting the
file.

A file with markers is always safe to re-fetch, however stale.

## Write-back

`writeback.py` copies the repo-owned block bodies out byte-for-byte and returns
a finished `body`. Only the header line (`**Sagan sync** · sha · builder ·
verifier · evidence`) is generated. The session posts that string unedited —
composing the comment in the model is exactly the paraphrase the design forbids.

`last_writeback` holds a truncated SHA-256 of the payload. Equal hash →
`post: false`, so re-running a run does not stack duplicate comments on the
issue.

## Ids and hygiene

Mirror filenames are the tracker identifier (`WHA-133.md`).
`T-000-example.md` is the worked sample of this anatomy (copy it to author a
local-store ticket); `T-001.md` is a legacy pre-mirror ticket kept as run
history. `precheck.py` reads both; `mirror.py` touches neither — it only
writes files for ids fetched from the tracker.

A live mirror puts private tracker ids in the working tree. In a public repo,
keep `ticket.mirror.commit: ignore` in `sagan.yaml` and let the Step 1 gate add
the `.gitignore` rule. Set `commit: commit` only deliberately.

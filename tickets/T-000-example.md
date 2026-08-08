---
# ── tracker-owned (regenerated on every /sagan-start fetch; edit in Linear) ──
id: T-000
title: Example ticket (copy me)
status: Backlog
priority: Medium
assignee:
labels:
parent:
# url is the tracker issue link when store: linear; linear_updated_at is
# stamped by the fetch.
url:
linear_updated_at:
# ── mirror-script-owned (stamped by sagan-start, never by hand) ──────────────
fetched_at:
mirror_version: 1
# ── repo-owned (carried across every fetch; set by the run, not the tracker) ─
# builder_id is set at dispatch (e.g. frontend-claude-r1); verifier_id at
# verify and is NEVER the builder; evidence_sha is the commit evidence binds to.
builder_id:
verifier_id:
evidence_sha:
---

<!-- sagan:linear-owned:start — regenerated on every fetch; edit in Linear -->

The ticket's description, mirrored verbatim from the tracker. If you write an
`## AC` section here in Linear, the first fetch seeds it into the repo-owned
block below (once) and stamps `ac_seeded_from: linear-description`.

Local-store projects (`ticket.store: local`): you author this whole file by
hand — keep both regions so the file stays fetch-safe if you attach a tracker
later.

<!-- sagan:linear-owned:end -->

<!-- sagan:repo-owned:start — agents write below; a fetch never touches this region -->
## AC

Write acceptance criteria BEFORE any dispatch — no criteria, no work. Rules
learned the hard way:

1. Every clause must be judgeable from some role's declared input set — a
   clause referencing an external document must either ship that document
   in the critic's pack or be routed to verify as a quoted attestation.
2. Pin exact strings where wording matters; explicitly permit paraphrase
   or local variation where it doesn't. Ambiguities multiple workers flag
   independently are AC bugs.
3. Prefer criteria testable by command or observation (verify must be able
   to mark each item PASS/FAIL with evidence).

Shaped like the real thing (from WHA-151, approved round 1):

1. `<file>` gains `<exact element>` with exact visible label `<string>`,
   placed `<exact position>`, using `<the existing idiom, quoted verbatim>`.
2. No new CSS, no JavaScript, no new external network resources.
3. The change is confined to `<file>`.
4. `<build command>` exits 0 and the built output contains `<exact string>`.
5. Rendered at 375px and 1280px: `<observable>` with no horizontal overflow.
6. `<the artifact>` works with JavaScript disabled.

Quality-shaped work gets a **comparative bar**, never adjectives — name a
reference and make the judgment a procedure:

7. The fresh critic views verify-supplied captures of `<the artifact>` and
   `<named reference>` blind, and must prefer ours on `<explicit axes>`.
   ("Visually beautiful" is not a criterion; losing a blind comparison is.)

## Method

Authored with the AC, before dispatch. Only what varies per ticket — the
circuit itself (fan-out, fresh critic, verify, caps) lives in `sagan.yaml`
and the role specs, never here.

- **items:** the independently buildable pieces, each traceable to an AC
  item, each checked on its own
- **lane:** correctness | quality — picks the round cap from `sagan.yaml`
- **round-1 evidence:** what verify ships with the first build (renders,
  captures, comparisons), so critique never burns a round asking for
  predictable proof
- **reference:** `<comparison artifact>` — only when the AC carries a
  comparative bar

## Frontend

(builder appends its build note here — what was built, key choices,
anything the AC left ambiguous. Builders never render-check their own work.)

## QA

(verify appends the evidence summary here — per-AC PASS/FAIL with the
command or observation that decided it, bound to `evidence_sha`.)

## Decisions

(the PM logs dated entries here: pre-dispatch decisions, AC amendments —
"Amended — see Decisions", never a silent edit — and the promote decision.)

<!-- sagan:repo-owned:end -->

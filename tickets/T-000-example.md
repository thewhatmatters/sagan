---
# ── tracker-owned (regenerated on every /sagan-start fetch; edit in Linear) ──
id: T-000
title: Marketing hero — headline, subhead, one CTA (shadcn primitives)
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

<!-- THIS is all the human wrote — three plain paragraphs (what, how, what
     done means) and one closing line. Everything below this region was
     compiled BY the PM agent from these words and confirmed by the human
     at a gate before any work. -->

Build the hero for sagan.run. Headline eight words or fewer, a subhead,
one CTA saying "Get started" → /docs. No secondary.

Only the shadcn primitives we have installed. Type-led — type carries the
hierarchy, whitespace is the design. One accent color, used once.
Everything from tokens. Nothing animates on load.

Done means all of these: delete the accent and it still reads premium;
nothing's filling space; a stranger knows what we do from the headline
and subhead alone; every value traces to a token; buttons are buttons;
one h1, heading order in sequence; focus visible, tab order follows
reading order; alt text or explicitly decorative; tap targets 44 by 44.

Any one of those you can't hit, stop and tell me which and why.

<!-- sagan:linear-owned:end -->

<!-- sagan:repo-owned:start — agents write below; a fetch never touches this region -->
## AC

<!-- Compiled by the PM, one clause of the brief's done-paragraph per
     item plus the how-paragraph's hard constraints; confirmed by the
     human at the needs-you gate — including what the brief left open
     (the exact headline was proposed there and approved). Mechanical
     items route to verify; judgment items route to the fresh critic on
     verify's evidence. The closing "stop and tell me which" line is the
     ESCALATE rule — a near-miss never ships quietly. -->

1. `src/components/marketing/hero.tsx` exports `Hero`, rendered at the
   top of `/`: an `h1` with exact text `Ship work you can prove.`
   (5 words; proposed by the PM at the gate, approved) and it is the
   page's only `h1`; a subhead; exactly ONE CTA — a shadcn `Button`
   reading `Get started` linking to `/docs` — and no other CTA.
2. Only primitives already under `@/components/ui/` appear in the diff;
   no new dependencies.
3. Tokens only: no arbitrary values (`[…]`) and no new hex colors in
   `git show`; the accent token appears exactly once in the hero; no
   animation on load — motion classes only under interaction states.
4. `npm run build` and `npm run typecheck` both exit 0 (the project's
   standing gate commands from sagan.yaml).
5. Semantics and access, verify-executable, one clause per brief check:
   the CTA is a real `<a>`/`<button>`, never a styled `div`; exactly one
   `h1` with heading order in sequence; visible focus on every
   interactive element and tab order follows reading order; images have
   alt text or are explicitly decorative; tap targets ≥ 44×44px; `axe`
   reports zero critical violations.
6. At 375px and 1440px: no horizontal overflow (standing render floor,
   added by the PM, confirmed at the gate).
7. Craft, judged by the fresh critic on verify's captures — any "no" is
   REVISE naming the item: (a) the accent-stripped capture still reads
   as premium; (b) nothing on the page exists to fill space; (c) the
   critic can state what Sagan does from the headline and subhead alone.

## Method

<!-- The per-ticket how — compiled by the PM from the brief's
     how-paragraph, with the AC, before dispatch. Only what varies per
     ticket: fan-out, fresh critic, verify, and caps are standing
     machinery in sagan.yaml and the role specs, never here. -->

- **items:** (1) structure + confirmed copy (AC 1), (2) the CTA
  (AC 1, 5), (3) token / accent / motion discipline (AC 3), (4) a11y
  pass (AC 5) — built and checked individually.
- **lane:** quality — craft judgment governs, round cap 3.
- **round-1 evidence:** 375px and 1440px captures in light and dark, an
  accent-stripped capture (for the "still reads premium" check),
  keyboard-focus capture, and the axe run — shipped with the first
  build so critique never waits.

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

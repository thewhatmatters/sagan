---
# ── tracker-owned (regenerated on every /sagan-start fetch; edit in Linear) ──
id: T-000
title: Marketing hero — headline, subcopy, CTA (shadcn primitives)
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

<!-- THIS is all the human wrote — the brief template (WHAT / HOW / DONE)
     filled in. Everything below this region was compiled BY the PM agent
     from this brief, same spine (WHAT stays here verbatim; HOW becomes
     ## Method plus mechanical AC; every DONE line becomes an AC item),
     and confirmed by the human at a gate before any work. -->

WHAT
Build the hero section for the sagan.run landing page.

It says: work ships only when independent checks prove it — agents build,
agents verify, you decide.

On the page: a headline (8 words or fewer) reading "Ship work you can
prove.", a subhead (20 or fewer) that names Sagan, a small "Now in public
beta" eyebrow, and a single call to action reading "Get started" that
goes to /docs. No secondary CTA.

HOW
Use only the shadcn primitives already installed: Button, Badge. Install
nothing new.

The look is calm and type-led: type carries the hierarchy — one family,
two weights at most, with size and spacing doing the work that color and
decoration usually do. Whitespace is the design element, not filler.

Specifically: no gradients, glows, meshes, or decorative backgrounds. One
accent color, used exactly once. Motion only in response to interaction —
nothing animates on load.

Voice: plain and confident; no hype words ("revolutionary", "blazing",
"magical"); every claim stated as a fact a reviewer could check.
Colors, spacing, and type come from the Tailwind theme tokens. No
hardcoded values.

DONE
It's done when all of these are true. Any single "no" means not done.

Craft
- Deleting the accent color entirely would still leave a page that reads
  as premium.
- Nothing on the page exists to fill space.
- A stranger can state what Sagan does after reading only the headline
  and subhead.

Brand
- Every color, spacing, and type value traces to a token.
- No component outside Button and Badge.
- No forbidden words or patterns from the voice rules.

Accessibility
- Every interactive element is the correct semantic tag — a button is a
  <button>, not a styled div.
- Heading order is sequential; the hero has exactly one h1.
- Focus is visible on every interactive element, and tab order follows
  reading order.
- Images have alt text, or are explicitly marked decorative.
- Tap targets are at least 44×44px.
- Any aria-* attribute is necessary and correct.

If something here can't be met, stop and say which item and why. Don't
ship a near-miss and mention it afterward.

<!-- sagan:linear-owned:end -->

<!-- sagan:repo-owned:start — agents write below; a fetch never touches this region -->
## AC

<!-- Compiled by the PM from the brief's DONE list + HOW constraints,
     confirmed by the human at the needs-you gate. Every clause judgeable
     from some role's declared input set; exact strings pinned; each item
     testable by command, observation, or a blind comparison — an
     adjective is never a criterion. Mechanical items route to verify;
     judgment items route to the fresh critic with verify's evidence.
     The brief's closing "stop and say which item" clause is the ESCALATE
     rule — a near-miss never ships quietly. -->

1. `src/components/marketing/hero.tsx` exports `Hero`, rendered at the
   top of `/`: `h1` exact text `Ship work you can prove.` (5 words) and
   the page's only `h1`; a subhead ≤ 20 words that names Sagan; a `Badge`
   eyebrow with exact text `Now in public beta`; exactly ONE CTA — a
   shadcn `Button` reading `Get started` linking to `/docs` — and no
   other CTA in the hero.
2. Only `Button` and `Badge` from `@/components/ui/` appear in the diff;
   no new dependencies; no components outside the installed list.
3. Tokens only: no arbitrary values (`[…]`) and no new hex colors in
   `git show`; the accent token appears exactly once in the hero; no
   animation on load — motion classes only under interaction states.
   Rendered copy contains none of the voice-rule forbidden words.
4. `npm run build` and `npm run typecheck` both exit 0.
5. Semantics and access, all verify-executable: the CTA is a real
   `<a>`/`<button>` (never a styled `div`); heading order sequential;
   visible focus on every interactive element with tab order = reading
   order; images have alt text or are marked decorative; tap targets
   ≥ 44×44px; `axe` reports zero critical violations (covers `aria-*`
   correctness).
6. At 375px and 1440px: no horizontal overflow.
7. Craft, judged by the fresh critic on verify's captures — any "no" is
   REVISE naming the item: (a) blind against linear.app's hero at
   1440px, the critic prefers ours on hierarchy and whitespace; (b) the
   accent-stripped capture still reads as premium; (c) nothing on the
   page exists to fill space; (d) the critic can state what Sagan does
   from the headline and subhead alone.

## Method

<!-- The per-ticket how — compiled by the PM from the brief's HOW, with
     the AC, before dispatch. Only what varies per ticket: fan-out, fresh
     critic, verify, and caps are standing machinery in sagan.yaml and
     the role specs, never here. -->

- **items:** (1) structure + pinned copy (AC 1), (2) the CTA (AC 1, 5),
  (3) token / motion / voice discipline (AC 3), (4) a11y pass (AC 5) —
  built and checked individually.
- **lane:** quality — the comparative bar governs, round cap 3.
- **round-1 evidence:** 375px and 1440px captures in light and dark, an
  accent-stripped capture (for DONE-Craft), keyboard-focus capture, the
  axe run, and a 1440px capture of the reference — shipped with the
  first build so critique never waits.
- **reference:** https://linear.app hero. Third-party captures stay out
  of the public repo — verify materializes them under
  `.sagan/ledger/<id>/` (gitignored evidence media).

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

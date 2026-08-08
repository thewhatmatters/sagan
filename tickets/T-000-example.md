---
# ── tracker-owned (regenerated on every /sagan-start fetch; edit in Linear) ──
id: T-000
title: Marketing hero — headline, subcopy, CTA pair (shadcn primitives)
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

<!-- THIS is all the human wrote, and it has the three parts every good
     brief has — WHAT (the task), HOW (approach + constraints), DONE (the
     bar) — like briefing a person. Everything below this region was
     drafted BY the PM agent from this brief, same spine (what stays here
     verbatim, how becomes ## Method, done becomes ## AC), and confirmed
     by the human at a gate before any work. -->

I want a landing-page hero that feels like linear.app's — calm, type-led,
confident. Headline "Ship work you can prove.", a small "public beta"
eyebrow, a short supporting line, and two buttons: get started, and view
on GitHub.

Build it from the shadcn primitives we already have — don't install
anything new.

It's done when a harsh reviewer, seeing ours and linear.app's side by
side without knowing which is which, prefers ours.

<!-- sagan:linear-owned:end -->

<!-- sagan:repo-owned:start — agents write below; a fetch never touches this region -->
## AC

<!-- The bar — compiled by the PM from the prose brief above, confirmed by
     the human at the needs-you gate. Rules learned the hard way: every
     clause judgeable from some role's declared input set (external docs
     ship in the critic's pack or route to verify as quoted attestations);
     exact strings pinned where wording matters; each item testable by
     command or observation; and an adjective is never a criterion —
     quality gets the comparative bar. -->

1. `src/components/marketing/hero.tsx` exports `Hero`, rendered at the top
   of `/`. It contains, in order: a `Badge` eyebrow with exact text
   `Now in public beta`, an `h1` with exact text `Ship work you can
   prove.`, one supporting paragraph (wording free, ≤ 160 characters, must
   name the product), and two CTAs.
2. CTAs use the existing shadcn `Button`: primary `Get started` linking to
   `/docs`; secondary `variant="outline"` `View on GitHub` linking to the
   repo URL from `package.json#repository`. No new dependencies, no custom
   button CSS — only primitives already under `@/components/ui/`.
3. Styling uses existing Tailwind tokens only: no arbitrary values
   (`[…]`) and no new hex colors anywhere in the diff (`git show` is the
   check). The `h1` uses the largest type step already present in the
   codebase; if none exists, `text-5xl md:text-7xl tracking-tight`.
4. `npm run build` and `npm run typecheck` both exit 0.
5. At 375px and 1440px: no horizontal overflow; both CTAs keep ≥ 44px
   touch-target height; body text ≥ 16px computed.
6. Keyboard: both CTAs reachable in DOM order with the project's visible
   focus ring; `axe` reports zero critical violations on `/`.
7. **Comparative bar:** the fresh critic views verify's 1440px captures of
   our hero and the reference blind, and must prefer ours on hierarchy and
   whitespace discipline — or return REVISE naming the axis that lost.

## Method

<!-- The per-ticket how — also drafted by the PM with the AC, before
     dispatch. Only what varies per ticket: fan-out, fresh critic, verify,
     and caps are standing machinery in sagan.yaml and the role specs,
     never here. -->

- **items:** (1) semantic structure + pinned copy (AC 1), (2) CTA pair
  wired to routes (AC 2), (3) token-clean responsive styling (AC 3, 5),
  (4) a11y pass (AC 6) — built and checked individually.
- **lane:** quality — the comparative bar governs, round cap 3.
- **round-1 evidence:** 375px and 1440px captures in light and dark,
  keyboard-focus capture, the axe run, and a 1440px capture of the
  reference — shipped with the first build so critique never waits.
- **reference:** https://linear.app hero. Third-party captures stay out of
  the public repo — verify materializes them under `.sagan/ledger/<id>/`
  (gitignored evidence media).

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

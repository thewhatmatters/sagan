# Retro — WHA-130 verify (verify-claude)

## What happened

Full protocol executed against fresh dist @ 1aca52d: build, size +
self-containment scan, section/image render check, 4-combo responsive
screenshots, reduced-motion emulation, no-JS render, a11y/contrast
audit. Overall PASS; aesthetics (AC3/AC4) and engraving-legibility
acceptability deferred to critic with factual measurements.

## Lessons for future verify runs

1. **Lazy images lie to naive render checks.** `loading="lazy"` images
   below the fold report `complete:false` at `networkidle` and render
   as blank boxes in `full_page` screenshots. First screenshot set had
   four blank evidence figures; looked like a broken build, wasn't.
   Fix: scroll through the page (use `mouse.wheel` — works in no-JS
   contexts too, unlike `window.scrollTo` via evaluate) and wait for
   networkidle before screenshotting or judging `img.complete`.
2. **Contrast must use the effective background.** body bg was
   rgb(211,212,207) (the "ground") but text sits on sheet surfaces
   rgb(248,245,230). Measuring vs body bg gave a false near-fail (4.14);
   walking ancestors for the first non-transparent background gave the
   honest 5.65/13.02. Always climb the ancestor chain.
3. **SVG text needs effective-size math.** Declared font-size inside a
   viewBox-scaled SVG is meaningless alone: effective px = declared ×
   (renderedWidth / viewBox width). This turned "13px sublabels" into
   9.2px effective at 1280 — the number the carried finding is actually
   about.
4. **Record inner-scroll behavior per element class.** At 375 the
   engraving fits (no scroll) but `pre.ledger` blocks scroll internally
   — page scrollWidth stays clean either way, so a page-level check
   alone would have hidden the distinction the critic needs.
5. `xmlns="http://www.w3.org/2000/svg"` and data-URI SVG filters false-
   positive on naive http:// grep scans — classify matches before
   declaring external requests.

## Open threads for critic

- Engraving soft annotations at 7.8–8.5px effective @1280 (target
  ≥ ~9.5px); min 4.1px @375. Improved from frame's 6.8px but short of
  the carried-finding number.

## Round 2 delta (SHA fee9144, delta_of 1aca52d)

Delta verify of the two revise fixes: PASS. Eager figures paint in
no-scroll full-page captures both schemes (the round-1 lazy-image trap
is gone — screenshots taken deliberately WITHOUT scroll-through to prove
it); engraving holds 504px fixed at 375 with a real inner scroll
(scrollLeft 0→120 verified, letterboxing gone) and sublabels clear the
carried target at 9.69px effective (504/728×14).

### Lessons added

6. **Delta verifies should invert the round-1 workaround.** Round 1
   needed scroll-through to defeat lazy loading; the round-2 fix claims
   eagerness, so the honest test is the exact capture flow that failed
   before (fresh page, screenshot immediately). Re-using the round-1
   script would have masked a regression.
7. **A viewBox change silently rescales every text.** 720→728 dropped
   scale 0.706→0.692: sublabels were nudged up past target, but the
   untouched 12px/11px annotations got marginally smaller (8.31/7.62
   effective). Recompute all text classes after any viewBox edit, not
   just the targeted one.
8. **git diff scopes the delta honestly.** Confirming the commit touched
   only the four img tags, .ev placeholder, SVG sizing/text, and
   .panel--scroll CSS is what justifies carrying AC2/AC5/AC6/AC7 instead
   of re-running them.

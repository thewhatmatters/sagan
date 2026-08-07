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

## Round 3 delta (SHA 9be4459, delta_of fee9144)

Delta verify of the structural rework (sticky topbar, merged
.sheet--doc, .foot-doc, five anchors): PASS. Sticky holds at midscroll;
all five anchors land exactly 72px below the bar without JS (56px bar at
1280, 40px at 375, scroll-margin-top 72px); 375 bar compresses to
numbers-only without overflow; round-2 fixes intact (four eager figures
paint with no scroll-through in dark, engraving 504×504); reduced motion
still zero animations.

### Lessons added

9. **`scroll-behavior: smooth` makes anchor checks time-dependent.** A
   400ms wait after fragment navigation measured targets 300–2200px
   short of landing and looked like a broken scroll-margin — it was the
   ~1.3s smooth-scroll animation mid-flight. Before ruling FAIL on any
   scroll-position assertion, sample position over time (stable page
   height + converging scrollY = animation, not bug), then measure at
   settle. Also: same-document goto (URL → URL#frag) doesn't reliably
   re-trigger fragment scroll in Playwright — use a fresh page per
   anchor, or click the link.
10. **Smooth scroll is itself a reduced-motion surface.**
    `getAnimations()` never counts it. Grep the built CSS: here
    `scroll-behavior:smooth` was correctly inside
    `@media (prefers-reduced-motion: no-preference)` — check for that
    guard explicitly whenever sticky-nav anchors appear.
11. **"X stays" contract language needs a per-breakpoint reading.** The
    grid chip is display:none at 375. Recorded as fact for the critic
    rather than ruled on — verify measures, the critic interprets
    contract intent.

### Open threads for critic

- Grid chip hidden at 375 vs pack's "the grid-toggle chip stays".
- Anchor navigation is animated (~1.3s) — acceptable polish or too slow?

## Round 4 delta (SHA f3ba049, delta_of 9be4459)

Delta verify of round 4b (canonical script, single-paper surface, paper-
native pinned nav, rebuilt hero, JSONL figure to section 04): PASS on
all nine protocol checks. Builder's contrast claims reproduced to the
hundredth (12.47/5.40/4.89 light, 14.42/6.74/5.76 dark). All five
anchors (incl. the #install alias span) land 88 ≥ bar 56 without JS.
Install chip select-all verified by actual click + getSelection —
returned the full npx command exactly, `$` prompt excluded via
user-select:none. Script sentences 3/3; "WHA-130"/"Receipts" zero hits.

### Lessons added

12. **Know which "soft" you're measuring.** The page has two soft-text
    mechanisms: the `--ink-soft` token (what the AC and builder claims
    mean — passes at 5.40/4.89) and an `.soft{opacity:.62}` class used
    only inside the engraving SVG, which blends to 4.04/3.87 in light.
    A naive `.soft` querySelector grabbed the wrong one first and
    initially returned full-ink numbers; verify the CSS rule behind a
    class before trusting its computed color, and compute opacity
    blends over the actual backdrop.
13. **`user-select: all` is verifiable, not just inspectable.** Click
    the element and read `window.getSelection().toString()` — this also
    catches the sibling `$` prompt correctly carrying
    `user-select:none` so copied text is exactly the runnable command.
14. **Anchor aliases need their own scroll-margin.** The zero-height
    `#install` alias span carries its own `scroll-margin-top` (88px) —
    measure the alias element itself, not its parent section.

### Open threads for critic

- SVG engraving `.soft` annotations at 4.04 (paper) / 3.87 (panel)
  effective contrast in light scheme — illustration-internal text in a
  `role=img` SVG with title+desc; below 4.5 if judged as page text.
- Grid chip still `display:none` at 375 (pack: "grid chip where it
  was").

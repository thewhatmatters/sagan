# Retro — WHA-130 · frontend

- **Went well:** the frame-as-contract model worked — palette, grid,
  sheet formula, and engraving transplanted into Astro with zero visual
  re-decisions; nearly all build time went into the three new sections
  and the responsive pass, not re-litigating the look.
- **Went well:** the carried critique findings were cheap to fix
  because they arrived as concrete numbers ("≥9.5px effective", "1px
  inset") — the border→inset-box-shadow swap was one line; keep writing
  findings with thresholds, not adjectives.
- **Fought me:** Astro treats `{}` in templates as expressions, so the
  real-JSONL specimen panels silently break without `is:raw`; worth a
  line in the frontend role spec for any Astro ticket that embeds code
  specimens.
- **Fought me:** enlarging engraving labels inside a fixed viewBox is
  geometry work — every widened label needed a hand width-check against
  the box edges, and the viewBox had to grow (`-36 0 720 720`). Next
  time the frame should size station labels for legibility from the
  start so the full build doesn't touch the drawing at all.
- **AC gap:** "no horizontal scroll at 375px" is ambiguous about
  scrollable *sub-containers* (the engraving panel scrolls internally
  at phone width). The AC should say whether inner `overflow-x: auto`
  regions are acceptable; I flagged it in the build note rather than
  choosing silently between two AC violations.
- **Role-spec suggestion:** the pack's "you may run `npm run build` —
  compile check, not render check" line is a good pattern; making
  static-check allowances explicit per-ticket avoided the T-001-era
  uncertainty about what a builder may verify.

## Round 2

- **Lesson (round 1's real bug):** `max-width:100%` on a fixed-attr
  SVG silently voids every size-derived claim — the 544px render I
  computed label sizes from never happened at 1280 (panel measure was
  509px). If a design claim depends on a rendered size, pin the size;
  don't let a fluid rule renegotiate it.
- **Went well:** verify's factual measurement (sublabels 9.2px @1280)
  reverse-engineered exactly to the container arithmetic (509/720 ×
  13 = 9.19) — numeric evidence made the root cause provable by hand,
  no render needed.
- **Went well (pattern):** `background-attachment:local` scroll
  shadows give an overflow-only scroll affordance with zero JS and no
  breakpoint math — it self-covers every band where the panel measure
  dips below the SVG width, not just 375.
- **Fought me (again):** enlarging labels in a fixed viewBox is
  geometry work — the 13→14 nudge pushed an end-anchored label past
  the box edge and forced a second viewBox widening (−36→−44). Same
  retro point as round 1, now proven twice: size engraving labels for
  legibility at the frame stage.

## Round 3

- **Lesson (why this round exists):** the extended-sheet formula
  (per-section void + sheet + footer) scaled the *hero's* drama to
  every section and read as slides. A hero frame approved in isolation
  doesn't license repeating its ground/paper rhythm — the frame stage
  should decide the document model (one paper vs many) before a full
  build, not leave it implied by the hero.
- **Went well:** the merge was almost pure structure — bands, clause
  system, figures, and all round-2 fixes moved into the single
  `.sheet--doc` untouched; the aesthetic/structure separation in the
  CSS (tokens + components vs page scaffolding) made "slides → one
  document" a scaffolding-only edit.
- **Conflict pattern worth naming:** "keep X exactly" + "only one Y on
  the page" collided (hero doc-foot vs single end footer). Resolved by
  scoping the global rule to the merged document and documenting the
  one-line fallback — packs should state which AC wins when a preserved
  artifact contains an instance of a thing being globally removed.
- **Pattern:** body-level `position:sticky` bar + `scroll-margin-top`
  on targets is a complete no-JS anchor-nav system; the only design
  decisions are bar height arithmetic (keep it on the 8px baseline)
  and a label-compression breakpoint (860px here, measured from mono
  advance widths, not eyeballed).
- **Ambiguity flag habit paid off again:** five structure decisions
  (hero footer, bar labels, dropped meta line, dropped eyebrows,
  doc-idx position marker) each got a documented rationale + cheap
  reversal path instead of a silent guess.

## Round 4b

- **Lesson (why 4a died and 4b worked):** copy, surface, and nav
  arrived as one pack with the script pre-approved verbatim — no
  copy negotiation mid-build. "Content is contract, layout is mine"
  is the cleanest division of labor this ticket has had; ask for
  approved copy before a full-page revise round, not during.
- **Pattern:** collapsing a two-surface system (ground/sheet) into
  one is mostly token deletion, but the *hierarchy debt* has to be
  repaid somewhere — here: opening whitespace, per-section rules +
  mono index lines, hairline-bordered panels, and a bigger pitch/
  closer size step. Name the replacement mechanisms explicitly
  before deleting the surface split, or the page goes flat.
- **Pattern (nav):** a "document-native" bar = same background as
  the page + its own copy of the page grain + one rule. The grain
  duplication matters — a solid-color sticky bar over a grained
  body reads as chrome the moment it pins.
- **Cheap win:** `user-select:all` on the install command gives
  click-to-copy affordance with zero JS — fits a no-JS contract
  page better than a clipboard button.
- **Verbatim-copy gotcha:** scripts written as prose lists ("Install
  — the command above…") don't map 1:1 onto name/description list
  markup; the em-dash split forces a case change on the description.
  Decide and flag it once, apply consistently.
- **Contrast discipline:** recomputing WCAG ratios took one python
  block and turned "retune ink tokens" from a vibe into arithmetic —
  the existing inks passed on #f3f0e2 (5.40 soft) and only the panel
  value needed choosing against the 4.5 floor (4.89). Always compute
  before swapping surface colors; the answer may be "keep the ink".

## Round 4c

- **Lesson (the actual bug):** descendant selectors on generic
  elements (`.doclist span`) are landmines in copy that nests inline
  spans — `display:block` reached two levels down and fragmented
  approved sentences. Structural list styling should always use
  child combinators (`>li>span`); reserve descendant scope for
  inheritable text properties only.
- **Gotcha (specificity ripple):** scoping one selector up (0-1-1 →
  0-1-2) silently breaks sibling overrides still written at the old
  specificity — `.doclist--split span{margin-top:0}` would have lost
  to the fix and re-broken the split alignment. When tightening a
  selector, grep for every other rule targeting the same element and
  re-check the cascade, not just the rule you're editing.
- **Cheap pattern:** "style like existing links" = extend the
  existing rule's selector list (`.body a` → `.body a,.doclist a`),
  not a new rule — one source of truth for the link look.

## Round 4d

- **Lesson (cut means sweep):** removing a section is three deletions,
  not one — markup + its assets (`public/` files ship even when
  unreferenced; Astro copies public/ wholesale) + its now-dead CSS.
  Grep class usage across .astro sources before deleting rules:
  `.c-7-13` looked 04-only but 02's figure uses it.
- **Gotcha (divider trick nets to zero):** the `div-l` gutter-divider
  used a −12px margin / +11px padding pair, so deleting the class
  restores the plain 24px gutter with no rebalancing needed — but its
  responsive overrides lived in two other media blocks; a divider is
  never one rule.
- **Verification cheap-trick:** `grep -c "real-run\|evidence/t-001"`
  against dist/index.html is a 1-second post-build contract check;
  beware false positives ("504" matches "04") — locate hits before
  trusting a nonzero count.

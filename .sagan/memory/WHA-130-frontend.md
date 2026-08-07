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

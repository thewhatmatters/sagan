# Retro — WHA-131 · frontend

- **Went well:** the moodboard's formula (mono index header → vast void →
  floating sheet → clauses → doc footer) translated almost 1:1; repeating
  it per section (01, 02) turned one reference image into a system. Real
  ledger JSONL as the code-specimen figure was a free win — the project's
  own artifacts are better texture than any invented copy.
- **Went well:** hand-computing the SVG engraving geometry (ring
  trig, arc endpoints with station gaps, tangent-angle chevrons) was
  slower than eyeballing but produced clean joins without render-checking
  — which the role boundary forbids anyway.
- **Fought me:** keeping hairline borders on the 8px baseline — every
  1px rule needs a compensated padding (7/11/15+1). Worth encoding as a
  reusable pattern in use-grid-system.
- **Fought me:** the sheet-vs-grid tension — a padded card breaks column
  alignment. Solution (sheet bleeds −48px past the type area so interior
  columns sit exactly on the page grid) is the note-worthy trick; the AC
  could name where the type area lives relative to the "paper".
- **AC gap:** CTA destinations (repo URL) and the intended default state
  of the "visible" grid overlay weren't specified — both flagged in the
  build note. Future design-frame ACs should state overlay-at-rest and
  link targets explicitly.
- **Role spec gap:** the frontend rubric's 375px clause contradicts a
  desktop-frame ticket; the pack overrode it, but the rubric should carry
  a "unless the ticket scopes viewport" escape hatch so critics don't
  ding frames for it.

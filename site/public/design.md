---
name: sagan-brand-guidelines
description: "Design, build, or extend an official Sagan-authored web surface. Use for the sagan.run site, documentation pages, reports, and any page that needs the Sagan mission-document look: one continuous paper, Geist typography on a strict baseline grid, thin-line engravings, hairline rules, and evidence-led restraint in light and dark."
---

# Design pages like Sagan

Act as a careful design engineer producing a mission document. Sagan is a standard for shipping work with AI agents where "done" has to be proven, not claimed. Its web surfaces borrow their authority from the artifacts of that tradition: the NASA press kit, the flight manual, the Voyager Golden Record cover. The page is not a marketing site that mentions evidence; it is itself a document — typeset, ruled, numbered, and engraved.

Make every artifact precise, calm, technical, and quietly confident. Authority comes from typography, alignment, and proof, never from decoration, color, or motion. If a page would still feel credible printed on paper and stapled into a flight binder, it is on brand.

## Use this priority order

When requirements compete, protect them in this order:

1. Preserve supplied facts, commands, verdict names, rule wording, and task constraints.
2. Preserve the host stack: Astro, static output, zero required client JavaScript, vendored fonts.
3. Keep the document metaphor intact — one continuous paper, numbered sections, hairline rules.
4. Hold the grid: 12 columns, 24px gutters, 72px margins, 1296px type area, 8px baseline.
5. Establish hierarchy through weight, scale, rules, and spacing before anything else.
6. Refine responsive behavior and progressive enhancement without weakening the document.

## Integrate with the project

The site lives in `site/` as a static Astro project: one page (`src/pages/index.astro`), one stylesheet (`src/styles/global.css`), fonts vendored in `public/fonts/` under the OFL. There is no client framework, no CSS tooling, and no runtime dependency. Keep it that way.

- All styling flows through `global.css` and its custom properties. Never inline a second token system or add a CSS framework.
- Pages must be fully functional with JavaScript disabled. Script is progressive enhancement only (the grid-overlay toggle is the model: `is:inline`, guarded, optional).
- Fonts are `Geist` 400/500/600 and `Geist Mono` 400, self-hosted as woff2 with `font-display: swap` and preloaded in the head. Do not add weights, faces, or a font CDN.
- Themes are implicit via `prefers-color-scheme` and `color-scheme: light dark`. Never add a visible theme switcher.

## One continuous paper

The ground IS the sheet. There is no void behind a floating card, no hero panel, no alternating section backgrounds. The entire page is a single surface — `--paper` — and the only elevation step is `--panel`, a slightly deeper tone with a hairline border, earned only by figures and specimen content.

- Light theme is warm archival paper: `--paper: #f3f0e2`, `--panel: #eae5d2`, ink `#23284a` (a deep blueprint blue-black), soft ink `#5d6076`.
- Dark theme is the instrument panel — the same single-surface logic at night: `--paper: #16171b`, `--panel: #23252c`, ink `#e9e7da`, soft ink `#a19f94`.
- A faint anisotropic paper grain (inline SVG turbulence, opacity .07 light / .10 dark) covers the full bleed, fixed, behind all content. Sticky surfaces that sit on the paper (the pinned index row) carry the same grain so they read as the same sheet.
- Hairlines come in two strengths: `--hair` (rgba ink at .26/.22) for internal division, `--hair-strong` (.45/.42) for section rules, the topbar rule, borders on controls.
- All ink-on-paper pairs are computed WCAG-checked: primary ink ≥ 11.3:1 on every surface in both themes; soft ink ≥ 4.9:1. Never introduce a text color below 4.5:1.

There is no accent color. Hierarchy is weight, scale, rules, and spacing — nothing else. The only chromatic values in the system are the grid-overlay diagnostics (red columns, teal baselines), which are instrumentation, not palette, and never appear in shipped content.

## Grid and alignment

One source of truth in `:root`: `--cols: 12`, `--gutter: 24px`, `--margin: 72px`, `--maxw: 1296px`, `--bl: 8px` baseline with body leading at exactly 3 baselines (24px). Every line-height in the system is a multiple of 8.

- Content sits in `.wrap`; grid bands are `.band` (a 12-column grid) with placement classes named by column line: `.c-1-5`, `.c-1-6`, `.c-1-7`, `.c-1-8`, `.c-5-13`, `.c-7-13`, `.c-1-13`. Beside a figure, text takes 5 columns (`.c-1-6`) with column 6 left empty as a spacer and the figure on 7–13.
- Prose columns hold 44–56ch max-width; wide evidence (figures, split lists) takes the right span or the full band.
- The layout is inspectable: the `G` key (desktop) toggles a drafting overlay showing columns, gutters, margins, and both baseline pitches. New work must survive that inspection — text baselines on the 24px rhythm, edges on column lines.
- Below 1100px, bands stack; the overlay and its toggle retire. Margins step 72 → 32 → 20px.

## Typography and rhythm

Geist Sans for everything readable; Geist Mono only for the document apparatus — section indices, navigation, captions, commands, verdicts, file paths, and figure annotations. Mono set small, uppercase, and letterspaced is the voice of the instrument label; sans set large and tight is the voice of the document title.

The type roles, exactly:

- **Display (h1):** 96/96, weight 600, tracking −.035em. Tablet 64/64, mobile 56/56. One per page.
- **Tagline:** 28/40, weight 400, tracking −.015em, max 19ch.
- **Pitch / lede:** 20/32, soft ink, max 46ch.
- **Section title (h2):** 44/48, weight 600, tracking −.02em. Tablet 36/40, mobile 30/32.
- **Body:** 16/24, regular; `strong` is weight 500 in full ink, used sparingly.
- **Section index (`.doc-idx`):** Mono 13/16, uppercase, tracking .14em, soft ink, above a strong hairline — the running head of each numbered section ("01 · Get started" left, "01 / 03" right).
- **Labels and nav:** Mono 11–13/16, uppercase, tracking .1–.22em (wider tracking for the brand mark).
- **Captions:** Mono 10/16, uppercase, tracking .08em, soft ink, set below figures like a plate caption.
- **Specimen text:** Mono 12/20, full ink, only inside panels (`pre`); annotations within a specimen dim to soft ink via `.soft`.

Sentence case for headings and rules; uppercase belongs to mono apparatus only. Numbered lists use the document idiom: mono two-digit counters ("01", "02") set small before a semibold term. Links underline with hairline-colored decoration and 3px offset — no color shift.

Spacing is relational and baseline-true: a heading and its lede are one unit (8px), a list following that unit steps clearly off it (32px), items within a list separated by hairlines with 20px padding, section turns large (128px desktop, 88/72 down the breakpoints), the footer preceded by the largest gap on the page (144px) and one closing rule.

## Rules, panels, and document furniture

- A section opens with a strong hairline rule spanning the band, then its mono index line. Sections are numbered and the count is shown ("02 / 03") — the document knows its own length.
- The pinned index row (`.topbar`) is the running header: brand mark left, numbered real section names right, one strong hairline below, paper backdrop with matching grain. Pure CSS sticky; functional without JavaScript.
- Panels (`.panel`) are the only boxed surface: `--panel` fill, `--hair` border, 8px radius, 24px padding. They hold figures and specimens, never ordinary prose. Horizontally overflowing panels (`.panel--scroll`) use edge-shadow scroll affordances that retire at the reached edge.
- Small interactive or labelled objects — CTAs, the command chip, verdict chips, the grid toggle — share one control grammar: mono type, 1px strong-hairline border, 2px radius. Hover fills with `--panel` or upgrades the border to full ink; nothing glows, lifts, or transitions color.
- Commands are presented in a chip with a non-selectable `$` prompt and a one-click-selects-all `code` payload.
- Verdict words (`APPROVED`, `REVISE`, `NEEDS_EVIDENCE`, `ESCALATE`) are typeset as small bordered mono chips inline in running text — instrument readouts, not badges.
- The composer specimen (`.composer`) depicts the human's chat brief as document furniture, never as a vendor screenshot: panel surface, sans prompt at body size, mono apparatus rows, and a bordered 2px-radius send chip. Monochrome, no icons, no product chrome; a `.fig-flow` mono line connects it to the artifact it compiles into.
- The footer is the same paper: one strong rule, one line of provenance text, mono links. The page ends; it does not fade out.

## Engravings

Diagrams are thin-line engravings in the manner of the Voyager Golden Record cover: single-weight strokes (0.4–1px), `currentColor` only, dashed and dotted auxiliaries, concentric-circle hubs, radial leader lines, binary tick marks, and small uppercase mono annotations set directly in the SVG.

- One color: `currentColor`, with opacity steps (roughly .28 / .42 / .6 / 1) as the only tonal range. No fills except pinpoint dots.
- Labels are Geist Mono, 11–14px, uppercase, tracked .06em; secondary labels drop to ~.62 opacity via a `.soft` class.
- Every engraving is semantic: `role="img"` with a real `<title>` and `<desc>`, presented in a panel as a figure with a head (title left, medium tag right) and a mono plate caption below.
- Engravings are drawn at fixed size and scroll inside their panel on small screens rather than shrinking their line work into illegibility.

## Motion

Default to stillness. The page is a document; documents do not animate. Permitted motion, all gated behind `prefers-reduced-motion: no-preference`: smooth anchor scrolling and the grid overlay's opacity fade. Nothing else — no scroll reveals, no hover transforms, no parallax, no typing cursors, no pulsing indicators.

## Reject these reflexes

Do not ship any of these recognizable defaults:

- An accent or brand color, gradient, glow, blob, glass effect, or colored CTA.
- A floating hero card, alternating section backgrounds, or any second surface besides `--panel`.
- Cards around prose, nested panels, or borders used to repair weak hierarchy.
- Shadows for depth (the only shadow-like marks are scroll affordances and overlay diagnostics).
- Icon sets, emoji, illustrations, stock imagery, or logos where an engraving or a word would do.
- Rounded-pill badges, eyebrow kickers in sans, or decorative section ornaments outside the mono index idiom.
- Arbitrary font sizes or line heights off the 8px baseline; numeric weights other than 400/500/600.
- A visible theme toggle, cookie bar, sticky CTA, or any chrome that outranks the content.
- Client-side JavaScript that content depends on; a framework for a static page.
- Centered hero copy over a card grid; marketing superlatives; exclamation points.

Restraint here is not minimalism for its own sake. The pages should feel dense with intent — ruled, numbered, annotated — like a document someone will be held to.

## Public CSS API

Structure and shell: `wrap`, `topbar`, `topbar-in`, `tb-brand`, `tb-right`, `tb-nav`, `tb-num`, `tb-label`, `tb-sep`, `hero`, `doc-sect`, `doc-idx`, `alias`, `foot`, `foot-line`, `foot-links`.

Grid: `band`, `c-1-5`, `c-1-6`, `c-1-7`, `c-1-8`, `c-5-13`, `c-7-13`, `c-1-13`, and the overlay set `guides`, `cols`, `col`, `rows`, `mline`.

Type and content: `tagline`, `pitch`, `body`, `mono`, `coda`, `verdict`, `chip`, `chip-p`, `ctas`, `cta`, `doclist` with modifiers `doclist--num` and `doclist--split`.

Figures: `fig-head` (with `t` title and `f` format tag), `panel`, `panel--scroll`, `engraving`, `soft`, `caption`, `fig-flow` (mono connector line between stacked figures), and the composer specimen set `composer`, `composer-meta`, `composer-prompt`, `composer-row`, `composer-k`, `composer-bar`, `composer-send` (`composer-row`/`composer-k` label a brief's three parts — what / how / done).

Tokens: `--paper`, `--panel`, `--ink`, `--ink-soft`, `--hair`, `--hair-strong`, `--grain-opacity`, `--grain-invert`, and the grid set `--cols`, `--bl`, `--lh`, `--gutter`, `--margin`, `--maxw`. Never invent a parallel token; new needs extend these in `global.css` with the same naming voice.

## Accessibility and responsive behavior

Meet WCAG AA everywhere; the palette is pre-computed to exceed it. Use landmarks, one `h1`, ordered headings, real `nav` with `aria-label`, `role="img"` with title and desc on every SVG figure, `aria-pressed` on toggles, and visible focus (`2px solid var(--ink)`, offset 2px). Selection inverts ink and paper.

Anchor targets clear the pinned row via `scroll-margin-top`. The page reflows 1296 → tablet → 375px by stacking bands and stepping the type scale; nothing truncates, nothing hides content, and wide specimens scroll locally inside their panel rather than breaking the sheet. Everything works with JavaScript off, in both themes, with no layout shift from font loading (woff2 preload + swap).

The target is a document that proves its claims — in its content and in its construction.

# Project memory — rolling synthesis

## From T-001 (2026-08-06) — first full loop: build → critique → evidence → approve

- **The loop worked as designed.** Round-1 critic returned NEEDS_EVIDENCE
  on render-dependent AC items instead of approving on a read; verify
  produced SHA-bound screenshots + a measured scrollWidth; round-2 critic
  approved on artifact + evidence with zero findings. APPROVED = verified
  held end to end.
- **AC ambiguities to fix at authoring time:** pin exact strings the
  footer/hero must carry (or explicitly permit paraphrase and local
  paths). Both workers independently flagged "footer naming the git repo
  path" — local path vs remote URL — as the ticket's only real ambiguity.
- **Critic isolation has an input-set edge:** an AC clause referencing a
  file outside the artifact ("true to AGENTS.md") is unjudgeable under
  artifact-only isolation. Resolution that worked: verify attests with
  quoted passages; critic relies on the attestation in round 2. Rule of
  thumb — if the AC references a source document, either include it in
  the critic's input set or route the clause to verify.
- **Role-spec gap:** frontend spec should state explicitly that builders
  do not render-check their own work (the builder assumed correctly, but
  it was an assumption).
- **Verify practicals:** full-page screenshots satisfy "show all
  sections" in one capture; save evidence under
  `.sagan/ledger/<ticket>/` so images sit next to their events.jsonl
  line; record grep counts and exit codes separately (grep -c exits 1 on
  zero matches).
- **Contract drift to watch:** round-2 critic added a `notes` field not
  in the role spec's JSON contract. Harmless here; a runtime with schema
  validation would have rejected it — the spec and the validator need to
  agree on the envelope.

## From the second run's staging (sagan.run site, 2026-08-06) — captured for the sagan PM skill

- **Dispatch access check (PM checklist item):** every pointer in a
  context pack must resolve *for the worker receiving it*. Inaccessible
  sources (JS-walled pages, auth-gated tracker attachments) get
  materialized into local artifacts before dispatch; the PM's written
  read supplements the original, never substitutes for it (the
  anti-paraphrase rule). Case: an art-direction moodboard on a JS-walled
  site — the image was materialized from the ticket attachment to a
  gitignored local path, with a structural read logged on the ticket;
  workers receive both.
- **Third-party reference imagery never gets committed to a public
  repo** — it lives on the ticket and in a transient gitignored path.
- **Linear MCP quirk (when Linear is the ticket store):** save_issue
  silently ignores a nonexistent project name — no error, no
  auto-create. Create the project first, then attach; and verify the
  response echoes `project` before claiming it. (Claim-vs-evidence
  applies to the PM's own tool calls.)
- **AC amendments are dated Decisions entries plus an edited AC block**
  (marked "Amended — see Decisions") — never a silent edit, never a
  Decisions-only note that leaves the AC stale. Case: amending the site
  ticket's AC to permit a build-time framework while keeping runtime
  constraints.
- **Startup sequence to codify in the skill:** read sagan.yaml → fetch
  ticket → check AC exists / blockers / gates → surface open decisions as
  structured questions → log run start to ledger → dispatch with pointer
  packs.
- **Memory hygiene in a public reference repo:** entries here are read
  by adopters, not just this fleet — cite in-repo artifacts (T-001) or
  write cases self-describing; private tracker IDs stay in the private
  tracker.

## From the sagan.run site run (2026-08-06) — wrap-up synthesis

Shipped: sagan.run (Astro, 248KB, zero third-party requests) through the
full loop — 2 tickets + deploy, ~16 agents, 5 build rounds, 2 human gate
rejections, 1 persona-test debut. Consolidated lessons for the PM skill:

- **Copy is a gated artifact.** The decisive quality jump came when the
  human approved a README-style content script BEFORE layout; builders
  lay approved words, they don't write them. Mandate script-first for
  any communication-bearing page.
- **A frame gate approves a frame, not a rhythm.** Showcase site runs
  need a structure/scroll-rhythm artifact gated alongside the visual
  frame — extending one approved sheet five times produced "slides".
- **Persona-test before human gates on user-facing work.** Its debut
  produced two approved copy amendments and caught a checklist hole;
  its trust-read predicted the human's reaction imperfectly (proof
  section) — the gate outranks it, but it belongs in the standing
  pipeline.
- **Ship predictable evidence with round 1** (overlay-on renders,
  no-scroll figure captures) — saved a full critique round when applied.
- **Verify deltas must re-execute what CSS-token changes could break**
  (the carried 375-scroll claim went stale); "diff-confined" reasoning
  needs a runtime-surface map, not a file list.
- **Critic contract drift is chronic** (3× `notes` field) — sync repo
  role specs from the wire-sagan template; schema enforcement will kill
  this class.
- **PM-direct execution is legitimate for credentialed infra** (authed
  Vercel account exceeds agent containment) — log builder_id pm-direct
  with rationale; verify stays separate.
- **Public-page hygiene = memory hygiene**: no private tracker IDs in
  shipped copy (footer leak caught by the human gate).
- **Same-finding circuit breaker never tripped** across 5 rounds — every
  round's findings were new, which is what healthy iteration looks like
  in the ledger.

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

## From WHA-130/131 staging (2026-08-06) — captured for the sagan PM skill

- **Dispatch access check (PM checklist item):** every pointer in a
  context pack must resolve *for the worker receiving it*. Inaccessible
  sources (JS-walled pages like cosmos.so, auth-gated Linear attachments)
  get materialized into local artifacts before dispatch; the PM's written
  read supplements the original, never substitutes for it (v3.2
  anti-paraphrase rule). Case: WHA-131 moodboard — image pulled from the
  Linear attachment to a gitignored local path + a structural read logged
  on the ticket; workers receive both.
- **Third-party reference imagery never gets committed to a public
  repo** — it lives on the ticket and in a transient gitignored path.
- **Linear MCP quirk:** save_issue silently ignores a nonexistent
  project name — no error, no auto-create. Create the project first,
  then attach; and verify the response echoes `project` before claiming
  it. (Claim-vs-evidence applies to the PM's own tool calls.)
- **AC amendments are dated Decisions entries plus an edited AC block**
  (marked "Amended — see Decisions") — never a silent edit, never a
  Decisions-only note that leaves the AC stale. Case: WHA-130 Astro
  amendment.
- **Startup sequence to codify in the skill:** read sagan.yaml → fetch
  ticket → check AC exists / blockers / gates → surface open decisions as
  structured questions → log run start to ledger → dispatch with pointer
  packs.

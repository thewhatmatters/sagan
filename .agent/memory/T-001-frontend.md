# T-001 frontend retro

- Went well: AC was concrete and testable-by-reading (file path, exact
  status-line string, landmark list, scheme support) — no back-and-forth
  needed; AGENTS.md gave ready-made truthful card copy.
- Went well: "no interactive elements is acceptable" clause in AC 6
  removed a whole class of guesswork (no fake nav/buttons added to
  satisfy a focus rule).
- Fought me: AC 2 "a footer naming the git repo path" is ambiguous —
  local absolute path vs. remote URL. No remote was in the context pack,
  so I used the local path and flagged it in the build note.
- Fought me: "one-line value statement" has no canonical source; AGENTS.md
  is a purpose doc, not marketing copy, so the hero line is a paraphrase
  the critic may dispute.
- Next time the AC should: pin the exact footer string (or say "repo
  root path as known to the builder") and either supply the hero tagline
  or state that paraphrase from AGENTS.md is acceptable.
- Next time the role spec could: state whether the builder may run a
  local render check (screenshot tooling exists) or whether all
  verification is strictly verify's job — I assumed strictly verify's.

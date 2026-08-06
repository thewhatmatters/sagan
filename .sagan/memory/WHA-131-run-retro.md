# WHA-131 run retro (PM notes — revisit at wrap-up)

## Roster + cost
| Agent | Duration | Tokens | Tools |
|---|---|---|---|
| frontend builder | 21.4 min | 113.8k | 24 |
| critic round 1 (fresh) | 2.5 min | 73.1k | 11 |
| critic round 2 (fresh) | 1.4 min | 69.4k | 11 |
| PM renders (not an agent) | ~1 min | — | — |

3 agents (2 predicted — the NEEDS_EVIDENCE round added one). Wall clock
dispatch→gate ≈ 35 min incl. renders + verdict handling. Round trip:
build → render → NEEDS_EVIDENCE → overlay evidence → APPROVED → Randy
approve. Zero blocking findings at gate.

## Refinements for the sagan skill (and next runs)
1. **Predictable evidence should ship with round 1.** The critic's
   NEEDS_EVIDENCE (grid-overlay-on render) was foreseeable for any
   use-grid-system artifact. PM render protocol should include
   overlay-on captures by default → saves a round and ~70k tokens.
2. **Critic contract drift recurred** (a `notes` field outside the JSON
   contract, second occurrence). The repo's .sagan/roles/critic.md
   predates the template fix that added "emit ONLY contract fields" —
   sync repo roles from the wire-sagan template (--update path exists).
3. **Pack must carry real link targets.** CTA hrefs came back as
   placeholders because the pack's content sources named the repo but
   not its URL. Access-check rule extends to URLs: resolve them into
   the pack, don't make builders invent anchors.
4. **PM-as-renderer is improvised, not specced.** Builders can't
   render-check their own work; for design artifacts the PM rendered.
   Codify in the sagan skill: who renders what, and that PM renders are
   pack-grade evidence (they fed both critique rounds).
5. **Carry-forward findings need a home.** Four low findings ride to
   WHA-130 (wire CTAs; bump engraving sublabels ≥9.5px effective; 1px
   dark border inset noted; dark-sheet taste call accepted by Randy).
   The skill should define the mechanism: approved-artifact findings
   auto-append to the successor ticket's pack.
6. **Builder runtime is the long pole** (21 min of 35). Fine for
   showcase tier; worth a progress-event convention (lane heartbeats)
   when Conan's surface exists.

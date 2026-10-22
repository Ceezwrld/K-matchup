# Second-reader handoff — Opus 5.5

Use this in a **new chat** (Claude Opus 5.5). This model is a **second reader + G1 operator**, not a rewrite of the Python board.

Repo: `Ceezwrld/K-matchup` · branch `cursor/alcs-g6-grade-g7-fe0c` · tools under `mlb-k-matchups/`.

---

## Paste this as the first message

Attach the @ files listed at the bottom, then paste:

---

You are the second reader and World Series G1 operator for this MLB K / Hits process.

**Job**
1. Honor every lock in `@backtest-lessons.md` (through ALCS G6). Do not re-learn them.
2. Do **not** retune `expected_ks`, HOT/COLD xwOBA thresholds, dump-fit tags, or hits scores.
3. Dump-fit (`TUNNEL` / `MISTAKE` / `CHASE` / `TAKE` / `OFFER` / `COLD`) and L/R pitch plans are **display-only**.
4. Pitch×zone “see it” (SEES / SITS / FOGS / CHASES / WEAK) stays **paper-only**. Do not code it.
5. Live player odds are a **question**, not a fire. Do not join batter props into scores.
6. When a card exists, second-read it before lock. When G1 OFF nines + both probables post, build the G1 card with `k_matchups.py --require-official-lineup` and `zone_overlap.py --images` on both SPs.

**How to read maps (the G6 Aranda miss)**
- Dump is vs **that batter’s hand**, not the other stand. Aranda is LHB; Armstrong’s real dump vs LHB was OUT-UP-3B FF (Aranda COLD). The card used the RHB ST dump (OUT-DN-1B 28%) on a lefty. HOT OUT-DN-1B vs LHB was only ~11% — secondary, not BEST.
- G4 Aranda 3-4 was a **full-box** night (first hit top 3 vs Griffin after a 1-IP opener), not a rematch of the Armstrong dump PA. Do not copy a smash box onto the wrong arm.
- SEASON_ONLY + 0 recent BIP + opener (~1 PA) = lottery, never 1★ / never 2-man A-leg.
- Opener dump-HOT ≠ 2-man A-ticket. Tiny O0.5 vs **that arm only**; after exit the dump lean is incomplete unless bulk shares the tunnel. Full-game 2-man anchor = CONFIRM / multi (Yandy-type).

**Process locks (do not re-learn)**
1. 2-man: ≥1 leg CONFIRM. SEASON_ONLY = singles / secondary, not A-ticket anchors.
2. O1.5 / 2+ Hits ≠ O0.5 — need Yandy-type multi.
3. Same-bat 2+ Hits + 3+ HRR is correlated, not identical (1-hit HR can cash HRR and miss 2+).
4. UNDER_OK + Stuff+≥105 / WHIFF → no chalk soft under.
5. Opener / SP ≤~2 IP → vs-SP incomplete; primary bulk = first long arm after opener.
6. Opener dump-HOT ≠ 2-man A-ticket.
7. Caminero-types COLD on RHP dump → pass vs that arm; fire vs LHP bulk (Gasser/Drohan).
8. Kwan-types: fade HRR/power, not O0.5 Hits.
9. Palacios-types: pass hard fade (need soft board + COLD dump + no recent multi).
10. Bailey-type WARM-mid CONFIRM without elite board → tiny / secondary, not a 2-man leg.
11. BEST = HOT on the pitcher’s **real dump vs that hand** or elite board + ≥3–4 HOTs (note if dump is COLD).
12. Fat `k_edge` is a question, not a ticket.

**Second-reader checklist (run on every locked card before fire)**
- [ ] Dump used is vs this batter’s stand (L vs R pitch-plan, not the other hand).
- [ ] If HOT is not the #1 throw pocket vs that hand, it is not BEST (secondary pocket).
- [ ] SEASON_ONLY / LOW_SAMPLE_RECENT / CONFLICT sized tiny — not 1★, not 2-man A.
- [ ] Opener / short SP: 1★ is not a dump lottery; 2-man A is a full-game CONFIRM/multi bat.
- [ ] Rematch “smash” was actually vs that arm (vs-SP), not the full box vs the bulk/pen.
- [ ] O0.5 vs O1.5 vs 3+ HRR are separate tickets.
- [ ] K lane separate from Hits. SPIKE / Stuff+≥105 blocks chalk soft under.
- [ ] Fades: Kwan = power not Hits; Palacios = pass hard fade unless all three fade gates.
- [ ] What would you **size down or kill**? List that first, then what you’d keep.

**World Series state (as of 2026-10-22)**
- Series: TB vs MIL. Preview only: `@pregame-world-series-2026-tb-mil.md`. Not a ticket lock.
- G1: Fri 10/23 7:00 CT · TB @ MIL · `pk=849805`.
- MIL probable: **Jacob Misiorowski**. TB probable: **TBD**. G2 both TBD.
- Base case was Misi vs Rasmussen/Jax. If TB names Peralta G1, STRONG K (Exp 5.51 vs MIL) moves up; Trop G3 re-slots.
- No G1 OFF card until **both** probables + official nines.
- Peralta vs MIL = STRONG O4.5 floor, not O6.5 (BAL). Misi = SPIKE Stuff+128, never soft U6. Rasmussen = SOFT + Stuff+110 WHIFF, no chalk under. Bauers = MIL #1 Hits vs TB RHP. Frelick = fade.

**First action in this chat**
1. Confirm you ingested the locks (do not rewrite them).
2. Check G1 schedule/probables. If TB still TBD, **wait** — do not lock tickets on prior nines.
3. When both SPs + OFF lineups post: refresh board + zone overlaps (4-panel: throws / swing / damage / overlap + dump-fit) → draft card → **run the second-reader checklist on your own draft** → then lock.
4. If I paste a card, only second-read it. Size-downs first. No code unless I ask.

---

## Files to @ in the new chat

`@HANDOFF-second-reader.md`
`@HANDOFF-alcs.md`
`@backtest-lessons.md`
`@pregame-world-series-2026-tb-mil.md`
`@backtest-2026-10-19-alcs-g6.md`
`@pregame-batter-leans-2026-10-19-alcs-g6-off.md`
`@zone-overlap-freddy-peralta-2026-10-19.md`
`@zone-overlap-shawn-armstrong-2026-10-19.md`
`@mlb-k-matchups/README.md`

Optional if it is building G1: `@rankings-2026-ws-preview.csv` `@hits-2026-ws-preview.csv`

## Cursor setup

1. New chat · model **Claude Opus 5.5** · same repo/branch.
2. @ the files above.
3. Paste the block.
4. Do not ask it to retune HOT or Exp K. Do not ask it to implement see-it yet.

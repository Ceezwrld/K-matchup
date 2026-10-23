# Handoff — MLB K-matchup / World Series

**Branch:** `cursor/alcs-g6-grade-g7-fe0c`  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md`. World Series **G1 is OFF**: `@pregame-batter-leans-2026-10-23-ws-g1.md`. Martinez vs Misiorowski, official nines. Next: live if Misi hooks ≤2 IP; then G2 Sat 10/24. Tools under `mlb-k-matchups/`.

## Done
- ALCS G3–G6 graded; series TB **4–2**
- Order-walk expected hits / RBI traffic
- **WS G1 OFF** locked (2026-10-23): Martinez vs Misiorowski, official nines

## Process locks (do not re-learn)
1. 2-man: ≥1 leg **CONFIRM** (SEASON_ONLY = singles only)
2. O1.5 / 2+ Hits ≠ O0.5 — Yandy-type multi; `p_ge_2` sizes this
3. Same-bat 2+ Hits + 3+ HRR = correlated nuke
4. UNDER_OK + Stuff+≥105 / WHIFF → no chalk soft under
5. Opener / SP ≤~2 IP → vs-SP incomplete; identify **primary bulk**
6. Opener dump-HOT ≠ 2-man A-ticket
7. Caminero-types COLD on RHP dump → pass vs that arm; **fire vs LHP**
8. Kwan-types: fade HRR/power, not O0.5 Hits
9. Palacios-types: **pass hard fade**
10. Bailey-type WARM-mid CONFIRM without elite board → tiny
11. **Dump vs that batter’s hand**
12. **expected_hits / rbi_spot size, dump-fit gates**

## G1 OFF snapshot
- **Misiorowski** Exp **4.37 SPIKE** · lineup Exp H **3.79** · never soft U6
- **Martinez** Exp **4.20 FILLER** · lineup Exp H **4.17** · pass K · MIL Hits/HRR
- TB: Simpson to 3 (Hits O0.5, fade HRR) · Hicks to 5 · Palacios out · Williamson in (pass)
- MIL: Bauers to 2 · Yelich to 3 · Contreras cleanup · Turang to 5
- Fire: Bauers Hits · Contreras Hits/HRR · Yandy Hits · Yelich Hits/HRR · Simpson Hits
- Pass: Caminero vs Misi · Aranda 1★ · Frelick · Williamson · 2+ Hits

## Open / next
1. Live re-lean if Misi hooks ≤2 IP
2. Grade G1 after final
3. G2 Sat 10/24 both TBD

## Files to @
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@pregame-batter-leans-2026-10-23-ws-g1.md` `@zone-overlap-jacob-misiorowski-2026-10-23.md` `@zone-overlap-nick-martinez-2026-10-23.md` `@mlb-k-matchups/README.md`

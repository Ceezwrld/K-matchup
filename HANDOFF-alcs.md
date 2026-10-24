# Handoff — MLB K-matchup / World Series

**Branch:** `cursor/ws-g1-grade-fe0c`  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md`. World Series **G1 graded**: `@backtest-2026-10-23-ws-g1.md`. G2 Sat 10/24 **Rasmussen vs Henderson** — wait for official nines. Tools under `mlb-k-matchups/`.

## Done
- ALCS G3–G6 graded; series TB **4–2**
- Order-walk expected hits / RBI traffic
- **WS G1 OFF** locked + **graded** (MIL 3–2): `@backtest-2026-10-23-ws-g1.md`

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
13. **Kalshi last-leg combo:** 4/5 in + 1 PA vs closer → cash ≥ ~$15. G1 $21 vs Yandy/Megill ($0 if ride).
14. **One anchor bat on one 2-man only** (G1 Bauers: A HIT, B died on Yandy).

## G1 grade (MIL 3, TB 2)
- Solos: Bauers / Contreras / Yelich / Simpson **HIT** · Yandy **MISS** (0-4)
- 2-man: **A** Bauers+Contreras HIT · **B** Yandy+Contreras MISS · **C** Contreras+Yelich HRR HIT
- Kalshi 5-leg cashed at **$21** (Yandy would have zeroed $97.94)
- Aranda 3-3 left on table (tiny, COLD dump) — do not flip 1★ gate
- Misi 3 K — SPIKE veto stands even though unders cashed

## Open / next
1. G2 Sat 10/24 7:00 CT · **Rasmussen vs Henderson** · wait official nines
2. Do not lock a G2 card on projected lineups

## Files to @
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@backtest-2026-10-23-ws-g1.md` `@pregame-batter-leans-2026-10-23-ws-g1.md` `@mlb-k-matchups/README.md`

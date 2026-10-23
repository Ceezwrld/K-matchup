# Handoff — MLB K-matchup / World Series

**Branch:** `cursor/alcs-g6-grade-g7-fe0c`  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md` (incl. ALCS G6 + expected-hits/RBI traffic). World Series **G1 EARLY** is up: `@pregame-batter-leans-2026-10-23-ws-g1.md`. Martinez vs Misiorowski, **PRIOR nines**. First: when official lineups post, refresh `--require-official-lineup` + re-map both SPs and lock the OFF card. Tools under `mlb-k-matchups/`.

## Done
- ALCS G3–G6 graded; series TB **4–2**
- WS preview + dump-fit layer
- **WS G1 EARLY** scored (2026-10-23): Martinez vs Misiorowski
- Order-walk **expected hits / RBI traffic** (display-only)

## Process locks (do not re-learn)
1. 2-man: ≥1 leg **CONFIRM** (SEASON_ONLY = singles only)
2. O1.5 / 2+ Hits ≠ O0.5 — Yandy-type multi; `p_ge_2` now sizes this
3. Same-bat 2+ Hits + 3+ HRR = correlated nuke
4. UNDER_OK + Stuff+≥105 / WHIFF → no chalk soft under
5. Opener / SP ≤~2 IP → vs-SP incomplete; identify **primary bulk**
6. Opener dump-HOT ≠ 2-man A-ticket
7. Caminero-types COLD on RHP dump → pass vs that arm; **fire vs LHP**
8. Kwan-types: fade HRR/power, not O0.5 Hits
9. Palacios-types: **pass hard fade**
10. Bailey-type WARM-mid CONFIRM without elite board → tiny
11. **Dump vs that batter’s hand** — do not put a LHB on the RHB dump (G6 Aranda)
12. **expected_hits / rbi_spot size, dump-fit gates** — volume does not clear a COLD dump

## G1 EARLY snapshot (PRIOR nines — not OFF)
- **Misiorowski** Exp **4.38 SPIKE** WHIFF · lineup Exp H **3.73** · never soft U6
- **Martinez** Exp **4.20 UNDER_OK** FLY · lineup Exp H **4.21** · pass juiced K · MIL Hits/HRR
- **Yandy Hits O0.5** — 3 PA, P1 44%, RBI thin, not 2+
- **Caminero PASS** — CONFIRM COLD + 2 PA / P1 32%
- **Bauers Hits + HRR** — CONFIRM + 3 PA + prime RBI
- **Turang Hits** — volume P1 51%
- **Contreras Hits/HRR** — prime RBI, dump CONFLICT (not 1★)
- **Mitchell** CONFIRM 2-man A, not volume
- **Frelick FADE** · Palacios pass-fade

## Open / next
1. **G1 OFF lock** when official nines post (re-walk expected hits with new slots)
2. If Misi hooks ≤2 IP → re-lean Caminero/Yandy vs first long arm
3. G2 Sat 10/24 both TBD

## Files to @
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@pregame-batter-leans-2026-10-23-ws-g1.md` `@pregame-world-series-2026-tb-mil.md` `@zone-overlap-jacob-misiorowski-2026-10-23.md` `@zone-overlap-nick-martinez-2026-10-23.md` `@mlb-k-matchups/README.md`

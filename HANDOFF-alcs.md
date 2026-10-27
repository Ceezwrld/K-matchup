# Handoff — MLB K-matchup / World Series

**Branch:** `cursor/ws-g4-early-fe0c`  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md`. World Series **G4 is EARLY**: `@pregame-batter-leans-2026-10-27-ws-g4-early.md`. Jax (R) confirmed vs MIL unnamed (Drohan L leftover). MIL leads 3–0. Next: lock when MIL names the arm and both nines post. Tools under `mlb-k-matchups/`.

## Done
- ALCS G3–G6 graded; series TB **4–2**
- Order-walk expected hits / RBI traffic
- **WS G1** locked + graded (MIL 3–2): `@backtest-2026-10-23-ws-g1.md`
- **WS G2** locked + graded (MIL 5–4): `@backtest-2026-10-24-ws-g2.md`
- **WS G3** locked + graded (MIL 10–1): `@backtest-2026-10-26-ws-g3.md`
- **WS G4 EARLY** (2026-10-27): Jax vs Drohan-leftover on G3 prior nines. `@pregame-batter-leans-2026-10-27-ws-g4-early.md`

## Process locks (do not re-learn)
1. 2-man: ≥1 leg **CONFIRM** (SEASON_ONLY = singles only)
2. O1.5 / 2+ Hits ≠ O0.5 — Yandy-type multi; `p_ge_2` sizes this
3. Same-bat 2+ Hits + 3+ HRR = correlated nuke
4. UNDER_OK + Stuff+≥105 / WHIFF → no chalk soft under
5. Opener / SP ≤~2 IP → vs-SP incomplete; identify **primary bulk**
6. Opener dump-HOT ≠ 2-man A-ticket
7. Caminero-types COLD on RHP dump → pass vs that arm; **fire vs LHP** (G3 0-fer does not unlearn)
8. Kwan-types: fade HRR/power, not O0.5 Hits
9. Palacios-types: **pass hard fade**
10. Bailey-type WARM-mid CONFIRM without elite board → tiny
11. **Dump vs that batter’s hand**
12. **expected_hits / rbi_spot size, dump-fit gates**
13. **Kalshi last-leg combo:** 4/5 in + 1 PA vs closer → cash ≥ ~$15. G1 $21 vs Yandy/Megill ($0 if ride).
14. **One anchor bat on one 2-man only** (G1/G2 Bauers A HIT / Yandy B MISS; G3 Caminero A MISS / Yandy B HIT).
15. **O0.5 ≠ 2+** — G2 Yelich/Yandy both HRR 1. Process 0.5 HIT; user 2+ MISS.
16. **SP hook ~3–4.2 IP** → later box is vs bulk. Grade vs-SP separate from the full box.
17. **ML slight leans are not process locks.** G3 TB ML died on Gasser’s 1-hitter.

## G4 EARLY snapshot
- **Jax** Exp **4.28 AVG** · STYLE **WHIFF** · stuff **elite / SPIKE** · **4.3 IP / 18 BF** · MIL Exp H **3.19**. Last start ALCS G3 **2 K / 4.0**. No O5.5+ · no U4.5. MIL Hits are 2-PA vs him, then a fried TB pen.
- **Drohan** Exp **4.10 SOFT BAL** · model 5.4 IP / 23 BF · **NLCS G4 was 1.0 IP**. 1/2 UNDER_OK. Pass juiced K. TB Hits vs L only if he lasts.
- MIL vs Jax: almost all **MISTAKE**. **Contreras** is the engine (WS HRR 3/3/5). Frelick **COLD**. Pratt only TUNNEL (7-hole tiny).
- TB vs Drohan: **Caminero TUNNEL 1★** if he starts. Yandy TUNNEL Hits not 1★. Vilade TUNNEL not 1★ (G3 0-2). Mesa 7-hole MISTAKE tiny.
- **Win lean: Milwaukee** (clincher, fresh pen, Jax length into a wrecked TB pen). Not a hammer.
- **Do not lock** until MIL names the arm + official nines.

## Open / next
1. **G4 OFF lock** when MIL probable + both nines post. If not Drohan, throw out the LHP TB card (Aranda/Hicks likely back).
2. If Drohan hooks ≤2 IP, void vs-SP; re-lean May / Hall / Romero.
3. Keep Caminero vs LHP if Drohan/Gasser-shape lasts. Do not pass from the G3 0-fer.

## Files to @
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@pregame-batter-leans-2026-10-27-ws-g4-early.md` `@backtest-2026-10-26-ws-g3.md` `@zone-overlap-griffin-jax-2026-10-27.md` `@zone-overlap-shane-drohan-2026-10-27.md` `@mlb-k-matchups/README.md`

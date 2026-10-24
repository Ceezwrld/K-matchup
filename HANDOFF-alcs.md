# Handoff — MLB K-matchup / World Series

**Branch:** `cursor/ws-g2-card-fe0c`  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md`. World Series **G2 is OFF**: `@pregame-batter-leans-2026-10-24-ws-g2.md`. Rasmussen vs Henderson, official nines. Next: live if Henderson hooks ≤2 IP; then G3 Mon 10/26. Tools under `mlb-k-matchups/`.

## Done
- ALCS G3–G6 graded; series TB **4–2**
- Order-walk expected hits / RBI traffic
- **WS G1** locked + graded (MIL 3–2): `@backtest-2026-10-23-ws-g1.md`
- **WS G2 OFF** locked (2026-10-24): Rasmussen vs Henderson, official nines

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

## G2 OFF snapshot
- **Rasmussen** Exp **4.66** · Stuff+ **110 WHIFF** · lineup Exp H **3.95** · pass juiced K · no chalk under · MIL Hits O0.5
- **Henderson** Exp **4.04 SPIKE** · lineup Exp H **3.99** · pass K · TB Hits
- TB: Palacios back 6 (pass) · Williamson out · Mesa to 8 · Aranda 1★ (Henderson dump is MISTAKE, not G1 COLD) · Simpson COLD dump (tiny) · Caminero pass (CONFIRM COLD)
- MIL: same 2–3–4 · Bauers Hits 1★ · Contreras Hits/HRR · Yelich Hits/HRR GOOD
- Fire: Aranda Hits · Bauers Hits · Contreras Hits/HRR · Yandy Hits · Yelich Hits/HRR
- 2-man: Bauers+Contreras · Yandy+Contreras (no second Bauers/Aranda pair)
- Pass: Caminero vs Henderson · Palacios · Simpson lock · Frelick · Henderson K under · Ras chalk under

## Open / next
1. Live re-lean if Henderson hooks ≤2 IP
2. Grade G2 after final
3. G3 Mon 10/26 at Trop — likely Peralta vs Gasser (LHP Caminero window)

## Files to @
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@pregame-batter-leans-2026-10-24-ws-g2.md` `@backtest-2026-10-23-ws-g1.md` `@zone-overlap-drew-rasmussen-2026-10-24.md` `@zone-overlap-logan-henderson-2026-10-24.md` `@mlb-k-matchups/README.md`

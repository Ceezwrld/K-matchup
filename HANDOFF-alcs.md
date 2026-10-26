# Handoff — MLB K-matchup / World Series

**Branch:** `cursor/ws-g3-off-fe0c`  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md`. World Series **G3 is OFF**: `@pregame-batter-leans-2026-10-26-ws-g3.md`. Gasser (L) vs Peralta (R) at the Trop, official nines. Next: live if either SP hooks ≤2 IP; then grade G3. Tools under `mlb-k-matchups/`.

## Done
- ALCS G3–G6 graded; series TB **4–2**
- Order-walk expected hits / RBI traffic
- **WS G1** locked + graded (MIL 3–2): `@backtest-2026-10-23-ws-g1.md`
- **WS G2** locked + graded (MIL 5–4): `@backtest-2026-10-24-ws-g2.md`
- **WS G3 OFF** locked (2026-10-26): Gasser vs Peralta, official nines. `@pregame-batter-leans-2026-10-26-ws-g3.md`

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
14. **One anchor bat on one 2-man only** (G1/G2 Bauers A HIT, Yandy B MISS both nights).
15. **O0.5 ≠ 2+** — G2 Yelich/Yandy both HRR 1. Process 0.5 HIT; user 2+ MISS.
16. **SP hook ~3 IP** → later box is vs bulk. Grade vs-SP separate from the full box.

## G2 grade snapshot (MIL 5–4)
- Process solos **4/5 HIT**: Aranda 1-4 2B · Bauers 1-3 · Contreras 2-5 HRR 3 · Yelich 1-4. **Yandy 0-5 MISS** (run makes HRR 0.5 a HIT).
- 2-man **A HIT** · **B MISS** (Yandy) · 3-man **HIT**. User 2+/3+ slip **1/3** (Contreras only); ride **$0**.

## G3 OFF snapshot
- **Peralta** Exp **5.51 STRONG** · STYLE **BAL** · Stuff+ **97** · O4.5 floor · no juiced O6 · MIL Hits O0.5 · lineup Exp H **3.86**
- **Gasser** Exp **3.83 SOFT FLY** · Stuff+ **106** · **UNDER_OK** U5.5+ · TB Hits vs LHP · lineup Exp H **4.48**
- TB OFF: Aranda/Hicks/Palacios **out** · **Vilade 2-hole TUNNEL** · Williamson 5 · Mesa **7** (still 2 PA, tiny) · Fortes 8 · **Caminero 1★** LHP TUNNEL
- MIL: same 2–3–4 · Contreras Hits/HRR · Bauers Hits (not auto-1★ vs Peralta) · Yelich GOOD · Frelick fade
- Fire: Caminero Hits/HRR · Contreras Hits/HRR · Vilade Hits · Yandy Hits · Bauers Hits · Yelich Hits/HRR
- 2-man: Caminero+Contreras · Yandy+Contreras (no second Caminero)
- Pass: Mesa 1★ in 7-hole · Williamson lock · Gasser U3.5 · Peralta juiced O6 · Frelick · Yandy 2+/HRR
- **G3 win lean:** TB slightly (Peralta STRONG + TB Exp H 4.48 vs Gasser FLY). Not a hammer — MIL pen / 2–3–4 still print.

## Open / next
1. Live re-lean if either SP hooks ≤2 IP
2. Grade G3 after final
3. G4 Tue 10/27 at Trop — likely Drohan (L) / leftover TB arm. Caminero LHP window can repeat if Drohan starts; 1 IP Drohan → incomplete.

## Files to @
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@pregame-batter-leans-2026-10-26-ws-g3.md` `@backtest-2026-10-24-ws-g2.md` `@zone-overlap-freddy-peralta-2026-10-26.md` `@zone-overlap-robert-gasser-2026-10-26.md` `@mlb-k-matchups/README.md`

# K-prop process lessons (from graded slates)

Living rules. Update after every backtest. Soft lines assume ~0.75+ edge unless noted.

## Every morning routine (do this first)

Run this **every morning** before tickets. Goal: one clear outlook for **every** probable starter.

1. **Refresh the board** (probable starters; usually all prior early):
   ```bash
   TZ=America/Chicago python3 mlb-k-matchups/k_matchups.py \
     --date YYYY-MM-DD \
     -o rankings-YYYY-MM-DD.csv \
     --html rankings.html \
     --hits-output hits-YYYY-MM-DD.csv
   ```
2. **Publish** CSV + `rankings.html` + hits CSV; note lineup status (`prior` vs `official`).
3. **Deliver the morning outlook** in this exact shape (arsenal-first):

   **Over leans** — arsenal ~#1–#3 / elite–strong (starter, not opener)  
   **Under leans** — soft / bottom-tier arsenal  
   **Fade / thin** — FILLER, openers, MATCHUP_OK (thin O3.5 only), high-risk watch list  

   For each arm include: **ark #**, **opp K% #**, Exp K, outing risk, game/time.  
   Mark the whole board **provisional** until official lineups post.
4. **Re-refresh when lineups confirm** — same report shape, flip prior→official, re-check leans before locking tickets.
5. **Accuracy lock before firing** — official nine in, starter not opener, side matches arsenal vulnerability, line edge still holds.

This morning pack is the daily starting point — not optional.

## Core thesis — pitcher vs batter vulnerability first

**Primary edge = arsenal matchup** (how this starter’s pitch mix stacks vs *this* opposing nine: matchup # / `expected_k_pct` / elite–soft grade).  
Exp K, projected IP, and raw opp lineup K% are **secondary**. Side selection (over vs under) starts from vulnerability, not the mean projection.

| Arsenal vs opposing nine | Lean | Why |
|--------------------------|------|-----|
| **Elite / strong (~#1–#3)** | **OVER** bias | Pitcher can beat a soft Exp K / hit O/U lines when bats are vulnerable to *his* mix |
| **Soft / poor (~bottom third, soft grade)** | **UNDER** bias | Even vs a high-K lineup, weak pitcher-vs-batter fit caps conversion — soft U6.5+ is live |
| **Mid-pack** | Pass / thin only | No clear vulnerability edge |

### Paired lesson (7/30) — opposite sides, same rule

Use these two together when deciding overs vs unders. **Arsenal matchup decides the side; opp team K% rank is secondary.**

| | **McLean vs MIA** | **Sasaki vs SEA** |
|--|-------------------|-------------------|
| Arsenal matchup | **#17 / soft** | **#3 / elite** |
| Opp lineup K% rank | **#5** (looks juicy) | **~#14** (looks soft) |
| Market line (example) | U6.5 | O5.5 |
| Result | **6 K — under HIT** | **7 K** (through ~5.1 IP, live) — **over cashed** |
| Read | Soft pitcher-vs-batter fit → under, even vs a high-K lineup on paper | Elite pitcher-vs-batter fit → over, even vs a weak team K% rank |

**Decision rule to keep:**  
1. Look at **pitcher arsenal vs that batting nine** first.  
2. If arsenal is soft/bottom → lean **under** (McLean). Don’t let a shiny opp K% rank talk you into the over.  
3. If arsenal is elite/strong (~#1–#3) → lean **over** (Sasaki). A middling/weak opp team K% rank matters less and should not fade a real dominance matchup.  
4. Then size the line (soft vs juice) with risk, IP, discipline, opener tags.

Other cards: **Barnett** (#2 elite / low Exp K) = matchup > mean projection, but opener ≠ full-start over. **Weathers** (#5) = not elite enough for over chalk (7 IP / 4 K).

## Core filters (kept working)

- Prefer **soft O3.5 / O4.5** with edge and **clear/low** outing risk — **only after** arsenal clears the over gate.
- **OVER gate — arsenal must rank well:** fire pitcher K overs when arsenal matchup vs that nine is **elite/strong (~slate #1–#3)**. Thesis: good pitcher-vs-batter fit can push a pitcher **over his projection / O/U line** even when Exp K looks modest. Mid-pack arsenal (#4+) → no ticket over (O3.5 floor max). Exp K and IP are secondary.
- **UNDER gate — soft arsenal is the edge:** when arsenal is **soft / bottom-tier** vs that nine, lean **unders** (esp. soft **U6.5 / U7.5**) even if opp lineup K% ranks high or Exp K sits near 5–6. McLean proved opp K% #5 ≠ over juice when arsenal is #17. Still: **no soft unders on SPIKE arms (K9 ≥ ~10)**; prefer wide edge under the line.
- Prefer **soft U6.5 / U7.5** with wide edge when arsenal is soft; **U5.5** OK if non-SPIKE and edge holds.
- **Fade unders on SPIKE arms (K9 ≥ ~10)** — they can jump a soft under even when proj is mid / arsenal looks soft.
- Fade **openers / uncertain swingmen** for *full-outing* K props (Barnett-style elite arsenal still isn’t a starter O4.5).
- **Medium/high** outing risk → need *more* edge for overs (or pass).
- **Soft-contact / low-K volume arms (K9 ≲ ~7, soft L3 Ks, elev_xFIP):** flag the **profile**, then check arsenal rank.
  - Soft profile + **avg/soft matchup** → **FILLER** — pass or O3.5 on Ks; does not help a K ticket.
  - Soft profile + **strong/elite arsenal matchup** → **MATCHUP_OK** — disclose the soft profile; soft O3.5 / thin O4.5 K only; still never a nuke anchor next to Wheeler-tier legs.
  - **Alt lane — pitcher outs:** when Ks are a poor fit (FILLER, or MATCHUP_OK but you don’t want the K over), consider **pitcher outs** instead if outing length / risk is clear-low and projected IP holds.
  - (7/27 Montero: soft profile + weak matchup → FILLER confirmed **1 K / 4.1 IP / 9 H**.)
- Exact-K MAE ~2 is normal; use **arsenal vulnerability for side**, Exp K for which line.
- **Card size: 2 legs.** Prefer straight 2-mans. 3-legs only when all legs are clear process (no filler/thin/prior). No 4/5/6-mans — correlation and early hooks kill bigger tickets.
- **Daily volume (when slate is full):** several **2-leg** tickets over fewer 3-mans. One chalk/nuke pair max; rest mix pitcher+bat or bat+bat. Cap any single player at **~2 tickets**.
- **Accuracy lock (before firing):** refresh with **official lineups**; only lock a leg if (1) batter is in the posted nine, (2) pitcher role is starter not opener/swingman, (3) **side matches arsenal vulnerability** (over only if ~#1–#3 elite–strong; under lean when soft/bottom-tier), (4) soft line edge holds on the *current* proj, (5) no same-game opposing K-over stack. Prior-lineup tickets are provisional only.
- **Disclose weak links:** if a recommended leg is filler/thin-sample/prior-lineup/SPIKE-capped, state that in the ticket writeup — don’t bury it.
- **Dual-rank read (vulnerability × context):**
  1. **Arsenal matchup rank (primary — decides over vs under)** — pitcher vs *these* batters.
  2. **Opp lineup K% rank (secondary)** — supports stretching an over or warns that a soft-arsenal under is fighting a K-prone nine (still take the under if arsenal is dead soft + line is soft U6.5+).
  3. **Plate discipline** — patient / walk-heavy can suppress K conversion on overs; free-swing helps overs.
  - **Over chalk:** arsenal ~#1–#3 *and* starter (Sasaki). Opp K% top-tier upgrades juice (O5.5+); **weak opp K% does not cancel** an elite arsenal over on a normal line (Sasaki O5.5 vs SEA #14). Still fade opener tags (Barnett).
  - **Under chalk:** arsenal soft/bottom-tier (McLean #17) + non-SPIKE + soft U6.5+; **ignore shiny opp K% rank** as an over reason.
  - **Pass:** mid arsenal, or opener, or SPIKE soft-under.
- **Length ≠ Ks:** full IP without elite arsenal isn’t an over lock (Weathers).
- **FILLER can spike:** Assad (FILLER) 4.23→6. Pass on tickets still correct; never soft-under FILLER either.

## 2026-07-30 partial (MAE ~1.89 on first 8 Final; evening still grading)

Early Final: TEX@TB, KC@MIN, NYY@CWS, CHC@STL. Also Final: MIA@NYM (McLean/Pérez), PIT@CIN, WSH@ATL. Still live: SF@SD, BOS@ATH, SEA@LAD.

| What happened | Lesson |
|---------------|--------|
| **Burke** 7.45→**10** (6 IP / 23 BF, clear) | Volume clear top-board cashed hard — O4.5/O5.5/O6.5 all hit; Burke-tier O5.5+ juice OK when proj ≥ ~7 and clear |
| **Weathers** 5.55→**4** (7 IP / 26 BF; arsenal **#5**, CWS lineup K% **#7**, disc neutral) | Arsenal **#5 fails the over gate** — contact outing, O4.5 miss / O3.5 HIT. Need top arsenal (#1–#3) vs the nine before firing overs |
| **McClanahan** 5.03→**3** (3 IP / 12 BF, clear, elite matchup) | Early hook again — elite K% matchup dead without outs. Outing survival > matchup grade for overs |
| **Cameron** 4.62→**7** (8 IP / 26 BF, clear, soft matchup) | Soft mid-board spiked with length — O3.5/O4.5 cashed; **don’t skinny-under** clear soft-grade arms when IP holds |
| **McLean** 5.47→**6** (6.1 IP; arsenal **#17 / soft**, MIA opp K% **#5**) | **U6.5 HIT.** Soft pitcher-vs-batter vulnerability beat the shiny opp K% rank — primary **under** edge validated |
| **Sasaki** ~5.3–5.6→**7+** (~5.1 IP live; arsenal **#3 / elite**, SEA opp K% **~#14**) | **O5.5 HIT** (user line). Opposite of McLean — elite arsenal cleared a soft/mid line even with weak team K% rank; opp K% mattered less |
| **Pérez** 5.19→**6** (6 IP; arsenal #8, NYM opp K% #2) | Mid arsenal vs elite K nine — cleared soft O4.5/O5.5 but not an arsenal-gate over chalk going in |
| **Ober** FILLER 5.04→**3** (6 IP) | FILLER correctly avoided O4.5; pass/O3.5 lane right |
| **Pallante** FILLER 4.71→**3** (6.1 IP / 7 H) | FILLER + outs alt still the read — K over miss; long outing via BIP |
| **Assad** FILLER 4.23→**6** (4.1 IP) | FILLER can still clear O4.5 — never a ticket *anchor*, but also **never soft-under** FILLER |
| **Winn** opener 1.06→**0** (1 IP) | Opener fade correct again |
| Soft **O3.5** clear/low e≥0.75 → **3/5 (60%)** | Weathers HIT floor; McClanahan + Pallante leaks (hook / FILLER) |
| Soft **O4.5** clear/low e≥0.75 → **1/2 (50%)** | Only Burke; Weathers the length-without-Ks miss |

### Reinforced from 7/30

1. **Paired confidence rule:** McLean (soft arsenal → **under**) and Sasaki (elite arsenal → **over**) are opposite proofs of the same edge — side from pitcher-vs-batter vulnerability first.
2. **Opp lineup K% is secondary** — MIA #5 did not force a McLean over; SEA #14 did not fade a Sasaki over.
3. **Barnett thesis kept:** elite arsenal can beat a tiny Exp K *if* he works as a real starter; opener tag still kills full-outing overs.
4. **FILLER:** Ober/Pallante validated pass; Assad spike warns against soft unders on the same tag.
5. Re-finalize Sasaki/Woo when SEA@LAD is Final; keep using this pair for future O/U decisions.

## 2026-07-27 lessons (MAE ~1.34, n=20 Final; HOU@LAA still live — excluded; CLE@CIN rain postponement)

| What happened | Lesson |
|---------------|--------|
| **Montero** 5.18→**1** (4.1 IP / 9 H), low risk / K9 6.6 | FILLER rule confirmed — O4.5 on soft-contact low-K arms is poison for multis |
| Soft **O3.5** clear/low → **4/6 (67%)** | Floor still usable; Montero+Kirby are the leaks |
| Soft **O4.5** clear/low e≥0.75 → **2/4 (50%)**; e≥1.0 → **1/2** | Weaker O4.5 night — Kirby 3 / Fried 4 (3 IP) both missed |
| **Wheeler** 5.85→**6** in only **3 IP** | SPIKE + clear still clears soft O4.5/O5.5 when hooked early — never soft-under |
| **Tolle** 5.13→**7** (5.1 IP) | Clear mid-board O4.5 cashed; thin O4.5 with real K9 is fine |
| **Fried** 5.40→**4** (3 IP) | Clear + edge died on early exit — outing length > matchup K% |
| **Perkins** 6.80→**4** (5.2 IP, medium) | Top-board swingman/medium risk O5.5+ chalk failed — don’t nuke medium tops |
| **Rocker** 5.29→**7** (6.2 IP) | Volume clear O4.5/O5.5 cashed when IP held |
| **Kelly** 5.30→**6** despite K9 5.6 / high risk | Low-K season ≠ auto-miss if length holds; still FILLER for *tickets* |
| **Yean** 2.51→**0** / **Scherzer** 2.91→**4** (2.2 IP) | Openers/short tags matter more than raw proj for full-outing props |
| CLE@CIN **Postponed** (Burns/Cecconi) | Rain outs void prior-lineup locks — don’t carry provisional tickets overnight |

### 7/27 card scorecard (discussed / late tickets)

- **Montero O4.5** — MISS (1). Correctly flagged FILLER; still burned if used as anchor.
- **Wheeler** — HIT soft overs (6 K / 3 IP).
- **Kirby O4.5** — MISS (3).
- **Fried O4.5** — MISS (4 / 3 IP early hook).
- **Tolle O4.5** — HIT (7).
- **Perkins** top-board — MISS vs high chalk (4 K).
- **HOU@LAA (Imai / Ureña)** — still live; excluded from this grade.

## 2026-07-26 lessons (MAE ~2.09, n=30; NYY@PHI still live at grade)

| What happened | Lesson |
|---------------|--------|
| Soft **O3.5** clear/low e≥0.75 → **11/13 (85%)** | O3.5 floor still the most reliable over lane |
| Soft **O4.5** clear/low e≥0.75 → **5/8 (62%)**; e≥1.0 → **3/6 (50%)** | O4.5 weaker than 7/25 — early hooks (Sánchez 2 IP / 2 K) and SEA@TEX both 4 K |
| **Ashcraft** 6.24→**5** | Soft **O4.5 HIT**, max **O5.5 MISS** — reinforces O5.5 as juice-only even at ~6.2–6.5 |
| **Misiorowski** 6.70→**12** | PP soft **6.5 More** would have cashed; model undershot ceiling. SPIKE + soft COL = smash. Don’t need O4.5 hesitation when board soft is already 6.5 |
| **Gilbert / deGrom** both **4 K** | Same-game opposing K overs both missed — correlation risk was real |
| **Gausman** 5.57→**6** | Avoiding him for “form tilt” left a cashing O4.5; last-start sample ≠ fade with clear edge |
| **Buehler** 3.67→**7** | Soft **U4.5/U5.5** on medium arms still leaky — need wider under lines |
| **Rasmussen** 4.53→**9** / **Messick** 4.04→**6** | Low-mid proj clear arms can still rack Ks in volume outings — don’t skinny-under |
| **Sánchez** 5.74→**2** (2 IP) | Clear + edge died on early exit — outing length risk dominates K overs |
| Bats: **Peña / Chourio** Hits cashed; **Vaughn** 1 H (HRRBI cashed); **Lopez / Walker / Yordan** missed | Prefer Hits on elite vs-hand AVGs; H+R+RBI saved Vaughn-style power nights |

### 7/26 card scorecard (discussed tickets)

- **Ashcraft O4.5** — HIT (5). **Ashcraft O5.5** — MISS.
- **Gilbert O4.5 / deGrom O4.5** — both MISS (4).
- **Misiorowski** — we passed PP 6.5; actual **12** (would have hit every over).
- **Gausman O4.5** — HIT (6); fade was wrong today.
- **Peña Hits O1.5** — HIT (2). **Vaughn Hits** — MISS (1); **H+R+RBI** HIT.
- **Chourio Hits** — HIT. **Yordan / Lopez / Walker** — MISS.
- **NYY@PHI live:** Sánchez **2 K / 2 IP** (O4.5 dead), Warren **2 H** through 2 IP, Marsh **0-1** (in progress).

## 2026-07-25 lessons (MAE ~2.00, n=29; Paredes scratched)

| What happened | Lesson |
|---------------|--------|
| Soft O4.5 edge≥0.75 went **6/7**; clear/low **4/4** | Keep O4.5 clear/low as the primary over lane |
| **Imanaga O4.5** (proj 4.63 → 4) missed | Thin O4.5s (edge under ~1.0, especially medium risk) are **leaks** — need ~1.0+ edge or stick O3.5 |
| **Bibee U4.5** (proj 4.03 → 5) missed | Soft **U4.5** when proj sits ~4.0 is too tight — prefer **U5.5** or pass |
| **Young U5.5** (proj 4.33 → 6) missed | Low-K projection ≠ locked under; leave room or demand wider edge |
| **Pallante** 3.93 → **8** | Clear + soft proj can still spike — don’t skinny-under without cushion |
| **Greene** 6.72 → **3** (medium SPIKE) | Medium-risk SPIKE overs are volatile — need extra edge or pass |
| **Cease / Skenes** crushed overs | SPIKE upside is real — never soft-under them; O3.5 safer than forcing thin O4.5 on SPIKE |
| **Burke** volume / **Yoshi O4.5** (5 K) | Volume+clear O4.5 good; **O5.5 stretch** on Yoshi would have failed — treat O5.5 as juice only |
| **Mayza / short Vásquez** stayed down | Opener/short tags continue to save unders / fade full-outing overs |
| **Paredes scratched** | Confirm probable before betting thin boards |

### Reinforced card rules

1. **O4.5 core:** clear/low, edge ≥ ~1.0 preferred (≥0.75 minimum).
2. **O5.5:** only with proj ≥ ~6.3–6.5 and clear (Burke-tier volume) — not default.
3. **U4.5:** only if proj ≤ ~3.5 and non-SPIKE; otherwise **U5.5+**.
4. **Same-game:** pitcher K over ↔ opposing bats for hits is fine; never pitcher K over + that team’s bats for hits vs him.
5. Log misses into this file after each `backtest-YYYY-MM-DD.csv`.

## Prior days (short)

- **7/26:** MAE ~2.09; O3.5 strong / O4.5 mixed; Ashcraft O5.5 miss; Misio 12; Sánchez early hook; Gausman fade wrong.
- **7/24:** Soft O3.5 ~76%, O4.5 ~67%; Miller 0 K killed multis; Manaea swingman fade / Way opener correct.
- **7/23:** MAE ~2.03; Sale U7 failed (SPIKE/high K night) — don’t soft-under elite K arms.

## Model upgrades (2026-07-27)

- **Outing survival:** `bf_risk_factor` now also haircuts for short recent IP and HR/xFIP+BB exit risk (floor 0.82).
- **Opp. lineup offense:** recent (else season) lineup K%/AVG → mild ±7% `offense_factor` on matchup Ks before form blend.
- Next: optional batter barrel/hard-hit layer for Hits props (not for pitcher K mean).

- **Hits board (2026-07-27):** barrel% / hard-hit% / xwOBA + AVG vs hand → `hits_score` / `hr_rbi_score` only. Explicitly isolated from `expected_ks`.

- **Ticket outlook (2026-07-28):** FILLER is no longer pitcher-only. Soft-contact profile is gated by opposing lineup **arsenal rank** (`expected_k_pct` percentile → `MATCHUP_OK` vs `FILLER`).
- **Plate discipline (2026-07-28):** opposing lineup **BB%** + K% shape → `discipline_grade` / `pitch_count_risk`. Patient/walk-heavy nines trim BF/IP and soften K projections (beyond raw batter K%).

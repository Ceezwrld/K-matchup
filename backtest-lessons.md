# K-prop process lessons (from graded slates)

Living rules. Soft lines assume ~0.75+ edge unless noted.

## Learn from every miss (non-negotiable)

**Every mistake updates the routine before the next ticket.** Not only end-of-night grades — mid-slate misses count (Young 13 outs / 98 pitches → Zone%/efficiency now in Step 5).

When a locked leg loses or a lean is clearly wrong:
1. **What broke?** (side / total / length / efficiency / line / role)
2. **Write the rule** into this file (ticket lock + same-day note).
3. **Apply on the next card** — do not repeat the same miss.
4. Full-slate grade still runs after finals (`backtest-YYYY-MM-DD.csv`) and folds into the same living rules.

Hits reinforce; misses rewrite the checklist. No silent losses.

## 2026-08-13 early/midday grade — process vs book (n=12 finals)

Full detail in `backtest-2026-08-13-early.csv`. Box scores verified via MLB StatsAPI. Board snaps: **morning** lite odds for 12:10/12:35 tips; **afternoon** OFF+odds for CHC@WSH (3:05). BOS@TOR graded on morning K line (5.5 Tolle) with afternoon alt (6.5) noted. Late still live: PHI@MIN · TEX@LAA · MIL@LAD → full slate `backtest-2026-08-13.csv` after finals.

**Model fit:** mean Exp **4.74 → 5.33** act · bias **+0.59** · MAE **2.07** (wider than 8/12’s 1.55 — Ashcraft/Cavalli +5 ceilings + Montero −3.25).  
**K over @ posted snap book:** **6/12 (50%)**. Blind chalk over is coin-flip; process lanes split cleanly.

### User ticket

| Arm | Snap Exp → Act | Book K | Leg | Result | Box |
|-----|----------------|--------|-----|--------|-----|
| **Parker Messick** | 5.63 → **6** | 5.5 | **O5.5** | **HIT** | 5.2 IP · 3 H / 2 ER / 2 BB / 1 HR · BF 23 · 102/59 |
| **Logan Gilbert** | 6.08 → **7** | 6.5 (→5.5 aft) | **O4.5** | **HIT** | 6.0 IP · 4 H / 0 ER / 1 BB · BF 22 · 95/59 · O5.5 & O6.5 also HIT |

### Pitcher-by-pitcher (metrics × book × actual)

| Arm | Process / lean | Stuff+ · Arv · Contact · Spike | Exp · Book K · Edge · P(O) | Act K/H/ER (IP) | K over | Process grade |
|-----|----------------|--------------------------------|----------------------------|-----------------|--------|---------------|
| **Messick** | User O5.5 · AVG/WHIFF clear | 97 · −1.0 · neutral · no | 5.63 · **5.5** · +0.13 · 51% | **6**/3/2 (5.2) | **HIT** | **CONFIRM** — Exp≈book; rate held (26% act) |
| **Montero** | UNDER_OK quiet; fade K-over juice | 95 · −1.7 · soft · no | 3.25 · **2.5** · +0.75 · 65% | **0**/3/0 (6.1) | **MISS** | Quiet **CONFIRM** (H/ER unders HIT) · fat K edge = **trap** |
| **Abbott** | Damage H/ER; fade K | 95 · +2.2 · strong flags | 4.05 · **4.5** · −0.45 · 38% | **3**/7/5 (4.1) | MISS | **CONFIRM_DAMAGE** — BB/xFIP flags printed |
| **Martin** | O3.5 max · length veto | **90** · −1.9 · elite label | 4.87 · **4.5** · +0.37 · 56% | **3**/2/3 (**2.0**) | MISS | **CONFIRM_LENGTH_VETO** — Stuff+90 + short_recent_ip |
| **Ashcraft** | SPIKE ceiling · never soft-under | **106** · **+2.4** · SPIKE | 4.71 · **5.5** · −0.79 · 32% | **10**/3/1 (**9.0**) | **HIT** | **CONFIRM_SPIKE** — Exp undershoot +5.3; soft-under dies |
| **Phillips** | MATCHUP_OK O3.5 floor | 96 · +1.1 · whiff_prone | 5.29 · **3.5** · **+1.79** · 81% | **6**/6/4 (5.1) | **HIT** | K floor **CONFIRM** + damage co-path (not clean) |
| **Gilbert** | User O4.5 floor · ELITE stack | **109** · +1.5 · whiff_prone · SPIKE | 6.08 · **6.5** · −0.42 · 41% | **7**/4/0 (6.0) | **HIT** | **CONFIRM** — floor sizing; elev_hr quiet |
| **Fried** | O4.5 lean · not O5.5 juice | 106 · +0.2 · SPIKE | 5.32 · **5.5** · −0.18 · 45% | **4**/5/1 (5.0) | MISS | **PARTIAL** — O4.5 would HIT; O5.5 miss |
| **Tolle** | SPIKE · no soft-under · fade aft 6.5 | **115** · −1.6 · contact_heavy · SPIKE | 5.39 · **5.5** (→**6.5**) · −0.11→−1.11 | **4**/2/0 (**8.0**) | MISS | **PROCESS_OK_MIXED** — gem without Ks; rule held |
| **Scherzer** | Fade K over · soft damage | 93 · +2.0 · MATCHUP_OK aft | 2.88 · **4.5** · −1.62 · 14% | **4**/3/1 (5.0) | MISS | **SOFT_MIXED** — miss by 0.5 K; damage overstated |
| **Gausman** | Aft OFF cut; not clean K | 98 · +2.5 · whiff_prone | **4.93** · **5.5** · −0.57 · 37% | **7**/7/6 (4.2) | **HIT** | **MIXED** — K cashes with blowup; morn 6.16/4.5 was wrong world |
| **Cavalli** | Fade O5.5 (not chalk under) | 102 · **−1.8** · whiff_prone | **4.49** · **5.5** · −1.01 · 28% | **10**/1/0 (**8.0**) | **HIT** | **MISS_FADE** — Castillo-style; BF collapse hid ceiling |

### Book line movers (why the board shifted)

| Arm | Morning | Afternoon | Actual | Read |
|-----|---------|-----------|--------|------|
| Gilbert K | **6.5** (edge −0.42) | **5.5** (edge +0.59) | 7 | Book cut into model; user O4.5 was the safe side either line |
| Tolle K | **5.5** (aligned) | **6.5** (edge −1.11) | 4 | Juice over after open — fade juiced O6.5 correct; soft under still vetoed by SPIKE |
| Gausman K | **4.5** / Exp **6.16** (edge +1.66) | **5.5** / Exp **4.93** | 7 | Morning fat edge was the danger signal; OFF refresh fixed direction |
| Cavalli Exp | 3.92 | 4.49 (BF ~20) | 10 | Still too low — Arv− vs whiff_prone + Stuff+≥100 + length |
| Ashcraft K | 5.5 | live **8.5** | 10 | In-game alt; pregame SPIKE read was the ticket frame |

### Process buckets

| Lane | Arms | Exp → Act | Verdict |
|------|------|-----------|---------|
| **User / ELITE stacks** | Messick, Gilbert | 5.86 → **6.50** | **2/2 HIT** — WHIFF + OFF + (Gilbert Stuff+109) |
| **SPIKE** | Ashcraft, Tolle | 5.05 → **7.00** | Never soft-under **held**; Ashcraft ceiling cashed; Tolle = length gem / K miss |
| **DAMAGE / quiet** | Abbott, Montero, Scherzer | 3.39 → **2.33** | Abbott damage **CONFIRM**; Montero quiet **CONFIRM**; Scherzer damage soft |
| **MATCHUP_OK / length** | Phillips, Martin | 5.08 → **4.50** | Phillips O3.5 OK; Martin length veto **CONFIRM** |
| **Aft OFF** | Gausman, Cavalli | 4.71 → **8.50** | Gausman chaos K; Cavalli fade **MISS** |

### Hits / ER vs book (where posted)

| Arm | Book H / ER | Act H / ER | H over | ER over |
|-----|-------------|------------|--------|---------|
| Messick | 4.5 / 2.5 | 3 / 2 | MISS | MISS |
| Montero | 4.5 / 2.5 | 3 / 0 | MISS (under side) | MISS (under side) |
| Ashcraft | 4.5 / 1.5 | 3 / 1 | MISS | MISS |
| Phillips | 4.5 / 1.5 | 6 / 4 | **HIT** | **HIT** |
| Gilbert | 4.5 / 2.5 | 4 / 0 | MISS | MISS |
| Fried | 4.5 / 1.5 | 5 / 1 | **HIT** | MISS |
| Tolle | 4.5 / 1.5 | 2 / 0 | MISS | MISS |
| Scherzer | 4.5 / 2.5 | 3 / 1 | MISS | MISS |
| Gausman | 4.5 / 2.5 | 7 / 6 | **HIT** | **HIT** |
| Cavalli | 5.5 / 2.5 | 1 / 0 | MISS | MISS |

Abbott/Martin: no H/ER books on morning snap — damage read was flag-driven (printed on Abbott).

### Biggest Exp misses

**Model low (undershoot):** Ashcraft **+5.29** · Cavalli **+5.51** · Gausman **+2.07**  
**Model high (overshoot):** Montero **−3.25** · Martin **−1.87** · Tolle **−1.39** · Fried **−1.32**

### Reinforced (lock after early 8/13)

1. **User ticket process worked** — Messick aligned O5.5; Gilbert O4.5 floor on Stuff+109 / whiff_prone / SPIKE.
2. **Never soft-under SPIKE** — Ashcraft 10 K is the exhibit; Tolle soft-under would cash *result* but process correctly blocked (K ceiling still live pregame).
3. **Fat `k_edge` ≠ ticket** — Montero +0.75 / P(O) 65% → 0 K; Gausman morning +1.66 was the warning before OFF cut.
4. **MATCHUP_OK = O3.5 + length** — Phillips 6 K OK; Martin 2 IP veto held (Stuff+90).
5. **Damage flags > matchup label** — Abbott strong arsenal / 7H/5ER; Scherzer damage was soft — need BIP/contact_heavy for juice.
6. **Castillo/Cavalli rule** — do **not** hard-fade K over when opp is **whiff_prone** + Stuff+≥100 + 5+ IP path, even with Arv− and model under book (fade ≠ chalk under, but today’s fade was wrong).
7. **Afternoon OFF matters** — Gausman Exp 6.16→4.93 and line 4.5→5.5 before tip; morning juice was not the betting board.

### Watch / still open

| Item | Note |
|------|------|
| **Nola O4.5 H** (user) | PHI@MIN Pre-Game — grade after final |
| Bradley SPIKE / pass | Held — do not chase |
| Late TEX@LAA / MIL@LAD | Refresh OFF 1–2h pre tip; lite odds only if asked |
| Cavalli-style Arv− | Add to fade checklist: whiff_prone + Stuff+≥100 → no hard fade |

**Process stance after early 8/13:** ticket lane clean (2/2); SPIKE/UNDER_OK/length rules held; biggest miss = Cavalli fade; biggest model miss = Ashcraft/Cavalli ceilings. Full slate after late finals.


## 2026-08-12 grade — K-gate held; bad-game T1 split; MATCHUP_OK length veto

Full slate in `backtest-2026-08-12.csv` (n=**29** with Exp K; Jackson Kent unscored). Mean Exp K **4.37 → 3.93** act (bias **−0.44**, MAE **1.55**). Model ran slightly hot on Ks — same MAE band as 8/11.

### Headline scorecard

| Lane | Result | Takeaway |
|------|--------|----------|
| **K-good gate (Miller only PASS)** | **5 K** / 6.0 IP (Exp 5.78) | Floor OK; **8 H / 5 ER** — elev_hr vetoed “clean good game” |
| **Matthews soft-Stuff ELITE** | **4 K** / Exp 6.22 | Gate correctly blocked; mid-slate note stands |
| **Bad-game T1 damage** | **3/6** clear H+ER cash | Kelly / Perkins smashed; Feltner H+; **Houser / Lauer / Quantrill** faded |
| **MATCHUP_OK** | **Mlodzinski 1 K / 2.1 IP** | Length kill — O3.5-only was the max |
| **UNDER_OK** | Suarez **2** cashed; **May 6** wrecked under | Stuff+≥100 UNDER_OK ≠ chalk under |
| **Castillo spike** | Exp 4.91 → **10 K** | Whiff_prone CWS + length; Arv −3 underweighted ceiling |

### Process buckets

| Layer | n | exp → act | Notes |
|-------|---|-----------|-------|
| **Top Exp (≥5.5)** | 4 | 5.99 → 5.25 | Miller 5 / Peterson 6 / Quantrill 6; **Matthews 4** drag |
| **SPIKE flag** | 12 | 4.25 → 3.92 | Near flat; never soft-under (Houser 5, Wheeler 5, Soriano 4, Lynch 3) |
| **UNDER_OK** | 4 | 3.52 → 3.25 | Suarez 2 / Feltner 2 / Valdez 3; **May 6** outlier |
| **MATCHUP_OK** | 3 | 4.78 → 3.00 | Lauer **6** OK; Thornton **2**; **Mlodzinski 1** length dud |
| **FILLER** | 3 | 4.69 → 3.33 | Kelly 2 / Junk 2 correct fade; Quantrill 6 = pass-not-fade |

### K-good sheet (gates: whiff_prone + Stuff+≥100 + ArvOpp>0)

| Arm | Gates | Exp → Act | H/ER | Note |
|-----|-------|-----------|------|------|
| **Bryce Miller** | **PASS** | 5.78 → **5** | **8 / 5** | Only full PASS; O4.5 K live, O5.5+ thin; elev_hr fired |
| Matthews | fail Stuff+ | 6.24 → **4** | 6 / 4 | Soft Stuff+ ELITE — blocked correctly |
| Lowder | fail Stuff+ | 4.96 → **4** | 7 / 2 | Stuff+86; flat K, damage noise |
| Castillo | fail Arv | 4.91 → **10** | 1 / 0 | Gate missed ceiling (Arv −3) but opp whiff_prone + 7 IP |

### Bad-game T1 / T2 (damage)

| Tier | Arm | Actual | Grade |
|------|-----|--------|-------|
| T1 | **Merrill Kelly** | 6 H / **6 ER** / 2 K | **HIT** — flags (high_hr/exit_hr) printed |
| T1 | **Jack Perkins** | **12 H / 6 ER** / 2 K | **HIT** — SPIKE outlook ≠ damage fade |
| T1 | **Ryan Feltner** | **7 H** / 2 ER / 2 K | **H HIT** / ER push at 2.5 |
| T1 | Adrian Houser | **2 H / 0 ER** / 5 K | **MISS** — T1 false positive (SPIKE + clean outing) |
| T1 | Eric Lauer | 4 H / 1 ER / **6 K** | **MISS** — MATCHUP_OK K side won; damage thesis lost |
| T1 | Cal Quantrill | 4 H / 1 ER / **6 K** | **MISS** — sheet marked thesis=False; correct skepticism |
| T2 | Soriano / Ray | 4H/1ER · 2H/2ER | **MISS** damage — short/quiet |

**Posted prop overs (partial book):** Kelly H/ER **HIT**, K MISS · Perkins H/ER **HIT**, K MISS · Houser K **HIT**, H/ER **MISS** · Wheeler H/ER **HIT** vs chalk U on K7.5 · May K **HIT** · Rasmussen ER **HIT**, K/H MISS.

### Biggest K deltas

**Model high (misses):** Mlodzinski −4.1 · Perkins −2.6 · Thornton −2.4 · Baz −2.3 · Kelly −2.3 · Matthews −2.2  
**Model low (undershoots):** Castillo **+5.1** · May +2.1 · Lynch +2.0 · Leahy +1.8 · Mahle +1.6

### Reinforced (lock)

1. **K-good gate** — Miller-only PASS → 5 K floor; still require **elev_hr / exit_hr size-down** before calling a “good game” ticket.
2. **ELITE + whiff_prone needs Stuff+≥100 + ArvOpp > 0** — Matthews 6.22→4 stands (see mid-slate note below).
3. **MATCHUP_OK = O3.5 floor + length check** — Mlodzinski 2.1 IP / 1 K; Thornton 2 K; do not juice without clear IP.
4. **Bad-game T1 ≠ auto ticket** — demand BIP/contact_heavy + risk flags; fade when SPIKE + soft-contact alone (Houser gem). Quantrill thesis=False was the right tell.
5. **Never soft-under SPIKE** — held (no chalk unders on Houser/Wheeler/Soriano).
6. **UNDER_OK + Stuff+≥100** — May 6 K; treat as thin under / prefer H-ER elsewhere (Feltner H cashed).
7. **FILLER ≠ fade every over** — Quantrill Exp inflated but 6 K; FILLER means “not a K anchor,” not “must under.”

### Watch only

| Read | Note |
|------|------|
| Castillo-style Arv− / whiff_prone | Ceiling can still nuke — don’t hard-fade K when opp is whiff_prone + 5+ IP |
| Houser T1 | Soft-contact + elev_hr without contact_heavy BIP → false damage |
| Warren SPIKE | 3 K / 5 ER / 3 HR — SPIKE without elite Arv still chaos, not under chalk |

**Process stance after 8/12:** K-gate + Matthews rule held; damage lane only when thesis+flags align (Kelly/Perkins); length veto on MATCHUP_OK; UNDER_OK needs Stuff+ check before chalk under.

---

## 2026-08-12 mid-slate — Zebby Matthews K miss (what broke)

Partial note (kept for ticket timeline). Full finals in `backtest-2026-08-12.csv`. Focus arm: **Matthews vs BAL**.

| | Pregame | Actual |
|--|---------|--------|
| Exp K / Act K | **6.24** | **4** (Δ **−2.24**) |
| IP | 5.4 proj | **5.0** (94 pitches / 60 strikes) |
| BF | 23 | **22** |
| H / ER / BB / HR | — | **6 / 4 / 2 / 1** |
| Solo / contact | ELITE · whiff_prone | K% act **18.2%** (4/22) vs Exp K% **25.3%** |
| Stuff+ / ArvOpp | **94.9** / **+0.48** | Failed later K-gate (Stuff+≥100) |
| Risk flags | high_hr, elev_xfip, exit_hr | **HR + 4 ER** — flags fired |

**Ks:** O'Neill, Beavers, Holliday, Taveras. Damage: Henderson BB → Alonso 1B (1st); Franklin/Narváez 1Bs (2nd); Alonso 1B → O'Neill 1B → **Beavers 3-run HR** (3rd).

### What went wrong (stack)

1. **Stuff+ undercut the ELITE chip** — season K% only **20**, Stuff+ **94.9**, stuff_grade **avg**. Model Exp was driven by opp whiff_prone + arsenal_abs **elite**, not by a true miss kit (same shape as Bradford 8/11 TRUST dud).
2. **Arsenal vs opp was thin** — ArvOpp only **+0.48** (barely positive). Lineup was “whiff_prone” on season K%/BIP, but not clearly vulnerable to *his* mix.
3. **Damage flags were pre-printed** — high_hr / exit_hr / elev_xfip → Beavers HR + 4 ER. K script died in the crooked 3rd; pitch count (94/5) also capped a 6+ K climb.
4. **SPIKE was L3 form, not stuff** — L3 K9 ~10.8 spiked the card, but outing SPIKE without Stuff+≥100 is form noise (Miller gate later required both).
5. **Efficiency / patient BAL** — three_true BB% ~10.7; 2 BB + traffic → early leash pressure. Got to 5 IP but never ran a clean K inning after the 1st.

### Rule written (lock)

- **ELITE + whiff_prone is not enough** without **Stuff+ ≥ ~100** *and* **arsenal_vs_opp clearly >0** (prefer ≥+1). Matthews 8/12 is the exhibit: Exp 6.24 → 4 K.
- Treat **high_hr / exit_hr** as a hard size-down on K overs even when contact_grade = whiff_prone.
- L3 K9 SPIKE alone does **not** override soft Stuff+.

## 2026-08-11 grade — hits lane cashed; TRUST dud + SPIKE under killed ticket

Full slate in `backtest-2026-08-11.csv` (n=**30** Final). Mean Exp K **4.53 → 4.40** act (bias **−0.13**, MAE **1.51**).

### User 7-leg ticket — **4/7 DEAD**

| Leg | Actual | Result | Break |
|-----|--------|--------|-------|
| Snell **U6.5 K** | **10 K** / 6.0 IP | **MISS** | AVG+**SPIKE**+WHIFF ceiling — never under SPIKE, even on “chalk” U6.5 |
| R. Johnson **U4.5 K** | **5 K** / 4.1 IP | **MISS** | FILLER ≠ UNDER_OK; Exp 3.4 lied soft |
| Bratt **O3.5 K** | **4 K** / 6.0 IP | **HIT** | MATCHUP_OK floor — O4.5 would miss |
| Sugano **O5.5 H** | **6 H** / 6.0 IP | **HIT** | Soft-contact + volume |
| Bradford **O3.5 K** | **1 K** / 7.0 IP | **MISS** | TRUST dud — tiny-sample ELITE/WHIFF + Stuff+ **86** undercut |
| Wacha **O4.5 H** | **7 H** / 6.2 IP | **HIT** | UNDER_OK soft-contact vs LAD |
| Martinez **O4.5 H** | **8 H** / 9.0 IP | **HIT** | Soft FILLER + long leash |

**Killers:** Snell SPIKE under + Bradford TRUST collapse (+ Johnson FILLER under).  
**Hits 3/3** on the card (Sugano/Wacha/Martinez) — strongest lane of the night.

### Discussed alts scorecard

| Alt | Actual | Result |
|-----|--------|--------|
| Bibee H O4.5 / ER O2.5 | 5 H / 5 ER | **HIT / HIT** |
| Lodolo ER O2.5 | 4 ER | **HIT** |
| Pallante U4.5 K | 2 K | **HIT** (UNDER_OK) |
| Whisenhunt BB O2.5 | 3 BB | **HIT** (thin lean OK) |
| Whisenhunt H/ER O | 4 H / 1 ER | MISS / MISS — short-outing veto right |
| Harrison O4.5 K | 3 K | **MISS** (fade correct) |
| Johnson ER/H O | 1 ER / 3 H | MISS / MISS — no rescue swap |

### Process buckets

| Layer | Signal |
|-------|--------|
| **TRUST** (n=1 Bradford) | **1 K / Exp 5.9** — catastrophic; tiny sample + Stuff+86 was the pre-flag |
| **THIN_TOTAL** (Imanaga/Woo) | both **5 K** vs Exp ~6.2 — juiced overs correctly blocked |
| **UNDER_OK** (Pallante/Wacha) | Pallante **2 K** cashed; Wacha K soft but **H O4.5** smashed |
| **MATCHUP_OK** (Bratt/Lodolo/Ober) | Bratt **4** = O3.5 only; Lodolo ER live; Ober **4 K / 8 H** |
| **SPIKE** (n=14) | mean ~flat; **Snell 10** / Eury·Cease·Sánchez·Burke **7–8** vs McLean **3** / Bradford **1** — veto soft+chalk unders |
| **soft-contact H>4.5** | **6/10** cashed (Wacha/Martinez/Sugano/Bibee/Ober/Lodolo) |

### Reinforced (lock)

1. **Never under SPIKE** — Snell U6.5 is the textbook chalk-under trap when WHIFF+elite stuff.
2. **THIN_TOTAL** — Imanaga/Woo 5K again; O3.5/thin O4.5 only.
3. **UNDER_OK / soft-contact hits** — Pallante K under + Wacha/Martinez/Sugano/Bibee H overs.
4. **MATCHUP_OK = O3.5 floor** — Bratt 4K; do not juice O4.5.
5. **TRUST needs Stuff+ confirm** — Bradford Stuff+86 + 70-pitch sample → treat as thin/caution next time, not floor O3.5 hammer.

### Watch only

| Read | Note |
|------|------|
| Tiny-sample TRUST | Bradford — require Stuff+ ≥~95 or larger pitch pool before TRUST floor overs |
| FILLER K unders | Johnson 5K — need UNDER_OK (2+ confirms), not Exp alone |
| Harrison-style K fade | 3K correct; 10 H was outing chaos — don’t retrofit H overs on SPIKE/WHIFF |

**Process stance after 8/11:** hits/UNDER_OK lane strong; SPIKE-under ban absolute; TRUST must survive Stuff+/sample check; THIN_TOTAL + MATCHUP_OK sizing held.

## 2026-08-10 grade — TRUST / ELITE / WHIFF / SPIKE confirmed; advanced noise watched

Full slate in `backtest-2026-08-10.csv` (n=**20** Final). Mean Exp K **4.67 → 5.15** act (bias **+0.48**, MAE **1.38**). Model slightly under — same direction as several prior nights.

| Solo grade | n | mean expK → act | Notes |
|------------|---|-----------------|-------|
| **ELITE** | 5 | 5.74 → **6.80** | Gore **9**, Kremer **7**, Detmers/Scott/Mize **6** — all ≥6 |
| **STRONG** | 3 | 4.02 → **6.00** | Dobbins / Painter / Tidwell all **6** |
| **AVG** | 5 | 4.62 → **3.60** | Cameron **2**, Hughes **3**, Wesneski **4** — pass lane right |
| **SOFT** | 7 | 4.23 → 4.71 | No-SPIKE held under-ish; SPIKE arms (Henderson **7**, Skubal **6**) spiked |

| Layer | Signal |
|-------|--------|
| **TRUST** (n=2) | Detmers **6/6.0**, Gore **9/5.1** — both overs cashed |
| **WHIFF** (n=5) | 5.63 → **6.80**, game K% **30.1** — best style bucket |
| **SPIKE** (n=8) | 4.73 → **6.12** — soft-under veto correct |
| **whiff_prone opp** (n=4) | avg **7.0K** / game K% **30** |
| **Stuff+ ≥105** (n=5) | avg **6.2K** (Detmers/Scott/Skubal/Henderson/Tidwell) |
| **contact_gb** | Gray **4K / 15.4%** in 6 IP — BIP-outs script true |
| **SOFT no-SPIKE** | Elder **4**, Soroka **4**, Taillon **3** — stayed soft |

### Ticket / lean scorecard

| Lean | Actual | Result |
|------|--------|--------|
| **TRUST Detmers** | 6 K / 6.0 IP | **HIT** — length held (unlike 8/5 short Detmers) |
| **TRUST Gore** | **9 K** / 5.1 IP | **HIT** — ceiling cashed |
| **ELITE+WHIFF Scott** | 6 K / 4.0 IP | **HIT** thin length; K% still 28.6 |
| **SPIKE no soft U — Skubal / Henderson** | 6 / 7 | Veto **correct** |
| **SOFT no-SPIKE Elder / Soroka / Taillon** | 4 / 4 / 3 | Under-ish **HOLD** |
| **AVG pass Cameron / Hughes / Wesneski** | 2 / 3 / 4 | Pass **correct** — no juice |
| **Kremer ELITE** (elev FIP 5.89 / Stuff+ 89 pre-flag) | **7 K** / 7.0 IP | Arsenal + whiff_prone beat advanced fade |
| **Tidwell** (Exp 1.30 opener proj; STRONG+SPIKE) | **6 K** / 5.2 IP | Short-IP proj lied; SPIKE/STRONG was the true read |

### Reinforced (lock — already process)

1. **TRUST** when IP holds — Detmers/Gore both cashed.
2. **ELITE / STRONG solo** as over juice — every ELITE/STRONG ≥6K.
3. **WHIFF** is the K-style edge; **SPIKE** still vetoes soft U6.
4. **whiff_prone opp** confirms overs; **AVG pass** and **SOFT no-SPIKE** stay non-nuke.
5. **Stuff+ ≥105** supported the SPIKE/TRUST ceiling pack this night (confirm only — does not move Exp K).

### Watch only (n=1 — do **not** rewrite rules yet)

| Read | Why it stays provisional |
|------|--------------------------|
| Season **Strike% ≥65** sizing gate | Did **not** separate (4.9K vs 5.3K). Game Strike% collapses still matter; board Strike% alone did not. |
| **FIP / Loc+** as K predictors | Low vs high FIP both ~5.1–5.2K; Loc+≥105 flat vs rest. |
| **under_n ≥2** on SPIKE/STRONG | Tidwell/Lopez noise — do not under those chips. |
| **Elev FIP vetoes ELITE** | Kremer smoked the fade; keep as caution, not auto-pass. |
| Short/opener **IP proj** (Tidwell 1.3→5.2) | Prefer STRONG+SPIKE over raw Exp when role/proj looks broken. |

**Process stance after 8/10:** reinforce the chip stack (TRUST · ELITE/STRONG · WHIFF · SPIKE · whiff_prone). Leave Strike%/FIP/Loc+/under_n tweaks as watch items until they show clean on ~2–3 graded nights.

## 2026-08-08 grade — board clears cashed; under lane mixed

Full slate in `backtest-2026-08-08.csv` (n=29 scored, mean Exp K 4.81 → act 4.83, bias **+0.02**).

### Ticket leans
| Leg | Actual | Result | Break |
|-----|--------|--------|-------|
| **Sale oK** (ELITE/WHIFF/clear Exp ~7.8) | **8 K / 6.0 IP** | **HIT** O4.5/O5.5 | Board clear + attack-plate — trusted correctly |
| **Williams oK** (STRONG/WHIFF/low Exp ~7.1) | **7 K / 5.7 IP** | **HIT** O4.5/O5.5 | #2 clear; three-true sizing OK |
| **Burns oK** (STRONG/WHIFF/clear Exp ~5.4) | **6 K / 5.3 IP** | **HIT** O4.5/O5.5 | Cleanest risk over on the card |
| **deGrom oK** (ELITE/WHIFF/low Exp ~6.5) | **9 K / 5.0 IP** | **HIT** O4.5/O5.5 | Zone soft didn’t kill the script |
| **Nola U6.5** (UNDER_OK OFF Exp ~3.5) | **8 K / 5.0 IP** | **MISS** | Soft+BAL UNDER_OK without GB/FLY — spike killed preferred multis |
| **Gasser U6.5** (UNDER_OK) | **3 K / 4.7 IP** | **HIT** | FLY + contact-heavy confirm held |
| **Pfaadt U6.5** (UNDER_OK) | **2 K / 7.0 IP** | **HIT** | GB + contact-heavy + length |
| **Kirby U6.5** (prior most of day) | **1 K / 4.0 IP** | would HIT | Short outing; under still cashed |
| Alvarez / Liberatore thin O3.5 | 2 / 3 K | **MISS** | ELITE/**BAL**/medium — THIN_TOTAL caution was right; even O3.5 failed |

### Pattern
1. **Trust-the-board (8/7) validated** — WHIFF clears Sale/Williams/Burns/deGrom all cashed soft O4.5+. Style bucket: **whiff 6.12→8.14** vs **balanced 4.44→4.06**.
2. **Preferred multi died on Nola** — Burns/Williams overs were right; UNDER_OK without GB/FLY (soft+BAL+contact-heavy only) spiked. Gasser/Pfaadt were the safer under legs.
3. **ELITE+BAL ≠ ELITE+WHIFF** — Alvarez 2 / Liberatore 3 with length still there = script collapse on BIP styles, not hooks.
4. **Jump 11 K** (ELITE/WHIFF/medium) — medium short-IP lean can still spike; floor O3.5 was process-correct sizing, not a veto on the side.
5. **Cole 9 K** as AVG/WHIFF pass — left money, but early OFF contact-heavy read correctly blocked him as Tier 1 co-anchor.

### Process updates from 8/8
- Prefer UNDER_OK legs that include **GB/FLY style** (Gasser/Pfaadt), not only contact-heavy + low Exp on **BAL** soft (Nola).
- Keep pairing board-clear WHIFF overs; do not sole-nuke three-true anchors.
- ELITE/STRONG + **BAL** → pass juiced totals; O3.5 still optional only — tonight even that missed.
- WHIFF board clears with clear/low risk remain the primary over edge.

## 2026-08-07 grade — what went wrong

Full slate in `backtest-2026-08-07.csv` (n=30, mean Exp K 4.43 → act 4.60, bias +0.17).

### Anchor miss
| Leg | Actual | Result | Break |
|-----|--------|--------|-------|
| **Eovaldi oK** (process Tier 1 — ELITE+WHIFF+TRUST+Strike%67+stuff bump · Exp **6.40**) | **2 K / 5.1 IP / 22 BF / 16 outs** | **MISS** (O5.5 & O6.5) | **Script collapse**, not length — stayed deep enough (outs chalk would cash) but K% cratered (~9% vs 25.5% arsenal). Medium risk + three-true BAL were the pre-flagged flaws; still fired as sole Tier 1. |
| Messick O4.5 / O5.5 | **8 K / 7.0 IP** | **HIT** | Soft Zone% caution was real but arm cleared |
| Cavalli / Fried O2.5 (promo chalk) | 8 / 7 K | **HIT** | Promo floor worked |
| Gausman O4.5 promo | **4 K / 7.0 IP** | **MISS** | Thin AVG/BAL chalk — need 5, got 4 |
| Montero U6.5 (UNDER_OK late OFF) | **5 K** | **HIT** | Soft under lane OK when chip live |
| Tolle O5.5 promo (we said pass anchor) | **14 K** | would HIT | SPIKE ceiling warning was the right read on upside |

### Pattern
1. **The model already printed the cash ticket** — Messick (#2 STRONG/WHIFF/clear Exp ~5.74 → 8), Cavalli (AVG/WHIFF floor → 8), Tolle (SOFT+SPIKE ceiling → 14). We demoted them under Eovaldi’s “perfect” attack-plate pack. Soft Zone% / AVG / SOFT labels were *sizing notes*, not vetoes — and we treated them like vetoes.
2. **Attack-plate pack ≠ immune** — Eovaldi had every confirm and still posted a 2-K night. Size / don’t nuke the whole ticket on one “perfect” stack; medium + three-true on the anchor is a real haircut.
3. **ELITE solo group failed as a bucket** (n=5, 5.44→3.60): Eovaldi 2, Mlodzinski 1 (3 IP hook), Blanco 1 — while Mahle 9 / Sasaki 5. Elite mix still needs length + non-collapse.
4. **SOFT SPIKE lane did its job** — Tolle 14, Rasmussen 8, Gilbert 6, Wheeler 6: no soft U6 was correct; soft≠locked under. SPIKE also means **promo over is live** as a secondary leg — don’t only use SPIKE as an under veto.
5. **Kelly OFF flip AVG/FILLER** before late tickets saved a bad under; Montero UNDER_OK was the live under.
6. **Outs pause stayed right for process** even though Eovaldi O12.5 outs promo would have cashed — don’t reopen outs on one chalk night.

### Process updates from 8/7
- **Trust the board first.** When the model stacks **STRONG/ELITE + WHIFF + clear/low + Exp K ≥ ~5.5** in the top ranks, that *is* a ticket lean — do not demote it to “Tier 2 soft” because Zone% is a hair soft or Strike% is 64 instead of 65. Attack-plate (Strike%≥65 / Zone%≥43 / stuff bump) is a **boost**, not a monopoly that erases everyone else.
- Build the multi from **what the board already cleared** (Messick-type) + **independent chalk the model supports** (Cavalli O2.5 / SPIKE promo floors). Never let one attack-plate arm be the only lean.
- When Tier 1 has **medium risk or three-true/elevated BB**, prefer **smaller K number** (O4.5/O5.5) or pair with those board clears — same rule, sharper reason.
- Promo **O4.5 on AVG/BAL** (Gausman) = filler only; promo **O2.5 on AVG/WHIFF** (Cavalli) = fine chalk leg.
- Keep SPIKE veto on soft unders; also allow SPIKE as **secondary over chalk** when Exp K / line edge is there. Keep UNDER_OK gate for unders.

## Outs tickets — PAUSED (8/6)

**Step away from pitcher outs tickets for now.** 8/6 full-outing outs overs missed back-to-back (Young O14.5→13, Peterson O16.5→15) on “low risk” length with thin cushions.

| Do | Don’t |
|----|--------|
| **K lane only** for real tickets (attack-plate overs · UNDER_OK unders) | Full-outing outs overs (O14.5 / O15.5 / O16.5 style) |
| Honor already-live chalk (e.g. Buehler O0.5) — don’t add new outs legs | Glue K promos to thin outs “anchors” |
| Keep outs efficiency notes for a later revisit | Force dual-lane tickets tonight |

Board can still *show* IP / STYLE for context. **Do not recommend new outs overs/unders** until we explicitly reopen the lane after more graded evidence.

## Product thesis (locked) — why can this pitcher get X strikeouts?

This is the main course. Book lines are the comparison surface; **understanding the path to X Ks** is the point.

1. **Books are usually sharper on public info.** Fat `k_edge` is a *question* (“why is the number there?”), not a ticket. Model edge ≠ true edge.
2. **Strikeouts are PA interactions**, not pitcher season K%. A 28% K arm vs 26–30% K hitters is a different game than the same arm vs 14–17% contact bats.
3. **Split the problem:**
   - **Rate** — K probability per PA (pitcher mix × hitter tendencies / this lineup)
   - **Volume** — batters faced / IP / pitch-count / traffic (how much of the nine he actually sees)
4. **Build a distribution, not only a mean.** Two arms can both Exp ~6 with very different shapes (tight 5–7 vs heavy right tail to 9–10). Prop betting cares about that shape (`k_p10`/`k_p90`, `k_p_ge_9`, `k_p_over` vs the book line).
5. **When odds are live:** compare Line ↔ Exp ↔ P(over) ↔ distribution shape, then write the plain-language *why* (lineup K environment + volume + confirms). Do not stop at “pitcher K% vs line.”

Board fields: `expected_k_pct` + `projected_bf` / `expected_ks_rate_x_bf`, `k_p10`–`k_p90`, `k_dist_shape`, `k_p_over`, `book_model_note`.

## Every morning routine (do this first)

Run this **every morning** before tickets. Goal: one clear outlook for **every** probable starter — **and** an honest read of why the book posted that K line / why the pitcher can reach X Ks.

**Mindset (locked 8/12):** Sportsbooks price information we do not fully see (role, pitch-count plan, platoon construction, market demand, injury whispers). **Model edge ≠ true edge.** A fat `k_edge` is a *question*, not a ticket. Bradford 8/11: TRUST/ELITE stack died because **Stuff+ 86** + Angels’ RHB-heavy / vs-LHP profile were the real story — details > Exp K.

1. **Refresh the board** (probable starters + live odds):
   ```bash
   export ODDS_API_KEY="…"   # or THE_ODDS_API_KEY / Actions secret
   TZ=America/Chicago python3 mlb-k-matchups/k_matchups.py \
     --date YYYY-MM-DD \
     -o rankings-YYYY-MM-DD.csv \
     --html rankings.html \
     --hits-output hits-YYYY-MM-DD.csv -v
   ```
   Odds join is display-only (`k_line` / `k_edge` = Exp K − line). Missing key → board still publishes without lines.
2. **Publish** CSV + `rankings.html` / `index.html` + hits CSV. Note lineup status (`prior` vs `official`).
   - Prefer the **current-branch / SHA htmlpreview** while iterating; `main` only after merge.
3. **Deliver the morning pack** in this exact shape (book-aware, every arm):

### Morning pack shape (locked)

**A. Slate status** — n starters · OFF vs PRIOR · odds coverage · games still without a K line.

**B. Book vs model map** — sort by `|k_edge|` and flag (always with P(over) + shape when present):
| Flag | Meaning |
|------|---------|
| Book **low** (edge ≥ ~+1.0) | Model likes overs more than the number — ask *why the book is soft* (role, Stuff+, platoon, name discount) before juicing |
| Book **high** (edge ≤ ~−1.0) | Name/SPIKE premium — Cam-rule under only if arsenal allows; never soft-under SPIKE |
| Line ≈ Exp | Aligned — size with STYLE / IP / confirms / **distribution shape**, not “edge” |
| Heavy right tail | Same mean, more 9–10 K mass — juiced overs / ceiling legs live; chalk unders fragile |
| Tight band | Mean is the story — size nearer the number; less nuke |
| No line | Short role / not posted — pass full-outing K props |

**C. Every-pitcher info card** (for *your* analysis — not a ticket lock yet). Compact chart + plain-language “why X Ks”:

```
#rk Name (H) TM vs OPP | PRIOR/OFF | role | time
Line O/U X.5 (book · O/U prices) · Exp K · edge · P(over) · P10–P90
| Solo | STYLE | SPIKE/outlook | Stuff+ | Loc+ | IP | BF | risk |
| Lineup K env (vs hand) | BIP/contact | rate×BF vs Exp |
| K9/L3 | SwStr/CSW | Strike%/Zone% | FIP/xFIP/SIERA/xERA | xwOBA/xBA |
Book why: …
Why X Ks: (PA matchups — which bats/pitches) + (volume — IP/BF/leash) …
Model read: …
Watch flags: Stuff+<95 · Loc+<95 · RHB-heavy vs LHP · tough-vs-hand K% · short IP · swingman …
```

**Bradford-rule watch flags (confirm/disprove juice):**
- **Stuff+ &lt; ~95** undercuts WHIFF/TRUST even on ELITE solo
- **Loc+ &lt; ~95** + elev BB9 → short outing / walk script
- **Platoon / hand construction** — LHP vs RHB-heavy nine that hits LHP well (use opp K% vs hand + lineup names)
- **Book disagreeing hard with Exp** — resolve the disagreement before sizing

**D. Bucket leans (provisional until OFF):** Over / Under / Fade-thin — each with the *book why* attached. No ticket lock on PRIOR alone except tiny promo chalk.

3b. **Info lean (default on every arm — not a full essay):** stack signals so outs-type is visible at a glance:
   - **Book line + k_edge** → what is priced? does the number fight our stack?
   - **Solo grade** → can the mix K *this* nine?
   - **STYLE** (WHIFF / GB / FLY / BAL) → does he usually get outs via Ks or BIP?
   - **Opp BIP / contact** (whiff_prone / neutral / contact_heavy) → will the nine help or fight Ks?
   - **Opp offense quality** (lineup PA-weighted **wOBA / wRC+ / ISO**) → soft/avg/good offense for **length/leash** (lower = longer leash OK; higher = size down overs). Confirm only — does **not** flip solo grade. Pitch-type vulnerability stays on **Arsenal lineup K%**, not per-pitch wOBA.
   - **Opp K% vs hand** (vs LHP / vs RHP matching the starter) → primary opp-K confirm; overall opp K% is secondary
   - **Stuff+ / Loc+ / Pit+** → quality red flags (Bradford rule)
   - **Strike% / Zone% / Z-Contact% / O-Swing%** (optional confirm) → does he attack the plate / induce chase / miss in-zone? High Strike% (≥~65) + Zone% supports WHIFF overs; O-Swing% confirms chase; low Strike% alone does **not** lock an under (SPIKE can still clear).
   - **L3 K/9 adj** → recent form scaled by opponent-team K% faced (juiced L3 opps haircut hot form; soft-K L3 opps boost it). Use adj for sizing, raw L3 for SPIKE ceiling.

   One-glance combos: ELITE+WHIFF+whiff-prone = strong K info · ELITE+FLY/GB = matchup OK, don’t overweight K total · SOFT+GB/FLY+contact_heavy = strong under info · SOFT+WHIFF/SPIKE = soft grade but K ceiling live · AVG+WHIFF+juiced line = Cam-rule under info · WHIFF+Strike%≥65 = command confirms the K script · soft offense (low wRC+) + WHIFF + clear IP = length confirms the over · **ELITE+WHIFF but Stuff+&lt;95 = size down / don’t TRUST-hammer**.

3c. **Full thesis / essay (on request only):** when asked for a specific pitcher (or a short list), expand to Littell/Skubal depth — table of arsenal / opp BIP / STYLE / stuff·SPIKE / IP·risk / **book line why**, then answer “can we trust the K total?” and line-sizing. Do **not** essay the whole slate unless asked — the morning pack’s per-arm chart already covers the slate. Same daily routine, deeper read on demand.

3d. **Full-metric slate essay (locked process — OFF confirm + when asked “what stands out”):**
   When official lineups post (or when asked for a full-metric pass), re-run the board and deliver **this exact shape** — not the short morning lean alone:
   1. **Slate status** — n starters · official vs prior count · games still on prior · **odds coverage**.
   2. **Prior → OFF callouts** — which arms flipped, any starter/role change, BIP/K%/wRC+ moves that change the lean · **line moves**.
   3. **Every-metric scan** per notable arm: solo · STYLE · stuff/SPIKE · SwStr/Contact/Z-Contact · Strike%/Zone%/O-Swing · Soft% · K9/L3 · BB9/xFIP/IP/risk · opp K%/BIP/BB% · **opp wOBA/wRC+/ISO** · TRUST/UNDER_OK/FILLER/SPIKE · **k_line/k_edge/book why** · **plus advanced confirm layer below**.
   4. **What stands out** — TRUST stacks, ceiling/SPIKE traps, dead-matchup elite miss, attack-plate without WHIFF, thin under lane, **book-vs-model disagreements**, pass/trap names.
   5. **Ticket lean table** — Tier 1 / co-anchor / ceiling / pass juiced / FILLER / no soft U6, with the metric + book-why reason on each.
   Explain **pitcher + opposing lineup** expectations in plain language (what the prior/OFF nine implies for Ks and leash). Better explained → clearer ticket.

3e. **Advanced confirm / disprove layer (locked — use on every pitcher essay from 8/11 onward):**
   After the core stack (solo → STYLE → SPIKE → Rates → opp leash), run these **confirm-only** checks. They never flip solo alone; they **size** the lean or veto juice.

   | Bucket | Metrics | Confirms lean when… | Disproves / caps lean when… |
   |--------|---------|---------------------|-----------------------------|
   | ERA estimators | FIP · xFIP · SIERA · xERA | All ≤~3.9 and aligned with WHIFF/TRUST | Elev (≥4.3) on a juiced over; SIERA≫FIP without GB/FLY story |
   | Expected contact | xwOBA · xBA · xSLG allowed | Low xwOBA (≲.300) / soft xSLG → leash OK | High xwOBA/xSLG → HR/BIP risk even with Ks |
   | Stuff quality | Stuff+ · Loc+ · Pit+ (100=avg) | Stuff+ ≥105 + Loc+ ≥100 supports TRUST/SPIKE | Soft Stuff+ (&lt;95) undercuts WHIFF story; high Stuff+ + soft Loc+ = BB/short-outing risk |
   | Arsenal weapons | Pitch Stuff+ · RV/100 | Best pitches are +RV and match lineup K holes | Featured pitch is −RV/100 (liability); weapons don’t overlap opp whiff |
   | Book line | k_line · k_edge · role news | Line agrees with stack (±0.5) | Fat edge unexplained = investigate before firing |

   **Essay line required:** one short “Confirms / Disproves” blurb using these metrics before the ticket call.
   Prior-lineup reviews use the same shape — label **PRIOR** and re-check on OFF.

4. **Re-refresh when lineups confirm** — same report shape **plus** the full-metric essay in **3d**; flip prior→official; re-check leans **and lines** before locking tickets.
5. **Accuracy lock before firing** — official nine in, starter not opener, side matches arsenal vulnerability, line edge still holds, **Stuff+/platoon watch flags cleared**, book-why resolved.

This morning pack is the daily starting point — not optional.

## How to read the board on your own (60-second card)

Open a pitcher card and answer **four questions in order**. Do not start at Exp K.

| Step | Look at | Question | What it decides |
|------|---------|----------|-----------------|
| 1 | **ELITE / STRONG / AVG / SOFT** chip | Can his mix K *this* nine? | **Side** (over vs under bias) |
| 2 | **STYLE** chip (WHIFF / GB / FLY / BAL) next to name | Does he get outs via Ks or BIP? | Whether to **trust the total** |
| 3 | **Opp BIP** (whiff_prone / contact_heavy in meta) | Will the nine help or fight Ks? | Confirmation / line size |
| 3b | **Opp wOBA / wRC+ / ISO** | Soft / avg / good offense? | **Length / leash** confirm — not a side flip |
| 4 | **SPIKE / THIN_TOTAL / UNDER_OK / MATCHUP_OK / FILLER** | Any veto or size cap? | Ticket legality |
| 5 | **Strike% / Zone% / Z-Contact%** (Rates row) | Does he attack the plate / miss in-zone? | Command confirm — **not** a side flip |

**One-glance recipes**

| Stack | Read | Ticket move |
|-------|------|-------------|
| ELITE/STRONG + **WHIFF** + Exp K ≥5.5 | **Trust total** | Soft O4.5 / O5.5 OK if IP clear |
| ELITE/STRONG + **WHIFF** + Strike% ≥~65 | Attack-plate confirm | Size up over confidence if IP clear |
| ELITE/STRONG + **GB/FLY** + Exp K ≥5.5 | **THIN_TOTAL** | O3.5 / thin O4.5 only |
| ELITE/STRONG + **BAL** + Exp K ≥5.5 | Total caution | Prefer O4.5 floor; don’t juice O6.5 |
| SOFT + **UNDER_OK** (2+ confirms) | Preferred under | Soft U6 / BIP under |
| SOFT + SPIKE / WHIFF | Ceiling live | No soft U6; Cam U7+ or pass |
| MATCHUP_OK | Soft profile + good mix | Thin O3.5 only — never nuke |
| FILLER / opener | Bad K fit or short role | Pass K overs; outs alt maybe |

Also check: **Official** vs Prior · projected IP · outing risk · vs-team history (confirm only).

## Ticket lock routine (USE THIS before every card)

**User-locked 8/5–8/6.** Run this full path before recommending or firing any over/under. Exp K and slate `#` come last. Goal = find edge or pass.

### Step 0 — Setup
1. Refresh board; hard-refresh the link.
2. Filter **Official only** (prior = scouting only — do not lock).
3. Skip **openers / swingmen / unscored**.
4. Note the book line for that pitcher.

### Step 1 — Solo arsenal (picks the side)
| Grade | Edge bias |
|-------|-----------|
| ELITE / STRONG | **Over** |
| SOFT | **Under** |
| AVG | Usually pass / Cam-rule only |

This is the edge. Everything else confirms or sizes it.

### Step 2 — STYLE (trust the total?)
| STYLE | Meaning |
|-------|---------|
| **WHIFF** | Outs via Ks → juiced totals OK |
| **GB / FLY** | BIP outs → **THIN_TOTAL** (O3.5 / thin O4.5 only) |
| **BAL** | Caution — don’t juice O6.5 |

Good mix + wrong style ≠ nuke over.

### Step 3 — Opp BIP / K%
| Opp look | Helps |
|----------|-------|
| **whiff_prone** (BIP ≤~64%) | Overs |
| **contact_heavy** (BIP ≥~71%) | Unders |
| **neutral** | No extra edge |

Confirm only — does not flip solo grade alone.

### Step 4 — Outlook chip (legal / illegal)
| Chip | Move |
|------|------|
| **TRUST** | Over live if IP clear |
| **THIN_TOTAL** | Thin over only — not a nuke |
| **UNDER_OK** | Preferred soft under |
| **SPIKE** | **No soft U6** |
| **MATCHUP_OK** | O3.5 / thin O4.5 only |
| **FILLER** | Pass K overs **and** soft unders |

If the chip vetoes → stop.

### Step 5 — Strike% / Zone% (command + outs efficiency)
Compare Rates row to slate **Avg Strike%** (~64%).
| Read | Use |
|------|-----|
| Strike% **≥~65** + WHIFF/TRUST | Size **up** K-over confidence |
| High Zone% + high Strike% | Attacks the plate — K script more live; **outs overs OK** |
| Zone% **&lt;~40–41** (soft / nibble) | **Outs over caution** — pitches burn without banking outs |
| Zone% **≥~43** + clear/low risk | Outs over efficiency confirm |
| Low Strike% + UNDER_OK stack | Soft K under OK |
| Low Strike% + SPIKE/WHIFF | **Do not** auto K-under |

**Outs efficiency (8/6 Young + Peterson — always apply on outs O/U):**
- Soft Zone% + high pitches-per-out → shortens outs even when outing risk reads “low” (Young **13 outs / 98 pitches** vs ~17 proj).
- **Outs over:** prefer GB length; on FLY/THIN_TOTAL require Zone% ≥~43 **or** ≥~3 outs of cushion vs line. Pass thin FLY O14.5-type spots when Zone% is soft.
- **Cushion / recent form (Peterson):** if `short_recent_ip`, elev_bb, or Zone% ≲42, demand ~**2+ outs** of cushion vs the line. ~17.3 proj vs O16.5 (= ~0.8 edge) is **too thin** — he finished **15 outs / 5.0 IP**. Weight **L3 IP**, not only season proj.
- **Outs under:** soft Zone% / medium-high risk / short recent IP **helps** the under (inefficiency = fewer outs). Still need line cushion; don’t fade chalk O0.5–O2.5 promos.
- Promo chalk (O0.5 / O2.5 outs) = length not required — separate from full-outing outs overs.

Command confirms the script. It does **not** create the K side.

### Step 6 — Length & risk
- Projected IP supports the line?
- Outing risk / early-exit flags?
- Exp K / proj outs vs line still has edge?
- **Cam rule:** name/SPIKE juiced ~1.0–1.5 above Exp K → under can be live on AVG/SOFT.

Short IP kills TRUST K overs and full-outing outs overs.

### Step 7 — Pre-ticket checklist (all must pass — read before every fire)
Use this as the comfort gate. If any box fails → **no ticket**.

**Setup**
- [ ] Board refreshed; line confirmed
- [ ] **Official** nine (promo chalk O0.5 OK on prior only if starter confirmed)
- [ ] **Starter** (not opener / swingman)

**Side / lane**
- [ ] Solo grade picks the K side (ELITE/STRONG over · SOFT under · AVG usually pass)
- [ ] Chip does not veto (TRUST / THIN / UNDER_OK / SPIKE / MATCHUP_OK / FILLER)
- [ ] Lane chosen: **Ks** or **outs** (not forcing the wrong prop)

**Confirms**
- [ ] STYLE fits the total (WHIFF→K juice OK · GB/FLY→thin K / outs lane)
- [ ] Opp BIP agrees enough (whiff_prone helps K overs · contact_heavy helps unders)
- [ ] Strike% / **Zone% efficiency** checked (soft Zone% → caution outs *overs*; can help outs *unders*)
- [ ] IP / risk / proj outs support the **posted line** (cushion holds)

**Card rules**
- [ ] Default **2-leg**; no same-game opposing K overs
- [ ] Arm on ≤2 tickets today; one nuke/chalk pair max
- [ ] Comfortable saying the lean in one sentence — if not, pass

### Where the edge is
- **K over edge:** OFF + ELITE/STRONG + WHIFF + (TRUST or clear IP) + (whiff_prone **or** Strike% ≥~65)
- **Attack-plate over pack (8/5 locked):** prefer arms that stack **ELITE/STRONG + WHIFF + Strike% ≥~65 / Zone% ≥~43** (Harrison 10, Rogers 9, Lopez 9, Skenes 6). Length still required (Detmers attack profile but 5 K / 4 IP). Skip THIN_TOTAL / MATCHUP_OK / BAL as nuke K overs even if Exp K is high.
- **K under edge:** OFF + SOFT + UNDER_OK (≥2 of GB/FLY · contact_heavy · Exp K ≤~4.2) + not SPIKE · line needs real cushion (pass flat U4.0 when Exp ~3.5)
- **Outs over edge (co-equal lane — 8/6 locked):** OFF + starter + projected IP holds (~≥5.5 → ~16.5+ outs) + outing risk **clear/low** + STYLE **GB/FLY** (or THIN_TOTAL / MATCHUP_OK / FILLER where Ks are the wrong prop) + **Zone% efficiency** (see Step 5). Length is the product — high risk / short IP / openers / soft-Zone% FLY = pass full-outing outs overs.
- **Outs under edge:** short/high-risk or soft Zone% inefficiency + line cushion; not vs chalk promos.
- **No edge (pass):** AVG mush on Ks · THIN_TOTAL *K nukes* · FILLER K overs · openers · SPIKE soft U6 · prior lineups (except tiny promo chalk) · outs overs on high-risk hooks · thin FLY outs overs with soft Zone%

### Dual ticket lanes (Ks **or** outs)
Every probable gets both reads. Chip decides the lane:
| Chip / stack | K ticket | Outs ticket |
|--------------|----------|-------------|
| TRUST / attack-plate WHIFF | **K over** | usually pass (Ks are the product) |
| THIN_TOTAL / FLY or GB + length + Zone% OK | thin K only | **outs over** preferred |
| THIN_TOTAL / FLY + soft Zone% | thin K only | **pass** thin outs over (Young) |
| MATCHUP_OK / FILLER + clear-low IP + Zone% OK | pass / O3.5 K | **outs over** if IP holds |
| UNDER_OK | **K under** (line cushion) | outs under if short/high-risk or soft Zone% |
| SPIKE soft solo | no soft K under | outs OK if length + efficiency clear |
| Promo chalk O0.5 outs | — | **fire** if he starts (pair with real leg) |

Pair across lanes freely (e.g. Ashcraft K over + Peterson outs over). Still default **2-leg**; no same-game opposing *K* overs.

### Fast edge test
> Solo says over or under → does STYLE allow that total → Ks or outs lane? → Zone% efficiency OK for outs? → does BIP agree → does the chip allow the ticket → does Strike%/IP support it?

Any **no** → **no edge** → pass.

### 8/5 attack-plate pack (remember for future cards)
User target overs that fit the new lens: **Harrison / Rogers / Detmers / Skenes / Lopez**.
Actuals: 10 / 9 / 5 / 6 / 9. Four clear cashes on soft O4.5+; Detmers only if line ≤4.5 (short IP). Use attack-plate as a **confidence boost** on next slates — not as a filter that drops STRONG/WHIFF/clear board answers (8/7 Messick lesson).

## Better tickets (habit)

1. **Default = 2-leg.** K over + K under, or two K overs / two UNDER_OK. **No new outs legs while outs lane is paused (8/6).** No 6-legs.
2. **Read the model answers, then size.** Start from board clears: solo grade + STYLE + outing risk + Exp K + outlook chip. Top of board ≠ auto-bet when the chip says THIN/FILLER (Dobbins) — but when chips **agree** with a top rank (Messick STRONG/WHIFF/clear), **take that lean**. Do not invent extra vetoes (soft Zone% alone, missing stuff bump) that demote a clear model answer under one prettier attack-plate stack.
3. **Attack-plate is a boost, not the only door.** Pair board clears with independent chalk; never sole-nuke a medium/three-true “perfect” arm.
4. **Pair opposite K scripts:** TRUST / board-clear over + UNDER_OK under. Avoid same-game opposing K overs.
5. **Line sizing:** K overs need IP + trust; K unders need confirms or U6.5+. Cam rule: if book juices name/SPIKE above Exp K by ~1.0–1.5 on AVG/SOFT, K under is live. SPIKE promo overs OK as secondary legs.
6. **Accuracy lock:** run the **Ticket lock routine** above — do not skip steps.
7. **Cap:** any arm on ≤2 tickets; one nuke/chalk pair max per day.

## Core thesis — pitcher vs batter vulnerability first

**Primary edge = solo arsenal vs this nine** — absolute `expected_k_pct` and **`arsenal_abs_grade`** (ELITE / STRONG / AVG / SOFT).  
That grade is banded on the pitcher’s arsenal-weighted K% vs *this* lineup and **does not move** when other starters are added/removed from the slate.

| Absolute arsenal K% vs lineup | Solo grade | Lean |
|------------------------------|------------|------|
| **≥ 24.0%** | **ELITE** | **OVER** bias |
| **≥ 22.5%** (league K%) | **STRONG** | **OVER** lean |
| **≥ 20.0%** | **AVG** | Neutral / need more |
| **&lt; 20.0%** | **SOFT** | **UNDER** bias |

Also check edges on the card: **vs league** (`expected_k_pct − 22.5`) and **vs opp K%** (mix beats/lags the lineup’s raw K tendency).

**Stuff ceiling (velo/whiff by pitch)** — separate from solo grade. Usage-weighted pitcher-own whiff% + primary FB velo → `stuff_grade` / **SPIKE** chip. Soft solo **+ SPIKE** = do **not** auto-under (U6.5+ or pass). Does not move Exp K.

**Advanced confirm layer (FIP / SIERA / xStats / Stuff+ / pitch RV) — display only:**
- **FIP · xFIP · SIERA · xERA** on Rates — ERA estimators; SIERA credits GB/popup weak contact. Lower better. Confirm length / soft-contact / luck — **does not flip** solo or Exp K.
- **xwOBA / xBA / xSLG allowed** (Savant) — contact quality allowed; lower = better suppression / sustainable profile.
- **Stuff+ · Loc+ · Pit+** (FanGraphs, 100 = avg) — true pitch quality next to the whiff/velo SPIKE proxy.
- **Arsenal RV/100 + pitch Stuff+** — FanGraphs pitch run value (positive = prevents runs) and per-pitch Stuff+. Use to see which pitch is carrying the arsenal; confirm-only.

**Lineup contact / BIP** — opposing nine’s balls-in-play rate (`lineup_bip_pct`) + `contact_grade` (`whiff_prone` / `neutral` / `contact_heavy`). Contact-heavy BIP trims Exp K; whiff-prone (high K% / low BIP) boosts it. Secondary to solo arsenal grade — sizes the number, doesn’t flip the side.

**Pitcher style (Ks vs BIP outs)** — season FanGraphs K%/Contact%/GB%/FB%/IFFB → `pitcher_style` chips (`P-WHIFF` / `P-GB` / `P-FLY` / `P-BAL`). Confirmation only (no Exp K move). WHIFF confirms overs / SPIKE caution on soft unders; GB/FLY = outs via contact — soft matchup strengthens under; don’t force huge overs on elite mix + contact style without length.

**Total-trust gate (THIN_TOTAL) — added after 8/4:** ELITE/STRONG with Exp K ≥ ~**5.5** only **fully trusts** the juiced total when STYLE is **WHIFF**. STYLE **GB/FLY** → board outlook **THIN_TOTAL** (O3.5 / thin O4.5 only — Dobbins 7.7→4). STYLE **BAL** → soft “total caution” note (prefer O4.5 floor; Manaea 6.8→7 still OK). Mix side can still be a thin over; the *total* is the leak on BIP-out styles.

**Under confirmation (UNDER_OK) — added after 8/4:** SOFT non-SPIKE needs ≥**2 of 3**: GB/FLY style · opp **contact_heavy** BIP · Exp K ≤ ~**4.2**. Passes → **UNDER_OK**. Fewer → weak under (prefer U6.5+ or pass). SPIKE still vetoes soft U6. Best 8/4 lane: Dobnak/Assad (SOFT+GB+contact-heavy).

**Secondary only:** slate `#` / slate `matchup_grade` / opp lineup K% `#` — “who’s best *today*,” not solo quality.  
Exp K and projected IP size the outing; they do not define the side.

| Solo grade (absolute) | Lean | Why |
|-----------------------|------|-----|
| **ELITE / STRONG** | **OVER** bias | Bats are vulnerable to *this* mix even if Exp K looks soft |
| **SOFT** | **UNDER** bias | Weak pitcher-vs-batter fit caps conversion — soft U6.5+ is live |
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
- **OVER gate — solo arsenal must be ELITE/STRONG:** fire pitcher K overs when absolute arsenal vs that nine is **ELITE (≥24% K) or STRONG (≥22.5%)**. Thesis: good pitcher-vs-batter fit can push a pitcher **over his projection / O/U line** even when Exp K looks modest. AVG solo grade → no ticket over (O3.5 floor max). Exp K, IP, and slate `#` are secondary.
- **UNDER gate — SOFT solo arsenal is the edge:** when absolute arsenal vs that nine is **SOFT (&lt;20% K)**, lean **unders** (esp. soft **U6.5 / U7.5**) even if opp lineup K% ranks high or Exp K sits near 5–6. McLean proved high opp K% ≠ over juice when the mix is soft vs that nine. Still: **no soft unders on SPIKE arms (K9 ≥ ~10)**; prefer wide edge under the line.
- Prefer **soft U6.5 / U7.5** with wide edge when arsenal is soft; **U5.5** OK if non-SPIKE and edge holds.
- **Fade unders on SPIKE arms (K9 ≥ ~10)** — they can jump a soft under even when proj is mid / arsenal looks soft.
- **Good-pitcher unders (line vs Exp K) — Cam rule:** books often set lines off **name / K9 / SPIKE ceiling**, not arsenal vs *this* nine. Edge = **Exp K well under the posted line** even on WHIFF/SPIKE arms.
  1. Exp K (fair) vs book line (ask) — want ~**1.0–1.5+ K** of cushion for unders.
  2. Solo grade **SOFT or AVG** vs that nine (ELITE/STRONG → not an under).
  3. STYLE/SPIKE size the *line*, not the side: **SOFT+SPIKE+WHIFF** → only **wide** unders (Cam U7 with Exp K ~5.4); non-SPIKE soft/avg → U6.5 OK if edge holds.
  4. Opp **contact_heavy** BIP strengthens the under; whiff-prone opp fights it (need extra line cushion).
  - **Cam 8/3:** Exp K ~5.4, STYLE WHIFF + SPIKE, book **7** → U7 edge; actual **6** in 3 IP cashed.
  - **Javier 8/3:** Exp K ~2.9, SOFT + TOR contact_heavy → under vs juiced name line; actual **2**.
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

## 2026-08-06 early lessons (n=14 Final; 8 still live — full grade later)

MAE ~**1.92**, bias **+0.34** (model slightly under). WHIFF arms ran hot; FLY/THIN K totals stayed soft.

### Ticket scorecard (early)

| Ticket | Result | Note |
|--------|--------|------|
| Young O14.5 outs + Ashcraft O4.5 K | **MISS** | Ashcraft **5 K HIT**; Young **13 outs** killed it |
| Ashcraft O2.5 promo + Peterson O16.5 outs | **MISS** | Ashcraft **5 K HIT**; Peterson **15 outs** |
| Buehler O0.5 outs + Miller O3.5 K | **on track** | Miller **5 K HIT**; Buehler **2 outs** (live chalk) |

### What worked (keep)
1. **K lane > outs lane** — every Ashcraft/Miller K leg cashed; both full-outing outs overs missed.
2. **SPIKE veto** — McLean **8**, Sánchez **6**. Never soft-under those.
3. **UNDER_OK** — Johnson **1**, Mikolas **1**.
4. **THIN_TOTAL / MATCHUP_OK as K fade** — Young **4 K**, Abbott **4 K** (not nuke overs).
5. **Attack-plate sizing** — Ashcraft/Miller O4.5 / O3.5 OK; do **not** juice Ashcraft to O5.5 (exactly 5).
6. **Soft Zone% ≠ auto under** — Cease Z% 36 → **10 K**.

### What failed (fix)
1. **Full-outing outs overs** — Young/Peterson. “Low risk” + season IP proj lied; soft Zone% / `short_recent_ip` were the tells.
2. **Pairing good K chalk with thin outs anchors** — tickets died on the outs leg.
3. **Thin outs cushions** — O16.5 on ~17.3 proj (~0.8 edge) is not enough.

### Improvements locked for next slate
| Change | Rule |
|--------|------|
| **Outs paused** | No new pitcher outs tickets until explicitly reopened |
| **K-only 2-legs** | Attack-plate / TRUST over + UNDER_OK under (or two K overs with real edge) |
| **O5.5 bar** | Need Exp K ≥ ~6.3–6.5 **or** clear TRUST + length — Ashcraft 5.6→5 is the ceiling warning |
| **Checklist first** | Official · solo · chip · STYLE · BIP · Strike%/Zone% · IP/line — pass if any box fails |
| **Vs-hand opp K%** | Use as confirm (now on board); not a side flip alone |
| **SPIKE / UNDER_OK** | Highest-confidence chip lanes today — size tickets from those first |

Full final review + `backtest-2026-08-06.csv` after the last eight finish.

## 2026-08-05 lessons (MAE ~2.21, n=23 Final scored; 6 still live at grade)

First night with **TRUST / UNDER_OK / THIN_TOTAL** + new **Strike%/Zone%** on the board. Model **understated** Ks (bias **+1.01**); whiff_prone nines and several soft/SPIKE arms ran hot.

| Solo grade | n | mean expK → act | Notes |
|------------|---|-----------------|-------|
| **ELITE** | 4 | 5.42 → **7.00** | Harrison **10**, Pérez **9**; Detmers TRUST 5 / 4 IP short; Whisenhunt 4 |
| **STRONG** | 3 | 5.25 → **7.00** | Lopez **9**, Imanaga **6**; Skenes TRUST **6** (nail) |
| **AVG** | 6 | 4.69 → 5.50 | Rogers **9**, Gray **8**, Scott **7**; Lauer FILLER **1** |
| **SOFT** | 10 | 4.21 → 4.90 | Bibee FILLER **10**, Cameron **9**, Brown SPIKE **8**; UNDER_OK lane held |

### Ticket leans (Final)

| Lean | Actual | Result |
|------|--------|--------|
| **TRUST Detmers** | 5 K / 4 IP | Soft miss — mix OK, length died |
| **TRUST Skenes** | **6 K** / 5 IP | **HIT** — chalk trust total |
| **UNDER_OK Sugano / Lowder / Irvin** | 3 / 3 / 3 | **HIT** — all ≤ Exp K, contact-heavy soft |
| **SPIKE Brown** (no soft U6) | **8 K** | Veto **correct** — soft under would have died |
| **SPIKE Burke** | 4 K | Soft side OK; SPIKE still right to block auto-U6 |
| **FILLER Bibee** | **10 K** | Never soft-under FILLER; never K-over anchor |
| **ELITE Harrison** (thin IP ~4.6) | **10 K** / 5 IP | Volume spike — Strike% 66.5 confirmed attack |

### Strike% / Zone% (new layer) — did it help?

Raw corr vs actual Ks was near **zero** alone (Strike% +0.07, Zone% +0.00) — **not a solo predictor**. Useful as **command confirm on WHIFF / over scripts**:

| Stack | Read from 8/5 |
|-------|----------------|
| **WHIFF + Strike% ≥65** | Harrison 10, Detmers 5 (short), Burke 4 — ceiling live when SPIKE/ELITE; length still required |
| **High Strike% + Zone% (attack plate)** | Rogers 68.6/44.4 → **9**; Harrison 66.5/42.8 → **10** — home-plate attack helped K conversion |
| **Low Strike% ≠ auto under** | Brown **59.6** Zone 37.6 → **8** (SPIKE/WHIFF); Lopez **60.3** → **9** |
| **UNDER_OK + low-mid Strike%** | Sugano/Lowder/Irvin ~61–62.5 → all **3 K** — command soft + contact-heavy stacked |

**Process add:** after solo → STYLE → BIP, glance **Strike%/Zone%**. If WHIFF/TRUST over and Strike% ≥ ~65 (slate avg was **64.0%**), trust the K script more. If Strike% is soft, do **not** flip a SPIKE/WHIFF arm to under — use it only to size UNDER_OK / pass juiced overs on nibble arms.

### Reinforced

1. **TRUST** works when IP holds (Skenes); short outing kills Detmers-tier totals.
2. **UNDER_OK** 3/3 — keep as preferred soft-under badge.
3. **SPIKE veto** on Brown saved the soft-under trap.
4. **FILLER can spike** (Bibee 10) — pass both K overs and soft unders.
5. **Strike%/Zone% = confirm, not side** — attack-the-plate helps WHIFF overs; does not invent unders.

## 2026-08-04 lessons (MAE ~1.61, n=24 Final; 6 still live at grade)

Process night for STYLE / BIP / SPIKE. ELITE totals overstated without WHIFF; contact-heavy soft unders were the clean lane.

| Solo grade | n | mean expK → act | Notes |
|------------|---|-----------------|-------|
| **ELITE** | 7 | 5.81 → **4.14** | **−1.66 bias** — Dobbins 7.7→4, Tidwell 6.8→3, Yesavage 0 / 2 IP |
| **STRONG** | 2 | 5.97 → 6.00 | Manaea **7**, Cantillo **5** — held |
| **AVG** | 6 | 4.58 → 5.17 | Henderson **8** SPIKE upside; Ryan soft |
| **SOFT** | 9 | 3.93 → 3.67 | Non-SPIKE under lane OK; Luzardo/Weathers SPIKE cleared 6+ |

| Layer | Signal |
|-------|--------|
| **contact_heavy** (n=4 Final) | mean act **~2.0** — Dobnak 1, Assad 3, Palmquist 0 |
| **whiff_prone** | mixed — Manaea/GRod OK; did **not** save Tidwell total |
| **STYLE WHIFF** | +0.5 bias; **GB** −0.9 (BIP outs) |
| **SOFT+SPIKE** | Luzardo **7**, Weathers **6** — SPIKE veto correct |
| **MATCHUP_OK** | Povich **7** / Tidwell **3** — thin-only rule kept |

### Reinforced / shipped

1. **THIN_TOTAL** — ELITE/STRONG + Exp K ≥5.5 + non-WHIFF → thin overs only (Dobbins/Tidwell).
2. **UNDER_OK** — SOFT non-SPIKE needs ≥2 of GB/FLY · contact-heavy · Exp K ≤4.2 (Dobnak/Assad).
3. SPIKE still blocks soft U6; MATCHUP_OK stays O3.5 / thin O4.5; 2-leg default.
4. Do **not** retune BIP ±7% or move STYLE into Exp K off one night.

### Discussed legs (partial)

| Leg path | Actual | Note |
|----------|--------|------|
| Dobbins high Exp K over | 4 K / 6.1 IP | THIN_TOTAL prototype (ELITE+GB) |
| Cantillo over | 5 K | STRONG+WHIFF floor OK |
| Dobnak under / floor | 1 K | UNDER_OK stack cashed |
| Luzardo soft under | 7 K / 8 IP | SPIKE veto — pass was right |
| Tidwell MATCHUP_OK nuke | 3 K | thin-only validated |
| Singer soft under | 6 K | weak under (no contact-heavy) |

## 2026-08-02 lessons (MAE ~1.94, n=28 starters)

Stronger night for volume overs; soft unders mixed again (Williams 10 spike).

| Solo grade | n | mean expK → act | Notes |
|------------|---|-----------------|-------|
| **ELITE** | 3 | 5.93 → 6.00 | **Burns 9**, Rea 7 (MATCHUP_OK cashed floor+); Keller 2 / 2 IP early hook |
| **STRONG** | 6 | 5.67 → 6.33 | **Misio 10**, Lambert 8, Freeland 8; Wheeler 3 / 2 IP early exit |
| **AVG** | 6 | 4.83 → 4.33 | Mostly quiet; Jax 8 upside |
| **SOFT** | 13 | 4.31 → 4.92 | 9/13 under 6; **Williams 10** and Liberatore/Ureña/Roupp spiked |

### Outlook report card

| Lean | Actual | Result |
|------|--------|--------|
| **O Misiorowski** | 10 K / 7 IP | **HIT** — volume strong/elite path |
| **O Burns** | 9 K / 6 IP | **HIT** — elite mix + length |
| **O Lambert / Freeland** | 8 / 8 | **HIT** — strong solo cashed |
| **O Wheeler** | 3 K / 2 IP | **MISS** — early exit (Completed Early) |
| **O Jump** | 5 K / 3.2 IP | thin / short |
| **U Bradish / Kay / Bennett** | 3 / 3 / 4 | **HIT** soft unders |
| **U Williams** | **10 K** | **MISS** — soft flip spiked (like 8/1 Rasmussen) |
| **U Rocker / Alcantara** | 5 / 5 | pushy vs U6 |

### Reinforced

1. **Volume + STRONG/ELITE + IP** is the over lane (Misio/Burns/Lambert).
2. **Early exits kill overs** even on strong mix (Wheeler, Keller).
3. **SOFT under still not locked** — Williams 10 after soft flip; prefer U6.5+ or low Exp K soft (Bennett/Kay/Bradish worked).
4. **MATCHUP_OK Rea 7** — floor over can cash, still not a nuke anchor thesis.
5. **Hart opener** 2 K / 3 IP — opener fade correct for full-outing overs.

## 2026-08-02 lessons (MAE ~1.98, n=30 modeled; BOS@LAD still In Progress)

Strong/elite overs cashed when they got length; soft unders mixed again — Williams **10** and Liberatore/Ureña/Roupp all cleared 6.

| Solo grade | n | mean expK → act | notes |
|------------|---|-----------------|-------|
| **ELITE** | 3 | 5.93 → 6.00 | Burns **9**, Rea **7**; Keller **2**/2 IP early hook |
| **STRONG** | 7 | 5.02 → 5.71 | Misio **10**, Lambert **8**, Freeland **8**; Wheeler rain short (3/2 IP) |
| **AVG** | 6 | 4.83 → 4.33 | Jax spiked **8**; Kirby/Bradley/Cavalli soft unders vs chalk |
| **SOFT** | 13 | 4.31 → **4.92** | **4/13 ≥6 K** — Williams **10**, Liberatore **7**, Ureña **7**, Roupp **6**; Kay/Bradish/Bennett/Montero under lane OK |

### Report-card style

| Lean type | Result | Note |
|-----------|--------|------|
| **O Misio / Burns / Lambert / Freeland** | 10 / 9 / 8 / 8 | Strong/elite + length — overs cashed |
| **O Wheeler / Keller** | 3 / 2 | Rain / early hook — IP killed overs |
| **O Rea MATCHUP_OK** | 7 K / 6 IP | Soft-contact + elite solo worked with length |
| **U Kay / Bradish / Bennett / Montero** | 3 / 3 / 4 / 2 | Soft under lane held |
| **U Williams (soft)** | **10 K** | Soft spike — never auto-U6 on soft with mid Exp K |
| **U Liberatore / Ureña / Roupp** | 7 / 7 / 6 | Soft cleared 6 again — prefer U6.5+ or low Exp K |

### Reinforced / adjusted

1. **SOFT still not automatic U6** (2nd straight night of spikes after 8/1) — require Exp K ≤ ~4.2 or line U6.5+, else pass.
2. **STRONG/ELITE + clear IP** remains the over path (Misio/Burns/Freeland); rain/early hooks (Wheeler/Keller) still kill.
3. **MATCHUP_OK with length** can cash (Rea 7) — still thin O3.5/O4.5 only without Exp K cushion.
4. **Sheehan / Bennett** still In Progress at grading — treat partial; don’t lock process lessons on unfinished outs.
5. **SPIKE reminder:** Williams soft→10 K — no soft unders on arms that can run K9 ≥ ~10.

## 2026-08-01 lessons (MAE ~2.21, n=23 starters)

Tough night for absolute SOFT unders — several soft-mix arms spiked Ks. Elite overs mostly short-outing misses.

| Solo grade | n | mean expK → act | vs O6 |
|------------|---|-----------------|-------|
| **ELITE** | 6 | 5.64 → 4.33 | 1/6 cleared O6 (Peterson 8); deGrom 3 / 3.1 IP, Abbott 1 |
| **STRONG** | 4 | 4.62 → 3.75 | 0/4 cleared O6 |
| **AVG** | 8 | 4.73 → **5.88** | Sánchez **11**, Mahle **9**, upside again |
| **SOFT** | 5 | 4.46 → **6.20** | **Failed under lane** — Rasmussen 10, Fried 7, Tolle 7, Messick 6; only Buehler 1 |

### Early outlook report card

| Lean | Result | Note |
|------|--------|------|
| **O Peterson** | **8 K** HIT path | Elite + length — only elite O6-style cash |
| **O Ashcraft / Prielipp** | 5 / 5 | Mix OK, no O6 |
| **O deGrom** | 3 K / 3.1 IP | Early hook — SPIKE/elite still needs IP |
| **O Gausman / Abbott** | 4 / 1 | Misses; Abbott high-risk flagged |
| **U Buehler** | **1 K** HIT | Clean soft under |
| **U Tolle / Fried / Messick / Rasmussen** | 7 / 7 / 6 / **10** | Soft solo **spiked** — do not treat soft as locked U6 |

### Reinforced / adjusted

1. **SOFT ≠ automatic under** after 8/1 — demand wider lines (U6.5+) or pass when Exp K ≥ ~5 or K9 is mid/high (Rasmussen/Fried/Tolle).
2. **ELITE still needs outing length** — deGrom 3.1 IP killed the over; prefer clear + IP ≥ ~5.5 for O5.5+.
3. **AVG upside continues** (Sánchez 11, Mahle 9) — not under chalk.
4. **Yamamoto / Baz → AVG fade** was correct vs forcing overs (3 K / 4 K).
5. **Phillips swingman MATCHUP_OK** (3 K) — fade full-outing chalk still right.

## 2026-07-31 lessons (MAE ~1.40, n=27 starters)

Solo absolute grade (`arsenal_abs_grade`) first full graded night.

| Solo grade | n | mean expK → act | vs U/O 6 |
|------------|---|-----------------|----------|
| **ELITE** | 7 | 5.19 → 4.71 | only 1/7 cleared O6; short outings (Skenes 7 K / 4 IP) |
| **STRONG** | 7 | 4.98 → 3.86 | 1/7 cleared O6 — strong ≠ automatic O6 |
| **AVG** | 6 | 4.87 → **6.17** | upside bucket (Warren 7, Cease 7, Wacha 7, Matthews **10**) |
| **SOFT** | 7 | 3.89 → 3.43 | **0/7 cleared O6**; 6/7 ≤5 K — best under lane |

### User ticket (Brown U6 / Eovaldi O6 / Sugano O3.5 / Drohan O6) → **2/4**

| Leg | Actual | Result | Lesson |
|-----|--------|--------|--------|
| **Brown U6** | 5 K / 5.2 IP | **HIT** | SOLO SOFT under with room under 6 — on-model |
| **Eovaldi O6** | 5 K / 5.0 IP | **MISS** | SOLO STRONG but Exp K ~6.1 → O6 is **zero-edge**; need O5.5 or more cushion |
| **Sugano O3.5** | 2 K / 6.2 IP | **MISS** | MATCHUP_OK / soft-contact floor over failed — disclose is not a cash |
| **Drohan O6** | 7 K / 6.0 IP | **HIT** | Cashed, but Friday lock was solo **AVG** (process pass) — result ≠ process proof |

Also: **same-game** Brown U + Eovaldi O (TEX@HOU) — both finished 5 K; correlated script risk.

### Reinforced

1. **SOFT solo = under lane** (esp. U6): 0/7 soft arms reached 6 K.
2. **ELITE/STRONG solo ≠ O6 chalk** — prefer O4.5/O5.5 unless Exp K ≥ ~6.8–7 + length.
3. **MATCHUP_OK O3.5** still fails (Sugano 2) — thin floor, not a 4-leg anchor.
4. **AVG solo overs** can spike (Matthews 10, Warren 7) — don’t treat AVG as under chalk either.
5. **Suarez 2 K** — sheet-green / solo-SOFT under thesis cashed; mix > season form.
6. **Fedde 6 K** — SOFT FILLER still spiked to 6; U6 on soft arms needs the cushion (prefer when Exp K ≤ ~4.5 or line U6.5+).

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

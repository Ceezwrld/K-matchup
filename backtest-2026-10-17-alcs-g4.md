# ALCS G4 grade — TB @ CLE · 2026-10-17 · TB 7, CLE 3

TB wins; series tied **2–2**.  
Pregame: Martinez Exp **3.2** UNDER_OK · Armstrong opener · Griffin LHP bulk live after rainout.  
Cards: `pregame-batter-leans-2026-10-17-alcs-g4-sharpened.md` · visual `pregame-visual-leans-2026-10-17-alcs-g4.md`.  
New layer: season ∩ recent heatmaps + `LOW_SAMPLE_*` flags.

**Context:** Armstrong **1.0 IP** → **Griffin 3.2 IP** (primary bulk) → Espino/Herrin/Cecconi/Festa/Cantillo (Cantillo only **0.2** late — not the length arm). Martinez **5.1 IP / 3 K / W**.

---

## Pitchers

| Arm | Exp / read | Act | Verdict |
|-----|------------|-----|---------|
| **Martinez** | 3.2 · UNDER_OK | **3 K / 5.1 IP** · 2 H · 1 ER · 2 BB · 79p · **W** | **HIT** soft-under path — rate + length both quiet |
| **Armstrong** | opener · pass K | **1 K / 1.0 IP** | **Process OK** — opener script |
| **Griffin** | SPIKE · no soft U | **5 K / 3.2 IP** · 4 H · 1 ER | **SPIKE confirm** — would’ve burned a soft under |
| Cantillo | WHIFF bulk option | **0.2 IP / 1 K** late | Not the bulk test — Griffin ate length |

---

## CLE vs Martinez — batter leans

| Lean | Pregame (sharpened) | Final | Grade |
|------|---------------------|-------|-------|
| **DeLauter Hits / HRR** | #1 · CONFIRM HOT MID-AWAY | **1-4**, 1 RBI · H+R+RBI=**2** | **HIT** Hits · **HIT** HRR (~O1.5) |
| **Lowe Hits / HRR** | #2 · board · heart SEASON_ONLY | **0-3** | **MISS** |
| **Adell Hits** | #3 · CONFIRM mid/away | **1-4** · HRR=1 | **HIT** Hits · HRR miss |
| **Halpin Hits** | #4 · season dump · LOW_SAMPLE_RECENT | **0-1**, BB | **MISS** |
| FADE Kwan | CONFIRM COLD dump | **1-4**, 1 R · HRR=2 | **Fade miss Hits** (HRR fade would’ve been wrong too) |
| FADE Ramírez | CONFIRM COLD | **0-3**, BB | **Fade HIT** |
| FADE Rocchio | COLD | **1-3**, RBI | Soft fade miss |
| Bazzana (GOOD secondary) | HOT heart/mid | **2-3**, **HR**, 1 R, 1 RBI · HRR=**4** | **Cashed outside primary** |
| Bailey (GOOD) | HOT hi-mid | **1-4**, 1 R · HRR=2 | Partial |

**CLE takeaway:** Sharpen layer’s top CONFIRM lean (**DeLauter**) cashed. **Lowe/Halpin SEASON_ONLY** missed — sizing them under DeLauter was right; making Lowe a 2-man anchor leg was still too hot. **Bazzana** was the CLE bat that actually went deep — GOOD map + mid-order vs soft SP deserved more ticket weight.

---

## TB — opener then Griffin bulk

| Lean | Pregame | Final | Grade |
|------|---------|-------|-------|
| **Aranda Hits / HRR** | BEST vs Armstrong / RHP · CONFIRM MID-IN | **3-4**, 2 R, 2 RBI · H+R+RBI=**7** | **SMASH HIT** |
| **Yandy Hits / HRR** | BEST vs LHP bulk | **2-5**, **HR**, 2 R, 2 RBI · HRR=**6** | **HIT** (incl. 9th HR) |
| **Caminero Hits / HRR** | BEST vs LHP bulk · COLD vs Armstrong dump | **1-5**, 2B, 1 RBI · HRR=**2** | **HIT** Hits · **HIT** HRR thin |
| Mesa Hits | Secondary RHP/opener | **1-4** · HRR=1 | **HIT** Hits · HRR miss |
| FADE Simpson | COLD | **0-3**, SF RBI | **Fade Hits OK** |
| FADE Palacios | COLD dump | **3-4**, 2 R · HRR=**5** | **Fade MISS** — biggest inverse |
| FADE Walls | COLD | **1-3**, 1 R | Soft miss |

**TB takeaway:** Pathing worked. Armstrong opener → Griffin LHP → **Aranda** (any RHP/opener) + **Yandy/Caminero** (LHP bulk) all cashed. **Palacios fade** failed hard — COLD map ≠ automatic 0-fer on a contact/utility bat in a crooked inning.

---

## Model lanes scored

| Lane | Call | Result | Grade |
|------|------|--------|-------|
| Martinez K | Under / pass over | 3 K / 5.1 | **HIT** |
| Armstrong K | Pass | 1 K / 1 IP | **N/A / pass correct** |
| Griffin K | No soft under (SPIKE) | 5 K / 3.2 | **Confirm** |
| DeLauter Hits/HRR | CLE #1 | 1 H / HRR 2 | **HIT** |
| Lowe Hits/HRR | CLE #2 | 0-3 | **MISS** |
| Adell Hits | CLE #3 | 1 H | **HIT** |
| Halpin Hits | CLE #4 | 0 H | **MISS** |
| Aranda Hits/HRR | TB primary | 3 H / HRR 7 | **HIT** |
| Yandy + Caminero vs Griffin | LHP bulk 2-man | both HRR ≥2 | **HIT** |
| Kwan fade Hits | FADE | 1 H | **MISS** |
| Palacios fade | FADE | 3 H | **MISS** |

### 2-man report card
| Ticket | Result |
|--------|--------|
| DeLauter Hits + Lowe Hits | **1/2** (Lowe kill) |
| DeLauter HRR + Lowe HRR | **1/2** |
| Aranda HRR (single) | **HIT** |
| Caminero HRR + Yandy HRR | **HIT** (both ≥2) |
| Halpin + Lowe | **0/2** |

---

## Did heatmaps + recent layer help?

**Helped**
- **CONFIRM > SEASON_ONLY** ranking: DeLauter over Lowe/Halpin was the right CLE order.  
- **LHP bulk re-anchor**: Griffin in → Yandy/Caminero production printed.  
- **Aranda** opener/RHP lean crushed.  
- **Martinez UNDER_OK** + **Griffin SPIKE** both confirmed.  
- Ramírez fade held.

**Didn’t / costs**
- **Lowe** as 2-man anchor despite SEASON_ONLY heart.  
- **Halpin** LOW_SAMPLE_RECENT still on the card — miss.  
- **Palacios fade** inverse (3-4).  
- **Kwan fade Hits** too aggressive for a contact leadoff vs soft FLY arm.  
- **Bazzana** underweighted (2-3, HR).

---

## Process updates (lock)

1. **2-man rule:** At least one leg must be **CONFIRM** (or elite board + CONFIRM-adjacent). **SEASON_ONLY** bats are singles / secondary — not A-ticket anchors.  
2. **LOW_SAMPLE_RECENT** → max one small Hits ticket; **no HRR 2-man leg**.  
3. **Identify primary bulk arm live** (first long reliever after opener) — grade TB LHP leans vs **Griffin**, not late Cantillo.  
4. **Fade Hits on contact leadoff (Kwan-types)** only when soft SP *and* you’re fading HRR/power — prefer fade H+R+RBI / HR, not O0.5 Hits.  
5. **COLD fade ≠ automatic** on mid/utility bats (Palacios) — require soft board **and** COLD dump **and** no multi-hit recent form; else pass fade.  
6. Promote **GOOD** mid-order bats with HOT heart/mid vs **UNDER_OK / soft FLY** SPs (Bazzana prototype) into the lean card, not just appendix notes.  
7. Keep opener incomplete grade; keep season∩recent CONFIRM as the sizing gate — this night validated it.

---

## Scoring tape
1. Bot 1 — DeLauter single (Kwan scores) → CLE 1–0  
2. Top 3 — Aranda single (Yandy scores) → tied  
3. Top 6 — Caminero double (Aranda scores) → TB 2–1  
4. Top 7 — Aranda single + error (2 R); Simpson SF → TB 5–1  
5. Bot 7 — Bazzana HR; Rocchio single (Bailey scores) → TB 5–3  
6. Top 9 — **Yandy 2-run HR** → TB **7–3** final

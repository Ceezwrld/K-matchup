# Zone overlap — vs Freddy Peralta (2026 Statcast)

**Game:** MIL@TB
**Pitcher:** Freddy Peralta (RHP, id 642547) · n=3347 pitches
**Windows:** season + **last 30d** (pitcher recent n=258)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter **damage**; **dump fit** adds where they **swing** on his LHB/RHB tunnel. **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** FF 54% / CH 23% / CU 13% / ST 5% / SL 4% / CS 1%
**Velo:** CH ~87.5, CS ~74.7, CU ~79.6, FF ~94.6, SL ~83.1, ST ~82.4

## Where the pitcher throws

### vs LHB — in-zone 42% · heart 6% · mean px=-0.422 (neg=3B) pz=2.405

- Top zones: OUT-UP-3B 24%, OUT-DN-3B 21%, OUT-DN-1B 8%, MID-IN 7%, HEART 6%, HI-IN (3B) 6%
- **Usage vs this hand:** FF 52%, CH 27%, CU 16%, SL 2%, ST 2%, CS 1%
- **CH lands:** OUT-DN-3B 43%, OUT-UP-3B 15%, OUT-DN-1B 11%
- **CU lands:** OUT-DN-3B 31%, OUT-DN-1B 19%, OUT-UP-3B 10%
- **FF lands:** OUT-UP-3B 33%, OUT-UP-1B 12%, HI-IN (3B) 10%
- **SL lands:** OUT-DN-1B 30%, OUT-DN-3B 22%, LO-IN 10%
- **ST lands:** OUT-DN-3B 33%, OUT-UP-3B 15%, LO-AWAY 9%
- **Zone → pitch mix:** OUT-UP-3B (23% throws → FF 74%+CH 17%); OUT-DN-3B (21% throws → CH 55%+CU 24%); OUT-DN-1B (8% throws → CU 39%+CH 36%); MID-IN (7% throws → FF 55%+CU 22%)
- **Dump (ticket tunnel):** OUT-UP-3B 23.5% FF+CH · chase; OUT-DN-3B 20.9% CH+CU · chase

### vs RHB — in-zone 45% · heart 6% · mean px=0.018 (neg=3B) pz=2.25

- Top zones: OUT-DN-1B 22%, OUT-UP-3B 16%, OUT-DN-3B 11%, OUT-UP-1B 7%, HEART 6%, MID-IN 6%
- **Usage vs this hand:** FF 56%, CH 17%, ST 12%, SL 7%, CU 7%, CS 1%
- **CH lands:** OUT-DN-3B 30%, OUT-DN-1B 28%, OUT-UP-3B 8%
- **CU lands:** OUT-DN-1B 25%, OUT-DN-3B 13%, MID-IN 9%
- **FF lands:** OUT-UP-3B 23%, OUT-UP-1B 11%, HI-MID 9%
- **SL lands:** OUT-DN-1B 66%, MID-AWAY 6%, MID-IN 6%
- **ST lands:** OUT-DN-1B 46%, LO-AWAY 11%, HEART 9%
- **Zone → pitch mix:** OUT-DN-1B (22% throws → ST 25%+CH 23%); OUT-UP-3B (16% throws → FF 83%+CH 9%); OUT-DN-3B (11% throws → CH 49%+FF 36%); OUT-UP-1B (7% throws → FF 90%+ST 4%)
- **Dump (ticket tunnel):** OUT-DN-1B 21.5% ST+CH · chase; OUT-UP-3B 15.6% FF+CH · chase

## Dump × swing (vs LHB / RHB)

Pitcher’s #1 throw pocket vs that batter’s hand, crossed with whether they **swing** there. TUNNEL = Hits location. MISTAKE = hunt middle, not the dump. CHASE/TAKE = not a Hits lean on the tunnel (K / take).

| Batter | Stand | Dump | Throw | Swing | Whiff | xwOBA | Fit |
|--------|-------|------|-------|-------|-------|-------|-----|
| Jake Bauers | L | OUT-UP-3B | 23.5% FF+CH | 10.2 | 58.1 | nan | **MISTAKE** |
| Garrett Mitchell | L | OUT-UP-3B | 23.5% FF+CH | 11.9 | 68.8 | nan | **MISTAKE** |
| Jackson Chourio | R | OUT-DN-1B | 21.5% ST+CH | 26.9 | 66.9 | 0.255 | **MISTAKE** |
| Brice Turang | L | OUT-UP-3B | 23.5% FF+CH | 20.3 | 26.3 | 0.262 | **MISTAKE** |
| William Contreras | R | OUT-DN-1B | 21.5% ST+CH | 22.9 | 59.8 | 0.266 | **MISTAKE** |
| Cooper Pratt | R | OUT-DN-1B | 21.5% ST+CH | 26.4 | 49.2 | 0.398 | **TUNNEL** |
| Christian Yelich | L | OUT-UP-3B | 23.5% FF+CH | 7.3 | 47.1 | nan | **MISTAKE** |
| David Hamilton | L | OUT-UP-3B | 23.5% FF+CH | 20.5 | 11.9 | 0.231 | **MISTAKE** |
| Sal Frelick | L | OUT-UP-3B | 23.5% FF+CH | 20.5 | 15.6 | 0.317 | **TAKE** |

## Batter heat vs opposing hand → overlap

### Jake Bauers (stand L, vs RHP, season n=1989, recent n=138)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-UP-3B; HOT in-zone MID-IN/HEART (swing 10.2% · whiff 58.1% · xwOBA nan)
- Swing 39.2% · whiff/swing 28.4%
- **Top swing (season):** HEART 77.1%; HI-MID 73.6%; MID-AWAY 62.5%; HI-AWAY (1B) 61.8%
- **Top damage season (xwOBA BIP):** OUT-UP-1B 0.764 (EV 84.9, brl 20.0%, BIP 10); HI-MID 0.644 (EV 101.6, brl 24.0%, BIP 25); HI-AWAY (1B) 0.566 (EV 83.5, brl 36.4%, BIP 11); MID-IN 0.506 (EV 98.1, brl 16.7%, BIP 30)
- **HOT/WARM overlap:** HOT OUT-UP-1B (W 6.1%, xwOBA 0.764, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT MID-IN (W 6.7%, xwOBA 0.506, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT HEART (W 6.5%, xwOBA 0.447, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM LO-MID (W 5.3%, xwOBA 0.481, recent — xwOBA 0.204 BIP 4 · SEASON_ONLY); WARM LO-IN (W 5.1%, xwOBA 0.356 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-3B (W 20.9%, xwOBA 0.247, recent — · SEASON_ONLY)

### Garrett Mitchell (stand L, vs RHP, season n=1841, recent n=110)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-UP-3B; HOT in-zone LO-MID/HEART (swing 11.9% · whiff 68.8% · xwOBA nan)
- Swing 45.6% · whiff/swing 33.9%
- **Top swing (season):** HEART 80.5%; HI-MID 79.0%; MID-IN 69.7%; HI-AWAY (1B) 68.1%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.642 (EV 97.7, brl 11.1%, BIP 18); HI-MID 0.625 (EV 100.2, brl 26.7%, BIP 15); HEART 0.586 (EV 99.8, brl 19.1%, BIP 47); MID-IN 0.554 (EV 97.2, brl 11.1%, BIP 27)
- **HOT/WARM overlap:** WARM LO-MID (W 5.3%, xwOBA 0.472, recent WARM xwOBA 0.353 BIP 4 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HEART (W 6.5%, xwOBA 0.586 · SEASON_ONLY); HOT MID-IN (W 6.7%, xwOBA 0.554 · SEASON_ONLY); HOT OUT-UP-1B (W 6.1%, xwOBA 0.611 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-DN-1B (W 7.8%, xwOBA 0.421, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 20.9%, xwOBA 0.206, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** WARM LO-MID

### Jackson Chourio (stand R, vs RHP, season n=1758, recent n=137)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone MID-IN/HEART (swing 26.9% · whiff 66.9% · xwOBA 0.255)
- Swing 49.1% · whiff/swing 23.8%
- **Top swing (season):** MID-IN 77.4%; HI-IN (3B) 74.6%; HEART 72.6%; HI-MID 68.7%
- **Top damage season (xwOBA BIP):** HEART 0.651 (EV 98.6, brl 26.2%, BIP 42); MID-IN 0.558 (EV 96.1, brl 23.7%, BIP 38); HI-MID 0.501 (EV 98.2, brl 22.7%, BIP 22); LO-IN 0.441 (EV 96.5, brl 10.0%, BIP 20)
- **Top damage recent (30d):** MID-IN 0.641 (BIP 5)
- **HOT/WARM overlap:** HOT MID-IN (W 6.3%, xwOBA 0.558, recent HOT xwOBA 0.641 BIP 5 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM OUT-UP-3B (W 15.6%, xwOBA 0.35, recent COLD xwOBA 0.178 BIP 4 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HEART (W 6.6%, xwOBA 0.651 · SEASON_ONLY); HOT HI-MID (W 6.0%, xwOBA 0.501 · SEASON_ONLY); WARM MID-AWAY (W 5.5%, xwOBA 0.409 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 21.5%, xwOBA 0.255, recent — · SEASON_ONLY); OUT-DN-3B (W 10.8%, xwOBA 0.194, recent — · SEASON_ONLY); OUT-UP-1B (W 7.1%, xwOBA 0.22, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT MID-IN
- **Season vs recent CONFLICT:** OUT-UP-3B (WARM→COLD)

### Brice Turang (stand L, vs RHP, season n=2214, recent n=119)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-UP-3B; HOT in-zone HEART/LO-MID (swing 20.3% · whiff 26.3% · xwOBA 0.262)
- Swing 44.2% · whiff/swing 19.0%
- **Top swing (season):** HI-MID 74.5%; HI-AWAY (1B) 71.8%; MID-AWAY 71.6%; HEART 68.8%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.554 (EV 97.0, brl 17.2%, BIP 29); HEART 0.553 (EV 95.8, brl 17.1%, BIP 41); OUT-DN-1B 0.517 (EV 92.9, brl 7.7%, BIP 13); LO-MID 0.504 (EV 89.6, brl 9.3%, BIP 54)
- **HOT/WARM overlap:** HOT OUT-DN-1B (W 7.8%, xwOBA 0.517, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 6.5%, xwOBA 0.553, recent — xwOBA nan BIP 0 · SEASON_ONLY); WARM LO-MID (W 5.3%, xwOBA 0.504 · SEASON_ONLY); WARM MID-IN (W 6.7%, xwOBA 0.375, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM LO-IN (W 5.1%, xwOBA 0.387 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 23.5%, xwOBA 0.262, recent — · SEASON_ONLY)

### William Contreras (stand R, vs RHP, season n=1790, recent n=121)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone MID-IN/HEART (swing 22.9% · whiff 59.8% · xwOBA 0.266)
- Swing 48.0% · whiff/swing 17.6%
- **Top swing (season):** HI-MID 81.0%; HEART 76.7%; MID-IN 74.5%; HI-IN (3B) 73.9%
- **Top damage season (xwOBA BIP):** OUT-DN-3B 0.516 (EV 90.6, brl 6.7%, BIP 15); HI-IN (3B) 0.453 (EV 91.6, brl 20.6%, BIP 34); OUT-UP-1B 0.430 (EV 83.5, brl 16.7%, BIP 12); LO-AWAY 0.428 (EV 90.2, brl 3.7%, BIP 27)
- **HOT/WARM overlap:** WARM MID-IN (W 6.3%, xwOBA 0.388, recent HOT xwOBA 0.401 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-3B (W 10.8%, xwOBA 0.516, recent — xwOBA nan BIP 1 · SEASON_ONLY); HOT OUT-UP-1B (W 7.1%, xwOBA 0.43, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HEART (W 6.6%, xwOBA 0.38, recent COLD xwOBA 0.028 BIP 4 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HI-MID (W 6.0%, xwOBA 0.4, recent — xwOBA 0.446 BIP 4 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 21.5%, xwOBA 0.266, recent — · SEASON_ONLY); OUT-UP-3B (W 15.6%, xwOBA 0.211, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** WARM MID-IN
- **Season vs recent CONFLICT:** HEART (WARM→COLD)

### Cooper Pratt (stand R, vs RHP, season n=997, recent n=120)
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-1B (W 21.5% ST+CH) (swing 26.4% · whiff 49.2% · xwOBA 0.398)
- Swing 45.2% · whiff/swing 17.3%
- **Top swing (season):** HEART 77.6%; HI-MID 68.8%; MID-IN 65.3%; LO-MID 62.7%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.398 (EV 82.0, brl 0.0%, BIP 17); LO-AWAY 0.378 (EV 82.7, brl 0.0%, BIP 18); MID-AWAY 0.368 (EV 91.8, brl 4.5%, BIP 22); HI-IN (3B) 0.358 (EV 80.3, brl 6.7%, BIP 15)
- **Top damage recent (30d):** LO-AWAY 0.508 (BIP 5); LO-MID 0.249 (BIP 5); HEART 0.157 (BIP 5)
- **HOT/WARM overlap:** WARM OUT-DN-1B (W 21.5%, xwOBA 0.398, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM HEART (W 6.6%, xwOBA 0.355, recent COLD xwOBA 0.157 BIP 5 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM MID-AWAY (W 5.5%, xwOBA 0.368 · SEASON_ONLY); WARM LO-AWAY (W 5.1%, xwOBA 0.378 · SEASON_ONLY); HOT OUT-UP-3B (W 15.6%, xwOBA 0.574, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 10.8%, xwOBA 0.104, recent — · SEASON_ONLY)
- **Season vs recent CONFLICT:** HEART (WARM→COLD)

### Christian Yelich (stand L, vs RHP, season n=1767, recent n=115)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-UP-3B; HOT in-zone LO-MID/HEART (swing 7.3% · whiff 47.1% · xwOBA nan)
- Swing 45.3% · whiff/swing 29.8%
- **Top swing (season):** HEART 76.4%; LO-AWAY 71.2%; HI-AWAY (1B) 70.5%; LO-MID 70.5%
- **Top damage season (xwOBA BIP):** HEART 0.635 (EV 95.4, brl 20.0%, BIP 30); MID-IN 0.560 (EV 98.6, brl 19.0%, BIP 21); HI-MID 0.500 (EV 82.0, brl 30.8%, BIP 13); LO-MID 0.482 (EV 96.5, brl 18.2%, BIP 33)
- **Top damage recent (30d):** LO-MID 0.653 (BIP 5)
- **HOT/WARM overlap:** WARM LO-MID (W 5.3%, xwOBA 0.482, recent WARM xwOBA 0.653 BIP 5 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HEART (W 6.5%, xwOBA 0.635, recent — xwOBA nan BIP 1 · SEASON_ONLY); HOT MID-IN (W 6.7%, xwOBA 0.56 · SEASON_ONLY); WARM HI-IN (3B) (W 6.2%, xwOBA 0.394 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 20.9%, xwOBA 0.226, recent — · SEASON_ONLY); OUT-DN-1B (W 7.8%, xwOBA 0.236, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** WARM LO-MID

### David Hamilton (stand L, vs RHP, season n=1457, recent n=65)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-UP-3B; HOT in-zone HEART/LO-IN (swing 20.5% · whiff 11.9% · xwOBA 0.231)
- Swing 45.9% · whiff/swing 17.5%
- **Top swing (season):** HI-MID 76.3%; MID-AWAY 76.3%; HEART 70.6%; HI-AWAY (1B) 67.9%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.475 (EV 96.4, brl 11.8%, BIP 17); HEART 0.432 (EV 85.7, brl 18.4%, BIP 38); LO-IN 0.363 (EV 73.9, brl 0.0%, BIP 10); MID-AWAY 0.342 (EV 85.6, brl 8.1%, BIP 37)
- **HOT/WARM overlap:** HOT HEART (W 6.5%, xwOBA 0.432 · SEASON_ONLY); WARM LO-IN (W 5.1%, xwOBA 0.363 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-UP-3B (W 23.5%, xwOBA 0.231, recent COLD · CONFIRM); OUT-DN-3B (W 20.9%, xwOBA 0.175, recent — · SEASON_ONLY); OUT-DN-1B (W 7.8%, xwOBA 0.24, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-UP-3B

### Sal Frelick (stand L, vs RHP, season n=1341, recent n=100)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TAKE`** — takes dump OUT-UP-3B (swing 20.5%) — not a Hits lean on that pitch (swing 20.5% · whiff 15.6% · xwOBA 0.317)
- Swing 43.0% · whiff/swing 7.6%
- **Top swing (season):** MID-AWAY 66.7%; LO-MID 66.2%; HI-MID 64.0%; HI-AWAY (1B) 62.3%
- **Top damage season (xwOBA BIP):** LO-IN 0.324 (EV 82.3, brl 0.0%, BIP 17); LO-MID 0.318 (EV 91.2, brl 10.5%, BIP 38); OUT-UP-3B 0.317 (EV 87.7, brl 9.1%, BIP 11); HI-IN (3B) 0.314 (EV 89.1, brl 0.0%, BIP 16)
- **COLD vs his tunnel:** OUT-DN-3B (W 20.9%, xwOBA 0.2 · SEASON_ONLY); OUT-DN-1B (W 7.8%, xwOBA 0.223, recent — · SEASON_ONLY)

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | Exp H | P(1+) | PA | RBI | HR/RBI | Zone note |
|------|--------|------|-------|-------|----|-----|--------|-----------|
| 2 | Jake Bauers | 59.4 | 0.43 | 37% | 3 | good | 60.7 | MISTAKE OUT-UP-3B; HOT OUT-UP-1B/MID-IN; COLD OUT-DN-3B |
| 6 | Garrett Mitchell | 58.7 | 0.29 | 27% | 2 | good | 59.3 | MISTAKE OUT-UP-3B; CONFIRM WARM LO-MID; COLD OUT-DN-3B; LOW_SAMPLE_RECENT |
| 1 | Jackson Chourio | 57.7 | 0.45 | 38% | 3 | thin | 57.8 | MISTAKE OUT-DN-1B; CONFIRM HOT MID-IN; COLD OUT-DN-1B; CONFLICT OUT-UP-3B |
| 5 | Brice Turang | 55.8 | 0.54 | 45% | 3 | prime | 54.0 | MISTAKE OUT-UP-3B; HOT OUT-DN-1B/HEART; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 4 | William Contreras | 54.4 | 0.58 | 47% | 3 | prime | 53.8 | MISTAKE OUT-DN-1B; CONFIRM WARM MID-IN; COLD OUT-DN-1B; CONFLICT HEART |
| 7 | Cooper Pratt | 51.5 | 0.38 | 34% | 2 | thin | 47.2 | TUNNEL OUT-DN-1B; HOT OUT-UP-3B; COLD OUT-DN-3B; CONFLICT HEART |
| 3 | Christian Yelich | 50.2 | 0.45 | 38% | 3 | prime | 50.3 | MISTAKE OUT-UP-3B; CONFIRM WARM LO-MID; COLD OUT-DN-3B; LOW_SAMPLE_RECENT |
| 9 | David Hamilton | 43.5 | 0.37 | 34% | 2 | thin | 41.0 | MISTAKE OUT-UP-3B; CONFIRM COLD OUT-UP-3B; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 8 | Sal Frelick | 42.3 | 0.38 | 34% | 2 | thin | 40.3 | TAKE OUT-UP-3B; COLD OUT-DN-3B; LOW_SAMPLE_RECENT |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM **TUNNEL** HOTs; MISTAKE = heart/in-zone, not the dump. Treat `LOW_SAMPLE_*` as sizing FYI.*

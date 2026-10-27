# Zone overlap — vs Griffin Jax (2026 Statcast)

**Game:** MIL@TB
**Pitcher:** Griffin Jax (RHP, id 643377) · n=1887 pitches
**Windows:** season + **last 30d** (pitcher recent n=99)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter **damage**; **dump fit** adds where they **swing** on his LHB/RHB tunnel. **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** ST 25% / SI 23% / CH 23% / FF 18% / CU 9% / FC 3%
**Velo:** CH ~90.9, CU ~85.0, FC ~92.7, FF ~95.9, SI ~95.4, ST ~87.6

## Where the pitcher throws

### vs LHB — in-zone 46% · heart 7% · mean px=-0.152 (neg=3B) pz=2.141

- Top zones: OUT-DN-3B 20%, OUT-DN-1B 16%, OUT-UP-3B 14%, HEART 7%, LO-MID 7%, LO-IN 6%
- **Usage vs this hand:** CH 30%, FF 20%, ST 17%, SI 16%, CU 12%, FC 4%
- **CH lands:** OUT-DN-3B 49%, LO-IN 12%, OUT-UP-3B 10%
- **CU lands:** OUT-DN-1B 32%, OUT-DN-3B 24%, LO-MID 9%
- **FC lands:** OUT-DN-1B 35%, HEART 15%, LO-AWAY 10%
- **FF lands:** OUT-UP-3B 32%, OUT-UP-1B 12%, HI-MID 12%
- **SI lands:** HEART 13%, OUT-UP-3B 12%, OUT-DN-1B 11%
- **ST lands:** OUT-DN-1B 36%, HEART 11%, LO-MID 10%
- **Zone → pitch mix:** OUT-DN-3B (20% throws → CH 74%+CU 15%); OUT-DN-1B (16% throws → ST 38%+CU 25%); OUT-UP-3B (14% throws → FF 49%+CH 22%); HEART (7% throws → SI 28%+ST 27%)
- **Dump (ticket tunnel):** OUT-DN-3B 19.7% CH+CU · chase; OUT-DN-1B 16.2% ST+CU · chase

### vs RHB — in-zone 44% · heart 7% · mean px=0.141 (neg=3B) pz=2.012

- Top zones: OUT-DN-1B 27%, OUT-DN-3B 13%, OUT-UP-3B 10%, HEART 7%, LO-AWAY 7%, OUT-UP-1B 6%
- **Usage vs this hand:** ST 39%, SI 35%, FF 13%, CH 11%, CU 2%, FC 0%
- **CH lands:** OUT-DN-3B 40%, OUT-DN-1B 26%, MID-IN 10%
- **FF lands:** OUT-UP-1B 33%, OUT-DN-1B 13%, HI-MID 12%
- **SI lands:** OUT-DN-3B 22%, OUT-UP-3B 19%, LO-IN 13%
- **ST lands:** OUT-DN-1B 49%, LO-AWAY 9%, HEART 8%
- **Zone → pitch mix:** OUT-DN-1B (27% throws → ST 71%+CH 10%); OUT-DN-3B (13% throws → SI 59%+CH 33%); OUT-UP-3B (10% throws → SI 67%+ST 19%); HEART (7% throws → SI 45%+ST 43%)
- **Dump (ticket tunnel):** OUT-DN-1B 27.2% ST+CH · chase; OUT-DN-3B 12.7% SI+CH · chase

## Dump × swing (vs LHB / RHB)

Pitcher’s #1 throw pocket vs that batter’s hand, crossed with whether they **swing** there. TUNNEL = Hits location. MISTAKE = hunt middle, not the dump. CHASE/TAKE = not a Hits lean on the tunnel (K / take).

| Batter | Stand | Dump | Throw | Swing | Whiff | xwOBA | Fit |
|--------|-------|------|-------|-------|-------|-------|-----|
| Jake Bauers | L | OUT-DN-3B | 19.7% CH+CU | 20.8 | 63.0 | 0.247 | **MISTAKE** |
| Garrett Mitchell | L | OUT-DN-3B | 19.7% CH+CU | 34.2 | 59.8 | 0.206 | **MISTAKE** |
| Jackson Chourio | R | OUT-DN-1B | 27.2% ST+CH | 26.7 | 66.9 | 0.255 | **MISTAKE** |
| Brice Turang | L | OUT-DN-3B | 19.7% CH+CU | 30.9 | 32.1 | 0.293 | **MISTAKE** |
| William Contreras | R | OUT-DN-1B | 27.2% ST+CH | 22.7 | 59.8 | 0.266 | **MISTAKE** |
| Cooper Pratt | R | OUT-DN-1B | 27.2% ST+CH | 27.3 | 50.0 | 0.379 | **TUNNEL** |
| Christian Yelich | L | OUT-DN-3B | 19.7% CH+CU | 33.7 | 51.6 | 0.226 | **MISTAKE** |
| David Hamilton | L | OUT-DN-3B | 19.7% CH+CU | 35.2 | 50.0 | 0.175 | **MISTAKE** |
| Sal Frelick | L | OUT-DN-3B | 19.7% CH+CU | 33.0 | 8.6 | 0.2 | **COLD** |

## Batter heat vs opposing hand → overlap

### Jake Bauers (stand L, vs RHP, season n=2011, recent n=154)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone MID-IN/HI-MID (swing 20.8% · whiff 63.0% · xwOBA 0.247)
- Swing 39.1% · whiff/swing 28.2%
- **Top swing (season):** HEART 77.2%; HI-MID 73.6%; MID-AWAY 62.2%; HI-AWAY (1B) 61.8%
- **Top damage season (xwOBA BIP):** OUT-UP-1B 0.764 (EV 84.9, brl 20.0%, BIP 10); HI-MID 0.644 (EV 101.6, brl 24.0%, BIP 25); HI-AWAY (1B) 0.566 (EV 83.5, brl 36.4%, BIP 11); MID-IN 0.495 (EV 98.0, brl 16.1%, BIP 31)
- **HOT/WARM overlap:** HOT MID-IN (W 6.1%, xwOBA 0.495, recent WARM xwOBA 0.367 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM HI-MID (W 5.2%, xwOBA 0.644 · SEASON_ONLY); HOT LO-MID (W 6.7%, xwOBA 0.481, recent — xwOBA 0.204 BIP 4 · SEASON_ONLY); HOT HEART (W 7.2%, xwOBA 0.439, recent — xwOBA nan BIP 2 · SEASON_ONLY); WARM LO-IN (W 6.1%, xwOBA 0.356 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-3B (W 19.7%, xwOBA 0.247, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT MID-IN

### Garrett Mitchell (stand L, vs RHP, season n=1859, recent n=113)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone HEART/MID-IN (swing 34.2% · whiff 59.8% · xwOBA 0.206)
- Swing 45.7% · whiff/swing 34.0%
- **Top swing (season):** HEART 80.5%; HI-MID 79.2%; MID-IN 69.1%; HI-AWAY (1B) 68.1%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.642 (EV 97.7, brl 11.1%, BIP 18); HI-MID 0.625 (EV 100.2, brl 26.7%, BIP 15); HEART 0.586 (EV 99.8, brl 19.1%, BIP 47); MID-IN 0.554 (EV 97.2, brl 11.1%, BIP 27)
- **HOT/WARM overlap:** HOT OUT-DN-1B (W 16.2%, xwOBA 0.421, recent — xwOBA None BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 7.2%, xwOBA 0.586 · SEASON_ONLY); HOT MID-IN (W 6.1%, xwOBA 0.554 · SEASON_ONLY); WARM HI-MID (W 5.2%, xwOBA 0.625 · SEASON_ONLY); HOT LO-MID (W 6.7%, xwOBA 0.472 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-3B (W 19.7%, xwOBA 0.206, recent — · SEASON_ONLY)

### Jackson Chourio (stand R, vs RHP, season n=1772, recent n=146)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone HEART/LO-MID (swing 26.7% · whiff 66.9% · xwOBA 0.255)
- Swing 49.2% · whiff/swing 23.7%
- **Top swing (season):** MID-IN 77.4%; HI-IN (3B) 74.6%; HEART 72.5%; HI-MID 69.4%
- **Top damage season (xwOBA BIP):** HEART 0.654 (EV 98.7, brl 25.6%, BIP 43); MID-IN 0.558 (EV 96.1, brl 23.7%, BIP 38); HI-MID 0.521 (EV 98.5, brl 21.7%, BIP 23); LO-IN 0.441 (EV 96.5, brl 10.0%, BIP 20)
- **Top damage recent (30d):** MID-IN 0.641 (BIP 5); MID-AWAY 0.632 (BIP 5)
- **HOT/WARM overlap:** HOT HEART (W 7.2%, xwOBA 0.654, recent HOT xwOBA 0.71 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM LO-MID (W 5.2%, xwOBA 0.367, recent WARM xwOBA 0.458 BIP 4 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM OUT-UP-3B (W 9.8%, xwOBA 0.35, recent COLD xwOBA 0.235 BIP 3 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM LO-IN (W 5.5%, xwOBA 0.441 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 27.2%, xwOBA 0.255, recent — · SEASON_ONLY); OUT-DN-3B (W 12.7%, xwOBA 0.194, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT HEART, WARM LO-MID
- **Season vs recent CONFLICT:** OUT-UP-3B (WARM→COLD)

### Brice Turang (stand L, vs RHP, season n=2227, recent n=126)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone HEART/LO-MID (swing 30.9% · whiff 32.1% · xwOBA 0.293)
- Swing 44.2% · whiff/swing 18.9%
- **Top swing (season):** HI-MID 74.5%; HI-AWAY (1B) 71.8%; MID-AWAY 71.6%; HEART 68.4%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.554 (EV 97.0, brl 17.2%, BIP 29); HEART 0.553 (EV 95.8, brl 17.1%, BIP 41); OUT-DN-1B 0.517 (EV 92.9, brl 7.7%, BIP 13); LO-MID 0.504 (EV 89.6, brl 9.3%, BIP 54)
- **HOT/WARM overlap:** HOT OUT-DN-1B (W 16.2%, xwOBA 0.517, recent — xwOBA None BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 7.2%, xwOBA 0.553, recent — xwOBA None BIP 0 · SEASON_ONLY); HOT LO-MID (W 6.7%, xwOBA 0.504 · SEASON_ONLY); WARM HI-MID (W 5.2%, xwOBA 0.479 · SEASON_ONLY); WARM LO-IN (W 6.1%, xwOBA 0.387 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 13.6%, xwOBA 0.244, recent — · SEASON_ONLY)

### William Contreras (stand R, vs RHP, season n=1812, recent n=139)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone LO-AWAY/HEART (swing 22.7% · whiff 59.8% · xwOBA 0.266)
- Swing 48.0% · whiff/swing 17.5%
- **Top swing (season):** HI-MID 81.4%; HEART 76.9%; MID-IN 74.5%; HI-IN (3B) 74.2%
- **Top damage season (xwOBA BIP):** OUT-DN-3B 0.516 (EV 90.6, brl 6.7%, BIP 15); HI-IN (3B) 0.443 (EV 91.7, brl 20.0%, BIP 35); LO-AWAY 0.428 (EV 90.2, brl 3.7%, BIP 27); OUT-UP-1B 0.414 (EV 82.4, brl 15.4%, BIP 13)
- **HOT/WARM overlap:** HOT OUT-DN-3B (W 12.7%, xwOBA 0.516, recent — xwOBA nan BIP 1 · SEASON_ONLY); HOT LO-AWAY (W 6.8%, xwOBA 0.428, recent — xwOBA nan BIP 0 · SEASON_ONLY); WARM HEART (W 7.2%, xwOBA 0.38, recent COLD xwOBA 0.028 BIP 4 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-UP-1B (W 6.5%, xwOBA 0.414, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM LO-IN (W 5.5%, xwOBA 0.411 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 27.2%, xwOBA 0.266, recent COLD · CONFIRM); OUT-UP-3B (W 9.8%, xwOBA 0.205, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-1B
- **Season vs recent CONFLICT:** HEART (WARM→COLD)

### Cooper Pratt (stand R, vs RHP, season n=1007, recent n=123)
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-1B (W 27.2% ST+CH) (swing 27.3% · whiff 50.0% · xwOBA 0.379)
- Swing 45.2% · whiff/swing 17.6%
- **Top swing (season):** HEART 77.6%; HI-MID 68.8%; MID-IN 65.3%; LO-MID 63.2%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.379 (EV 82.6, brl 0.0%, BIP 18); LO-AWAY 0.378 (EV 82.7, brl 0.0%, BIP 18); MID-AWAY 0.368 (EV 91.8, brl 4.5%, BIP 22); HI-IN (3B) 0.358 (EV 80.3, brl 6.7%, BIP 15)
- **Top damage recent (30d):** LO-AWAY 0.508 (BIP 5); LO-MID 0.249 (BIP 5); HEART 0.157 (BIP 5)
- **HOT/WARM overlap:** WARM LO-AWAY (W 6.8%, xwOBA 0.378, recent HOT xwOBA 0.508 BIP 5 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM OUT-DN-1B (W 27.2%, xwOBA 0.379, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM HEART (W 7.2%, xwOBA 0.355, recent COLD xwOBA 0.157 BIP 5 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-UP-3B (W 9.8%, xwOBA 0.574, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 12.7%, xwOBA 0.104, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** WARM LO-AWAY
- **Season vs recent CONFLICT:** HEART (WARM→COLD)

### Christian Yelich (stand L, vs RHP, season n=1778, recent n=117)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone LO-MID/HEART (swing 33.7% · whiff 51.6% · xwOBA 0.226)
- Swing 45.3% · whiff/swing 29.8%
- **Top swing (season):** HEART 76.6%; LO-AWAY 71.2%; HI-AWAY (1B) 71.0%; LO-MID 70.5%
- **Top damage season (xwOBA BIP):** HEART 0.672 (EV 95.7, brl 22.6%, BIP 31); MID-IN 0.560 (EV 98.6, brl 19.0%, BIP 21); HI-MID 0.500 (EV 82.0, brl 30.8%, BIP 13); LO-MID 0.482 (EV 96.5, brl 18.2%, BIP 33)
- **HOT/WARM overlap:** HOT LO-MID (W 6.7%, xwOBA 0.482, recent HOT xwOBA 0.529 BIP 4 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HEART (W 7.2%, xwOBA 0.672, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT MID-IN (W 6.1%, xwOBA 0.56 · SEASON_ONLY); WARM HI-MID (W 5.2%, xwOBA 0.5 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 19.7%, xwOBA 0.226, recent — · SEASON_ONLY); OUT-DN-1B (W 16.2%, xwOBA 0.236, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT LO-MID

### David Hamilton (stand L, vs RHP, season n=1473, recent n=78)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone HEART/LO-IN (swing 35.2% · whiff 50.0% · xwOBA 0.175)
- Swing 45.8% · whiff/swing 17.5%
- **Top swing (season):** HI-MID 76.3%; MID-AWAY 75.5%; HEART 70.2%; HI-AWAY (1B) 67.9%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.475 (EV 96.4, brl 11.8%, BIP 17); HEART 0.432 (EV 85.7, brl 18.4%, BIP 38); LO-IN 0.363 (EV 73.9, brl 0.0%, BIP 10); MID-AWAY 0.342 (EV 85.6, brl 8.1%, BIP 37)
- **HOT/WARM overlap:** HOT HEART (W 7.2%, xwOBA 0.432, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM LO-IN (W 6.1%, xwOBA 0.363 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-UP-3B (W 13.6%, xwOBA 0.255, recent COLD · CONFIRM); OUT-DN-1B (W 16.2%, xwOBA 0.24, recent — · SEASON_ONLY); OUT-DN-3B (W 19.7%, xwOBA 0.175, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-UP-3B

### Sal Frelick (stand L, vs RHP, season n=1348, recent n=107)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `COLD`** — COLD on dump OUT-DN-3B — pass Hits vs this tunnel (swing 33.0% · whiff 8.6% · xwOBA 0.2)
- Swing 43.0% · whiff/swing 7.6%
- **Top swing (season):** MID-AWAY 66.7%; LO-MID 66.2%; HI-MID 64.0%; MID-IN 61.6%
- **Top damage season (xwOBA BIP):** LO-IN 0.324 (EV 82.3, brl 0.0%, BIP 17); LO-MID 0.318 (EV 91.2, brl 10.5%, BIP 38); OUT-UP-3B 0.317 (EV 87.7, brl 9.1%, BIP 11); HEART 0.312 (EV 90.9, brl 2.7%, BIP 37)
- **Top damage recent (30d):** HI-IN (3B) 0.177 (BIP 6)
- **COLD vs his tunnel:** OUT-DN-1B (W 16.2%, xwOBA 0.223, recent COLD · CONFIRM); OUT-DN-3B (W 19.7%, xwOBA 0.2 · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-1B

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | Exp H | P(1+) | PA | RBI | HR/RBI | Zone note |
|------|--------|------|-------|-------|----|-----|--------|-----------|
| 2 | Jake Bauers | 59.4 | 0.29 | 27% | 2 | good | 60.7 | MISTAKE OUT-DN-3B; CONFIRM HOT MID-IN; COLD OUT-DN-3B |
| 6 | Garrett Mitchell | 58.7 | 0.30 | 27% | 2 | good | 59.3 | MISTAKE OUT-DN-3B; HOT OUT-DN-1B/HEART; COLD OUT-DN-3B; LOW_SAMPLE_RECENT |
| 1 | Jackson Chourio | 57.7 | 0.32 | 29% | 2 | thin | 57.8 | MISTAKE OUT-DN-1B; CONFIRM HOT HEART/WARM LO-MID; COLD OUT-DN-1B; CONFLICT OUT-UP-3B |
| 5 | Brice Turang | 55.8 | 0.38 | 34% | 2 | good | 54.0 | MISTAKE OUT-DN-3B; HOT OUT-DN-1B/HEART; COLD OUT-UP-3B |
| 4 | William Contreras | 54.4 | 0.41 | 37% | 2 | good | 53.8 | MISTAKE OUT-DN-1B; CONFIRM COLD OUT-DN-1B; COLD OUT-DN-1B; CONFLICT HEART |
| 7 | Cooper Pratt | 51.5 | 0.41 | 37% | 2 | thin | 47.2 | TUNNEL OUT-DN-1B; CONFIRM WARM LO-AWAY; COLD OUT-DN-3B; CONFLICT HEART |
| 3 | Christian Yelich | 50.2 | 0.31 | 29% | 2 | good | 50.3 | MISTAKE OUT-DN-3B; CONFIRM HOT LO-MID; COLD OUT-DN-3B; LOW_SAMPLE_RECENT |
| 9 | David Hamilton | 43.5 | 0.37 | 34% | 2 | thin | 41.0 | MISTAKE OUT-DN-3B; CONFIRM COLD OUT-UP-3B; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 8 | Sal Frelick | 42.3 | 0.40 | 36% | 2 | thin | 40.3 | COLD OUT-DN-3B; CONFIRM COLD OUT-DN-1B; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM **TUNNEL** HOTs; MISTAKE = heart/in-zone, not the dump. Treat `LOW_SAMPLE_*` as sizing FYI.*

# Zone overlap — vs Jacob Misiorowski (2026 Statcast)

**Game:** TB@MIL
**Pitcher:** Jacob Misiorowski (RHP, id 694819) · n=3044 pitches
**Windows:** season + **last 30d** (pitcher recent n=250)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter **damage**; **dump fit** adds where they **swing** on his LHB/RHB tunnel. **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** FF 63% / FC 13% / CU 12% / SL 11% / CH 2% / SI 0%
**Velo:** CH ~91.7, CU ~87.7, FC ~95.8, FF ~100.5, SI ~100.6, SL ~91.9

## Where the pitcher throws

### vs LHB — in-zone 50% · heart 7% · mean px=0.011 (neg=3B) pz=2.586

- Top zones: OUT-UP-3B 21%, OUT-DN-1B 15%, OUT-UP-1B 10%, HI-MID 8%, HEART 7%, HI-IN (3B) 6%
- **Usage vs this hand:** FF 63%, CU 14%, FC 14%, SL 7%, CH 2%, SI 0%
- **CH lands:** OUT-UP-3B 25%, OUT-DN-3B 20%, OUT-DN-1B 18%
- **CU lands:** OUT-DN-1B 37%, OUT-DN-3B 11%, OUT-UP-3B 11%
- **FC lands:** OUT-DN-1B 32%, MID-AWAY 10%, OUT-UP-1B 10%
- **FF lands:** OUT-UP-3B 27%, OUT-UP-1B 12%, HI-MID 10%
- **SL lands:** OUT-DN-1B 26%, OUT-UP-3B 15%, LO-MID 13%
- **Zone → pitch mix:** OUT-UP-3B (21% throws → FF 80%+CU 7%); OUT-DN-1B (15% throws → CU 36%+FC 29%); OUT-UP-1B (10% throws → FF 81%+FC 13%); HI-MID (8% throws → FF 80%+FC 9%)
- **Dump (ticket tunnel):** OUT-UP-3B 21.2% FF+CU · chase; OUT-DN-1B 14.8% CU+FC · chase

### vs RHB — in-zone 50% · heart 7% · mean px=0.322 (neg=3B) pz=2.487

- Top zones: OUT-DN-1B 22%, OUT-UP-3B 13%, OUT-UP-1B 12%, MID-AWAY 8%, HI-AWAY (1B) 7%, HEART 7%
- **Usage vs this hand:** FF 62%, SL 17%, FC 12%, CU 8%, CH 1%, SI 0%
- **CU lands:** OUT-DN-1B 50%, OUT-UP-3B 11%, OUT-DN-3B 8%
- **FC lands:** OUT-DN-1B 33%, MID-AWAY 10%, HEART 9%
- **FF lands:** OUT-UP-1B 18%, OUT-UP-3B 17%, OUT-DN-1B 12%
- **SL lands:** OUT-DN-1B 36%, LO-AWAY 15%, MID-AWAY 8%
- **Zone → pitch mix:** OUT-DN-1B (22% throws → FF 33%+SL 29%); OUT-UP-3B (13% throws → FF 80%+SL 8%); OUT-UP-1B (12% throws → FF 88%+FC 5%); MID-AWAY (8% throws → FF 64%+SL 18%)
- **Dump (ticket tunnel):** OUT-DN-1B 21.6% FF+SL · chase; OUT-UP-3B 13.4% FF+SL · chase

## Dump × swing (vs LHB / RHB)

Pitcher’s #1 throw pocket vs that batter’s hand, crossed with whether they **swing** there. TUNNEL = Hits location. MISTAKE = hunt middle, not the dump. CHASE/TAKE = not a Hits lean on the tunnel (K / take).

| Batter | Stand | Dump | Throw | Swing | Whiff | xwOBA | Fit |
|--------|-------|------|-------|-------|-------|-------|-----|
| Junior Caminero | R | OUT-DN-1B | 21.6% FF+SL | 27.1 | 51.4 | 0.197 | **MISTAKE** |
| Yandy Díaz | R | OUT-DN-1B | 21.6% FF+SL | 26.4 | 21.5 | 0.272 | **MISTAKE** |
| Jonathan Aranda | L | OUT-UP-3B | 21.2% FF+CU | 14.3 | 37.9 | 0.13 | **MISTAKE** |
| Liam Hicks | L | OUT-UP-3B | 21.2% FF+CU | 20.3 | 11.3 | 0.206 | **MISTAKE** |
| Victor Mesa Jr. | L | OUT-UP-3B | 21.2% FF+CU | 21.5 | 56.2 | nan | **MISTAKE** |
| Chandler Simpson | L | OUT-UP-3B | 21.2% FF+CU | 24.3 | 3.8 | 0.211 | **TAKE** |
| Jonny DeLuca | R | OUT-DN-1B | 21.6% FF+SL | 34.1 | 48.7 | 0.221 | **MISTAKE** |
| Ben Williamson | R | OUT-DN-1B | 21.6% FF+SL | 20.8 | 45.5 | 0.232 | **MISTAKE** |
| Taylor Walls | L | OUT-UP-3B | 21.2% FF+CU | 23.2 | 29.3 | 0.343 | **MISTAKE** |

## Batter heat vs opposing hand → overlap

### Junior Caminero (stand R, vs RHP, season n=2113, recent n=150)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone MID-AWAY/HI-AWAY (1B) (swing 27.1% · whiff 51.4% · xwOBA 0.197)
- Swing 46.2% · whiff/swing 23.6%
- **Top swing (season):** MID-IN 75.9%; HEART 74.6%; HI-IN (3B) 71.2%; LO-IN 65.3%
- **Top damage season (xwOBA BIP):** HI-MID 0.535 (EV 100.0, brl 26.1%, BIP 23); HI-AWAY (1B) 0.532 (EV 102.9, brl 30.0%, BIP 10); OUT-UP-1B 0.502 (EV 90.5, brl 20.0%, BIP 25); LO-MID 0.469 (EV 92.8, brl 13.6%, BIP 22)
- **Top damage recent (30d):** OUT-DN-1B 0.081 (BIP 6)
- **HOT/WARM overlap:** WARM MID-AWAY (W 7.8%, xwOBA 0.363, recent HOT xwOBA 0.545 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-UP-1B (W 12.3%, xwOBA 0.502, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT HI-AWAY (1B) (W 7.4%, xwOBA 0.532, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-MID (W 6.8%, xwOBA 0.535 · SEASON_ONLY); HOT HEART (W 7.3%, xwOBA 0.462, recent — xwOBA nan BIP 1 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 21.6%, xwOBA 0.197, recent COLD · CONFIRM)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-1B, WARM MID-AWAY

### Yandy Díaz (stand R, vs RHP, season n=2028, recent n=146)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone HEART/HI-AWAY (1B) (swing 26.4% · whiff 21.5% · xwOBA 0.272)
- Swing 47.6% · whiff/swing 13.1%
- **Top swing (season):** HI-MID 77.4%; MID-IN 76.9%; HI-IN (3B) 66.7%; HEART 66.0%
- **Top damage season (xwOBA BIP):** HEART 0.658 (EV 101.0, brl 27.0%, BIP 37); HI-AWAY (1B) 0.496 (EV 98.4, brl 21.4%, BIP 14); HI-MID 0.472 (EV 96.6, brl 25.0%, BIP 20); LO-IN 0.426 (EV 93.8, brl 9.5%, BIP 42)
- **HOT/WARM overlap:** HOT HEART (W 7.3%, xwOBA 0.658, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT HI-AWAY (1B) (W 7.4%, xwOBA 0.496, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-MID (W 6.8%, xwOBA 0.472 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 21.6%, xwOBA 0.272, recent — · SEASON_ONLY); OUT-UP-3B (W 13.4%, xwOBA 0.161, recent — · SEASON_ONLY)

### Jonathan Aranda (stand L, vs RHP, season n=2078, recent n=133)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-UP-3B; HOT in-zone HI-MID/HEART (swing 14.3% · whiff 37.9% · xwOBA 0.13)
- Swing 48.2% · whiff/swing 19.5%
- **Top swing (season):** LO-MID 78.8%; HI-MID 74.8%; HEART 73.1%; MID-AWAY 71.6%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.565 (EV 95.2, brl 14.3%, BIP 21); OUT-DN-1B 0.562 (EV 92.3, brl 17.2%, BIP 29); LO-MID 0.523 (EV 96.0, brl 17.3%, BIP 52); HI-MID 0.516 (EV 96.0, brl 13.6%, BIP 22)
- **HOT/WARM overlap:** HOT OUT-DN-1B (W 14.8%, xwOBA 0.562, recent — xwOBA nan BIP 0 · SEASON_ONLY); HOT HI-MID (W 7.8%, xwOBA 0.516, recent COLD xwOBA 0.222 BIP 4 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HEART (W 7.2%, xwOBA 0.495 · SEASON_ONLY); WARM LO-MID (W 5.4%, xwOBA 0.523, recent — xwOBA 0.334 BIP 3 · SEASON_ONLY); WARM HI-IN (3B) (W 6.2%, xwOBA 0.396 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-UP-1B (W 9.6%, xwOBA 0.224, recent — · SEASON_ONLY); OUT-UP-3B (W 21.2%, xwOBA 0.13, recent — · SEASON_ONLY)
- **Season vs recent CONFLICT:** HI-MID (HOT→COLD)

### Liam Hicks (stand L, vs RHP, season n=1723, recent n=111)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-UP-3B; HOT in-zone HEART/LO-MID (swing 20.3% · whiff 11.3% · xwOBA 0.206)
- Swing 41.9% · whiff/swing 10.4%
- **Top swing (season):** HI-MID 73.3%; HEART 68.6%; LO-AWAY 64.1%; HI-AWAY (1B) 62.5%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.535 (EV 86.7, brl 11.1%, BIP 9); LO-MID 0.434 (EV 91.7, brl 11.1%, BIP 36); HEART 0.365 (EV 90.0, brl 9.7%, BIP 62); MID-IN 0.353 (EV 92.2, brl 0.0%, BIP 40)
- **Top damage recent (30d):** HI-MID 0.222 (BIP 6)
- **HOT/WARM overlap:** WARM HEART (W 7.2%, xwOBA 0.365, recent WARM xwOBA 0.377 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-1B (W 14.8%, xwOBA 0.535, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM LO-MID (W 5.4%, xwOBA 0.434, recent — xwOBA 0.349 BIP 3 · SEASON_ONLY); WARM MID-IN (W 5.1%, xwOBA 0.353, recent — xwOBA nan BIP 1 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 21.2%, xwOBA 0.206, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** WARM HEART

### Victor Mesa Jr. (stand L, vs RHP, season n=795, recent n=114)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-UP-3B; HOT in-zone HEART/HI-MID (swing 21.5% · whiff 56.2% · xwOBA nan)
- Swing 56.2% · whiff/swing 24.4%
- **Top swing (season):** HEART 91.5%; MID-AWAY 88.0%; HI-MID 87.0%; MID-IN 80.5%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.637 (EV 95.5, brl 25.0%, BIP 12); HEART 0.563 (EV 94.8, brl 26.3%, BIP 19); OUT-DN-3B 0.429 (EV 86.4, brl 5.0%, BIP 20); LO-AWAY 0.425 (EV 85.3, brl 15.4%, BIP 13)
- **HOT/WARM overlap:** HOT HEART (W 7.2%, xwOBA 0.563, recent HOT xwOBA 0.456 BIP 4 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-1B (W 14.8%, xwOBA 0.637, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-MID (W 7.8%, xwOBA 0.418, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM LO-MID (W 5.4%, xwOBA 0.402, recent — xwOBA 0.145 BIP 4 · SEASON_ONLY); HOT HI-IN (3B) (W 6.2%, xwOBA 0.416 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **Season ∩ recent CONFIRM:** HOT HEART

### Chandler Simpson (stand L, vs RHP, season n=1435, recent n=63)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TAKE`** — takes dump OUT-UP-3B (swing 24.3%) — not a Hits lean on that pitch (swing 24.3% · whiff 3.8% · xwOBA 0.211)
- Swing 47.7% · whiff/swing 9.1%
- **Top swing (season):** HI-AWAY (1B) 90.0%; HEART 73.9%; HI-MID 73.2%; MID-AWAY 65.0%
- **Top damage season (xwOBA BIP):** HEART 0.349 (EV 84.4, brl 0.0%, BIP 48); LO-MID 0.324 (EV 80.7, brl 0.0%, BIP 36); MID-IN 0.323 (EV 80.2, brl 0.0%, BIP 38); OUT-DN-1B 0.319 (EV 76.7, brl 0.0%, BIP 9)
- **COLD vs his tunnel:** OUT-UP-3B (W 21.2%, xwOBA 0.211, recent COLD · CONFIRM); HI-MID (W 7.8%, xwOBA 0.262 · SEASON_ONLY); OUT-UP-1B (W 9.6%, xwOBA 0.197, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-UP-3B

### Jonny DeLuca (stand R, vs RHP, season n=927, recent n=119)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone HI-MID (swing 34.1% · whiff 48.7% · xwOBA 0.221)
- Swing 51.9% · whiff/swing 20.6%
- **Top swing (season):** HI-IN (3B) 78.0%; MID-AWAY 76.1%; HI-MID 75.4%; HEART 73.8%
- **Top damage season (xwOBA BIP):** HI-MID 0.497 (EV 93.8, brl 18.8%, BIP 16); LO-MID 0.415 (EV 94.6, brl 5.0%, BIP 20); MID-AWAY 0.329 (EV 91.8, brl 3.7%, BIP 27); MID-IN 0.310 (EV 79.3, brl 5.9%, BIP 17)
- **Top damage recent (30d):** MID-AWAY 0.299 (BIP 6); HEART 0.267 (BIP 6); LO-AWAY 0.263 (BIP 6)
- **HOT/WARM overlap:** HOT HI-MID (W 6.8%, xwOBA 0.497, recent — xwOBA nan BIP 2 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 21.6%, xwOBA 0.221, recent — · SEASON_ONLY); OUT-UP-1B (W 12.3%, xwOBA 0.259, recent — · SEASON_ONLY); HI-AWAY (1B) (W 7.4%, xwOBA 0.224 · SEASON_ONLY)

### Ben Williamson (stand R, vs RHP, season n=729, recent n=13)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone HI-MID/HEART (swing 20.8% · whiff 45.5% · xwOBA 0.232)
- Swing 40.3% · whiff/swing 15.0%
- **Top swing (season):** HI-IN (3B) 71.8%; HEART 67.3%; HI-MID 63.9%; MID-IN 57.1%
- **Top damage season (xwOBA BIP):** HI-MID 0.444 (EV 97.2, brl 8.3%, BIP 12); HEART 0.375 (EV 94.8, brl 5.0%, BIP 20); LO-MID 0.328 (EV 93.5, brl 0.0%, BIP 15); OUT-UP-3B 0.322 (EV 75.4, brl 0.0%, BIP 19)
- **HOT/WARM overlap:** HOT HI-MID (W 6.8%, xwOBA 0.444 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HEART (W 7.3%, xwOBA 0.375 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 21.6%, xwOBA 0.232 · SEASON_ONLY); MID-AWAY (W 7.8%, xwOBA 0.266 · SEASON_ONLY)

### Taylor Walls (stand L, vs RHP, season n=1243, recent n=94)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-UP-3B; HOT in-zone HI-IN (3B)/MID-AWAY (swing 23.2% · whiff 29.3% · xwOBA 0.343)
- Swing 41.9% · whiff/swing 22.8%
- **Top swing (season):** HEART 74.0%; HI-MID 65.4%; MID-IN 65.2%; HI-IN (3B) 60.9%
- **Top damage season (xwOBA BIP):** MID-IN 0.387 (EV 86.9, brl 16.7%, BIP 24); HI-IN (3B) 0.373 (EV 86.1, brl 5.9%, BIP 17); MID-AWAY 0.350 (EV 81.2, brl 10.0%, BIP 10); LO-MID 0.345 (EV 81.0, brl 10.5%, BIP 19)
- **HOT/WARM overlap:** WARM HI-IN (3B) (W 6.2%, xwOBA 0.373 · SEASON_ONLY); WARM MID-AWAY (W 6.2%, xwOBA 0.35 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM MID-IN (W 5.1%, xwOBA 0.387 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 14.8%, xwOBA 0.175, recent — · SEASON_ONLY); OUT-UP-1B (W 9.6%, xwOBA 0.193, recent — · SEASON_ONLY)

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | Exp H | P(1+) | PA | RBI | HR/RBI | Zone note |
|------|--------|------|-------|-------|----|-----|--------|-----------|
| 4 | Junior Caminero | 59.5 | 0.35 | 32% | 2 | good | 60.3 | MISTAKE OUT-DN-1B; CONFIRM COLD OUT-DN-1B/WARM MID-AWAY; COLD OUT-DN-1B |
| 1 | Yandy Díaz | 59.0 | 0.53 | 44% | 3 | thin | 57.1 | MISTAKE OUT-DN-1B; HOT HEART/HI-AWAY (1B); COLD OUT-DN-1B |
| 2 | Jonathan Aranda | 57.0 | 0.48 | 41% | 3 | good | 56.1 | MISTAKE OUT-UP-3B; HOT OUT-DN-1B/HI-MID; COLD OUT-UP-1B; CONFLICT HI-MID |
| 5 | Liam Hicks | 52.1 | 0.42 | 37% | 2 | good | 47.6 | MISTAKE OUT-UP-3B; CONFIRM WARM HEART; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 7 | Victor Mesa Jr. | 51.0 | 0.30 | 28% | 2 | thin | 52.2 | MISTAKE OUT-UP-3B; CONFIRM HOT HEART; LOW_SAMPLE_RECENT |
| 3 | Chandler Simpson | 46.2 | 0.71 | 56% | 3 | good | 39.2 | TAKE OUT-UP-3B; CONFIRM COLD OUT-UP-3B; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 6 | Jonny DeLuca | 45.3 | 0.37 | 33% | 2 | thin | 41.9 | MISTAKE OUT-DN-1B; HOT HI-MID; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |
| 8 | Ben Williamson | 44.7 | 0.37 | 34% | 2 | thin | 42.7 | MISTAKE OUT-DN-1B; HOT HI-MID; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |
| 9 | Taylor Walls | 38.1 | 0.26 | 24% | 2 | thin | 35.1 | MISTAKE OUT-UP-3B; WARM HI-IN (3B)/MID-AWAY; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM **TUNNEL** HOTs; MISTAKE = heart/in-zone, not the dump. Treat `LOW_SAMPLE_*` as sizing FYI.*

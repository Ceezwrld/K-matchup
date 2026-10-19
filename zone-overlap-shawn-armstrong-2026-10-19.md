# Zone overlap — vs Shawn Armstrong (2026 Statcast)

**Game:** CLE@TB
**Pitcher:** Shawn Armstrong (RHP, id 542888) · n=824 pitches
**Windows:** season + **last 30d** (pitcher recent n=117)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter damage; **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** ST 31% / FF 30% / FC 22% / SI 18%
**Velo:** FC ~89.9, FF ~93.3, SI ~93.6, ST ~84.4

## Where the pitcher throws

### vs LHB — in-zone 57% · heart 8% · mean px=-0.146 (neg=3B) pz=2.634

- Top zones: OUT-UP-3B 22%, OUT-DN-1B 11%, HI-IN (3B) 10%, HI-MID 9%, MID-IN 9%, HEART 8%
- **Usage vs this hand:** FF 38%, FC 28%, ST 26%, SI 8%
- **FC lands:** OUT-DN-1B 21%, HI-MID 11%, OUT-UP-1B 11%
- **FF lands:** OUT-UP-3B 34%, HI-IN (3B) 17%, HI-MID 12%
- **SI lands:** OUT-UP-3B 41%, OUT-DN-3B 12%, LO-IN 9%
- **ST lands:** OUT-DN-1B 16%, MID-IN 14%, OUT-UP-3B 12%
- **Zone → pitch mix:** OUT-UP-3B (22% throws → FF 59%+SI 15%); OUT-DN-1B (11% throws → FC 52%+ST 38%); HI-IN (3B) (10% throws → FF 64%+ST 15%); HI-MID (9% throws → FF 47%+FC 33%)

### vs RHB — in-zone 49% · heart 8% · mean px=0.456 (neg=3B) pz=2.322

- Top zones: OUT-DN-1B 28%, OUT-UP-3B 10%, MID-AWAY 10%, OUT-UP-1B 10%, HEART 8%, LO-AWAY 7%
- **Usage vs this hand:** ST 35%, SI 26%, FF 23%, FC 16%
- **FC lands:** OUT-DN-1B 24%, MID-AWAY 18%, HEART 14%
- **FF lands:** OUT-UP-3B 25%, OUT-UP-1B 13%, HI-AWAY (1B) 10%
- **SI lands:** OUT-DN-1B 25%, OUT-UP-3B 13%, MID-AWAY 11%
- **ST lands:** OUT-DN-1B 44%, LO-AWAY 9%, OUT-UP-1B 8%
- **Zone → pitch mix:** OUT-DN-1B (28% throws → ST 55%+SI 24%); OUT-UP-3B (10% throws → FF 54%+SI 33%); MID-AWAY (10% throws → FC 29%+ST 29%); OUT-UP-1B (10% throws → ST 30%+FF 30%)

## Batter heat vs opposing hand → overlap

### Junior Caminero (stand R, vs RHP, season n=2107, recent n=170)
- Swing 46.2% · whiff/swing 23.7%
- **Top swing (season):** MID-IN 75.9%; HEART 74.6%; HI-IN (3B) 71.2%; LO-IN 65.3%
- **Top damage season (xwOBA BIP):** HI-MID 0.535 (EV 100.0, brl 26.1%, BIP 23); HI-AWAY (1B) 0.532 (EV 102.9, brl 30.0%, BIP 10); OUT-UP-1B 0.474 (EV 89.8, brl 16.7%, BIP 24); LO-MID 0.469 (EV 92.8, brl 13.6%, BIP 22)
- **Top damage recent (30d):** OUT-DN-1B 0.080 (BIP 7)
- **HOT/WARM overlap:** WARM MID-AWAY (W 10.2%, xwOBA 0.363, recent HOT xwOBA 0.545 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-UP-1B (W 9.8%, xwOBA 0.474, recent — xwOBA nan BIP 1 · SEASON_ONLY); HOT HEART (W 7.7%, xwOBA 0.462, recent — xwOBA nan BIP 1 · SEASON_ONLY); HOT HI-AWAY (1B) (W 6.4%, xwOBA 0.532, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-MID (W 5.2%, xwOBA 0.535, recent — xwOBA 0.144 BIP 3 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 28.0%, xwOBA 0.197, recent COLD · CONFIRM)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-1B, WARM MID-AWAY

### Yandy Díaz (stand R, vs RHP, season n=2021, recent n=155)
- Swing 47.6% · whiff/swing 13.2%
- **Top swing (season):** MID-IN 77.6%; HI-MID 77.4%; HI-IN (3B) 66.3%; HEART 66.0%
- **Top damage season (xwOBA BIP):** HEART 0.658 (EV 101.0, brl 27.0%, BIP 37); HI-AWAY (1B) 0.496 (EV 98.4, brl 21.4%, BIP 14); HI-MID 0.472 (EV 96.6, brl 25.0%, BIP 20); HI-IN (3B) 0.438 (EV 88.6, brl 0.0%, BIP 12)
- **HOT/WARM overlap:** HOT HEART (W 7.7%, xwOBA 0.658, recent HOT xwOBA 0.612 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HI-AWAY (1B) (W 6.4%, xwOBA 0.496, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-MID (W 5.2%, xwOBA 0.472 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 28.0%, xwOBA 0.272, recent — · SEASON_ONLY); OUT-UP-3B (W 10.5%, xwOBA 0.161, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT HEART

### Jonathan Aranda (stand L, vs RHP, season n=2070, recent n=147)
- Swing 48.2% · whiff/swing 19.5%
- **Top swing (season):** LO-MID 79.3%; HI-MID 74.6%; HEART 73.1%; MID-AWAY 72.3%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.565 (EV 95.2, brl 14.3%, BIP 21); OUT-DN-1B 0.562 (EV 92.3, brl 17.2%, BIP 29); HI-MID 0.532 (EV 97.4, brl 14.3%, BIP 21); LO-MID 0.523 (EV 96.0, brl 17.3%, BIP 52)
- **HOT/WARM overlap:** HOT OUT-DN-1B (W 10.9%, xwOBA 0.562, recent — xwOBA nan BIP 0 · SEASON_ONLY); HOT HI-MID (W 9.3%, xwOBA 0.532, recent COLD xwOBA 0.233 BIP 3 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM HI-IN (3B) (W 10.1%, xwOBA 0.396 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT MID-IN (W 8.6%, xwOBA 0.452, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT LO-AWAY (W 6.8%, xwOBA 0.565 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 22.3%, xwOBA 0.13, recent — · SEASON_ONLY)
- **Season vs recent CONFLICT:** HI-MID (HOT→COLD)

### Liam Hicks (stand L, vs RHP, season n=1714, recent n=109)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 41.9% · whiff/swing 10.4%
- **Top swing (season):** HI-MID 73.3%; HEART 68.4%; LO-AWAY 65.1%; HI-AWAY (1B) 61.7%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.535 (EV 86.7, brl 11.1%, BIP 9); LO-MID 0.434 (EV 91.7, brl 11.1%, BIP 36); HEART 0.369 (EV 90.1, brl 9.8%, BIP 61); MID-IN 0.353 (EV 92.2, brl 0.0%, BIP 40)
- **Top damage recent (30d):** HI-MID 0.321 (BIP 7)
- **HOT/WARM overlap:** HOT OUT-DN-1B (W 10.9%, xwOBA 0.535, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM MID-IN (W 8.6%, xwOBA 0.353, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM HEART (W 7.5%, xwOBA 0.369, recent — xwOBA nan BIP 2 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 22.3%, xwOBA 0.206, recent — · SEASON_ONLY); HI-IN (3B) (W 10.1%, xwOBA 0.228 · SEASON_ONLY)

### Chandler Simpson (stand L, vs RHP, season n=1428, recent n=67)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 47.8% · whiff/swing 9.1%
- **Top swing (season):** HI-AWAY (1B) 90.0%; HEART 73.7%; HI-MID 72.9%; MID-AWAY 65.0%
- **Top damage season (xwOBA BIP):** HEART 0.354 (EV 84.9, brl 0.0%, BIP 47); LO-MID 0.324 (EV 80.7, brl 0.0%, BIP 36); MID-IN 0.323 (EV 80.2, brl 0.0%, BIP 38); OUT-DN-1B 0.319 (EV 76.7, brl 0.0%, BIP 9)
- **HOT/WARM overlap:** WARM HEART (W 7.5%, xwOBA 0.354, recent WARM xwOBA 0.376 BIP 4 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]
- **COLD vs his tunnel:** OUT-UP-3B (W 22.3%, xwOBA 0.211, recent COLD · CONFIRM); HI-MID (W 9.3%, xwOBA 0.264 · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-UP-3B, WARM HEART

### Ryan Vilade (stand R, vs RHP, season n=583, recent n=47)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 45.8% · whiff/swing 20.2%
- **Top swing (season):** HEART 82.1%; LO-MID 75.9%; HI-MID 75.8%; MID-IN 74.2%
- **Top damage season (xwOBA BIP):** HEART 0.542 (EV 98.1, brl 11.8%, BIP 17); LO-MID 0.480 (EV 93.2, brl 16.7%, BIP 12); MID-AWAY 0.450 (EV 90.7, brl 12.5%, BIP 8); MID-IN 0.336 (EV 85.2, brl 7.1%, BIP 14)
- **HOT/WARM overlap:** HOT MID-AWAY (W 10.2%, xwOBA 0.45 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 7.7%, xwOBA 0.542 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 10.5%, xwOBA 0.143 · SEASON_ONLY)

### Jonny DeLuca (stand R, vs RHP, season n=923, recent n=122)
- Swing 51.9% · whiff/swing 20.7%
- **Top swing (season):** HI-IN (3B) 78.0%; MID-AWAY 76.1%; HI-MID 75.4%; MID-IN 73.8%
- **Top damage season (xwOBA BIP):** HI-MID 0.497 (EV 93.8, brl 18.8%, BIP 16); LO-MID 0.415 (EV 94.6, brl 5.0%, BIP 20); MID-AWAY 0.329 (EV 91.8, brl 3.7%, BIP 27); MID-IN 0.310 (EV 79.3, brl 5.9%, BIP 17)
- **Top damage recent (30d):** MID-AWAY 0.299 (BIP 6); LO-AWAY 0.263 (BIP 6); HEART 0.229 (BIP 5)
- **HOT/WARM overlap:** WARM HI-MID (W 5.2%, xwOBA 0.497, recent — xwOBA nan BIP 2 · SEASON_ONLY)
- **COLD vs his tunnel:** HEART (W 7.7%, xwOBA 0.216, recent COLD · CONFIRM); OUT-DN-1B (W 28.0%, xwOBA 0.224, recent — · SEASON_ONLY); OUT-UP-1B (W 9.8%, xwOBA 0.259, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD HEART

### Ben Williamson (stand R, vs RHP, season n=729, recent n=13)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 40.3% · whiff/swing 15.0%
- **Top swing (season):** HI-IN (3B) 71.8%; HEART 67.3%; HI-MID 63.9%; MID-IN 57.1%
- **Top damage season (xwOBA BIP):** HI-MID 0.444 (EV 97.2, brl 8.3%, BIP 12); HEART 0.375 (EV 94.8, brl 5.0%, BIP 20); LO-MID 0.328 (EV 93.5, brl 0.0%, BIP 15); OUT-UP-3B 0.322 (EV 75.4, brl 0.0%, BIP 19)
- **HOT/WARM overlap:** WARM HEART (W 7.7%, xwOBA 0.375 · SEASON_ONLY); WARM HI-MID (W 5.2%, xwOBA 0.444 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-1B (W 28.0%, xwOBA 0.232 · SEASON_ONLY); MID-AWAY (W 10.2%, xwOBA 0.266 · SEASON_ONLY)

### Taylor Walls (stand L, vs RHP, season n=1231, recent n=87)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 42.2% · whiff/swing 22.9%
- **Top swing (season):** HEART 74.0%; HI-MID 66.2%; MID-IN 65.2%; HI-IN (3B) 60.9%
- **Top damage season (xwOBA BIP):** MID-IN 0.387 (EV 86.9, brl 16.7%, BIP 24); HI-IN (3B) 0.373 (EV 86.1, brl 5.9%, BIP 17); MID-AWAY 0.350 (EV 81.2, brl 10.0%, BIP 10); LO-MID 0.345 (EV 81.0, brl 10.5%, BIP 19)
- **HOT/WARM overlap:** WARM HI-IN (3B) (W 10.1%, xwOBA 0.373 · SEASON_ONLY); WARM MID-IN (W 8.6%, xwOBA 0.387 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 10.9%, xwOBA 0.175, recent — · SEASON_ONLY)

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | HR/RBI | AVG vs hand | Barrel | HH | Zone note |
|------|--------|------|--------|-------------|--------|----|-----------|
| 4 | Junior Caminero | 59.5 | 60.3 | 0.272 | 13.1% | 49.7% | CONFIRM COLD OUT-DN-1B/WARM MID-AWAY; COLD OUT-DN-1B |
| 1 | Yandy Díaz | 59.0 | 57.1 | 0.305 | 7.1% | 48.1% | CONFIRM HOT HEART; COLD OUT-DN-1B |
| 2 | Jonathan Aranda | 57.0 | 56.1 | 0.284 | 9.9% | 46.0% | HOT OUT-DN-1B/HI-MID; COLD OUT-UP-3B; CONFLICT HI-MID |
| 7 | Liam Hicks | 52.1 | 47.6 | 0.309 | 3.7% | 27.1% | HOT OUT-DN-1B; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 5 | Chandler Simpson | 46.2 | 39.2 | 0.318 | 0.0% | 13.6% | CONFIRM COLD OUT-UP-3B/WARM HEART; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 3 | Ryan Vilade | 45.6 | 47.7 | 0.202 | 7.1% | 39.9% | HOT MID-AWAY/HEART; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 6 | Jonny DeLuca | 45.3 | 41.9 | 0.267 | 3.6% | 30.2% | CONFIRM COLD HEART; COLD HEART |
| 8 | Ben Williamson | 44.7 | 42.7 | 0.250 | 1.9% | 33.2% | WARM HEART/HI-MID; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |
| 9 | Taylor Walls | 38.1 | 35.1 | 0.233 | 2.1% | 21.9% | WARM HI-IN (3B)/MID-IN; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM HOTs; treat `LOW_SAMPLE_*` as sizing FYI.*

# Zone overlap — vs Nick Martinez (2026 Statcast)

**Game:** TB@CLE
**Pitcher:** Nick Martinez (RHP, id 607259) · n=2849 pitches
**Windows:** season + **last 30d** (pitcher recent n=207)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter damage; **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** SI 31% / CH 26% / FC 22% / FF 13% / SL 4% / CU 4% / PO 0%
**Velo:** CH ~78.2, CU ~79.9, FC ~89.2, FF ~92.7, PO ~93.2, SI ~92.4, SL ~85.2

## Where the pitcher throws

### vs LHB — in-zone 54% · heart 8% · mean px=-0.027 (neg=3B) pz=2.393

- Top zones: OUT-DN-3B 14%, OUT-UP-1B 11%, OUT-UP-3B 11%, OUT-DN-1B 10%, HEART 8%, MID-AWAY 7%
- **Usage vs this hand:** CH 29%, SI 25%, FC 22%, FF 14%, SL 5%, CU 4%, PO 0%
- **CH lands:** OUT-DN-3B 36%, OUT-UP-3B 16%, LO-IN 10%
- **CU lands:** OUT-UP-3B 17%, OUT-DN-3B 17%, OUT-DN-1B 17%
- **FC lands:** OUT-UP-1B 18%, OUT-DN-1B 15%, MID-AWAY 14%
- **FF lands:** OUT-UP-3B 19%, OUT-UP-1B 13%, MID-IN 11%
- **SI lands:** OUT-UP-1B 19%, HI-AWAY (1B) 15%, MID-AWAY 13%
- **SL lands:** OUT-DN-3B 24%, OUT-DN-1B 16%, HEART 13%
- **Zone → pitch mix:** OUT-DN-3B (14% throws → CH 75%+SL 8%); OUT-UP-1B (11% throws → SI 42%+FC 36%); OUT-UP-3B (11% throws → CH 43%+FF 26%); OUT-DN-1B (10% throws → FC 33%+CH 24%)

### vs RHB — in-zone 51% · heart 8% · mean px=-0.027 (neg=3B) pz=2.189

- Top zones: OUT-DN-1B 18%, OUT-UP-3B 13%, OUT-DN-3B 12%, HEART 8%, LO-MID 6%, LO-AWAY 6%
- **Usage vs this hand:** SI 38%, CH 22%, FC 21%, FF 11%, SL 4%, CU 4%
- **CH lands:** OUT-DN-3B 33%, OUT-DN-1B 24%, OUT-UP-3B 7%
- **CU lands:** OUT-DN-1B 21%, OUT-DN-3B 21%, OUT-UP-3B 19%
- **FC lands:** OUT-DN-1B 31%, MID-AWAY 15%, HEART 11%
- **FF lands:** OUT-UP-1B 29%, OUT-UP-3B 22%, HI-MID 12%
- **SI lands:** OUT-UP-3B 19%, HI-IN (3B) 10%, MID-IN 10%
- **SL lands:** OUT-DN-1B 52%, LO-AWAY 12%, LO-MID 10%
- **Zone → pitch mix:** OUT-DN-1B (18% throws → FC 36%+CH 29%); OUT-UP-3B (13% throws → SI 58%+FF 19%); OUT-DN-3B (12% throws → CH 59%+SI 30%); HEART (8% throws → SI 46%+FC 32%)

## Batter heat vs opposing hand → overlap

### Chase DeLauter (stand L, vs RHP, season n=1654, recent n=162)
- Swing 41.8% · whiff/swing 12.0%
- **Top swing (season):** HI-AWAY (1B) 94.7%; HEART 82.5%; MID-AWAY 75.7%; HI-MID 75.4%
- **Top damage season (xwOBA BIP):** HI-AWAY (1B) 0.481 (EV 86.2, brl 7.7%, BIP 13); MID-AWAY 0.456 (EV 92.7, brl 10.3%, BIP 29); LO-AWAY 0.450 (EV 96.0, brl 13.8%, BIP 29); HI-IN (3B) 0.428 (EV 96.3, brl 14.3%, BIP 14)
- **Top damage recent (30d):** HEART 0.390 (BIP 6)
- **HOT/WARM overlap:** HOT MID-AWAY (W 7.3%, xwOBA 0.456, recent WARM xwOBA 0.403 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM OUT-UP-3B (W 10.8%, xwOBA 0.37, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM OUT-DN-1B (W 10.2%, xwOBA 0.37, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-AWAY (1B) (W 6.0%, xwOBA 0.481, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-MID (W 7.1%, xwOBA 0.397, recent — xwOBA 0.398 BIP 4 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-3B (W 14.0%, xwOBA 0.222, recent — · SEASON_ONLY); OUT-UP-1B (W 11.2%, xwOBA 0.2, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT MID-AWAY

### Nathaniel Lowe (stand L, vs RHP, season n=1786, recent n=138)
- Swing 45.4% · whiff/swing 19.0%
- **Top swing (season):** HI-MID 77.5%; HEART 73.9%; HI-AWAY (1B) 72.2%; MID-AWAY 63.9%
- **Top damage season (xwOBA BIP):** HEART 0.596 (EV 96.7, brl 19.5%, BIP 41); HI-IN (3B) 0.507 (EV 96.1, brl 11.8%, BIP 17); MID-IN 0.502 (EV 95.4, brl 13.6%, BIP 22); LO-AWAY 0.470 (EV 95.1, brl 13.6%, BIP 22)
- **Top damage recent (30d):** MID-AWAY 0.348 (BIP 6)
- **HOT/WARM overlap:** WARM OUT-DN-3B (W 14.0%, xwOBA 0.373 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 8.2%, xwOBA 0.596, recent — xwOBA 0.29 BIP 3 · SEASON_ONLY); HOT MID-AWAY (W 7.3%, xwOBA 0.448, recent — xwOBA 0.348 BIP 6 · SEASON_ONLY); HOT MID-IN (W 6.4%, xwOBA 0.502, recent — xwOBA nan BIP 2 · SEASON_ONLY); WARM LO-MID (W 5.3%, xwOBA 0.464, recent — xwOBA 0.361 BIP 4 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-1B (W 11.2%, xwOBA 0.164, recent — · SEASON_ONLY); OUT-UP-3B (W 10.8%, xwOBA 0.135, recent — · SEASON_ONLY)

### Travis Bazzana (stand L, vs RHP, season n=1520, recent n=130)
- Swing 45.8% · whiff/swing 21.4%
- **Top swing (season):** MID-AWAY 85.7%; HEART 82.9%; LO-AWAY 79.7%; HI-MID 79.2%
- **Top damage season (xwOBA BIP):** MID-AWAY 0.497 (EV 94.1, brl 15.8%, BIP 19); HEART 0.429 (EV 96.2, brl 12.0%, BIP 50); MID-IN 0.348 (EV 86.9, brl 6.9%, BIP 29); HI-MID 0.324 (EV 91.9, brl 13.0%, BIP 23)
- **Top damage recent (30d):** LO-IN 0.331 (BIP 5); HEART 0.290 (BIP 8)
- **HOT/WARM overlap:** HOT MID-AWAY (W 7.3%, xwOBA 0.497 · SEASON_ONLY); HOT HEART (W 8.2%, xwOBA 0.429, recent — xwOBA 0.29 BIP 8 · SEASON_ONLY); HOT OUT-UP-1B (W 11.2%, xwOBA 0.53, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 14.0%, xwOBA 0.247, recent — · SEASON_ONLY); OUT-UP-3B (W 10.8%, xwOBA 0.192, recent — · SEASON_ONLY)

### Jo Adell (stand R, vs RHP, season n=2074, recent n=173)
- Swing 52.9% · whiff/swing 25.5%
- **Top swing (season):** HEART 82.9%; LO-MID 76.5%; MID-AWAY 74.8%; HI-MID 73.6%
- **Top damage season (xwOBA BIP):** HI-AWAY (1B) 0.470 (EV 99.3, brl 0.0%, BIP 15); LO-MID 0.462 (EV 97.8, brl 11.8%, BIP 34); OUT-DN-3B 0.445 (EV 88.2, brl 15.4%, BIP 13); MID-AWAY 0.434 (EV 95.0, brl 13.2%, BIP 38)
- **Top damage recent (30d):** HEART 0.120 (BIP 8)
- **HOT/WARM overlap:** HOT LO-AWAY (W 6.3%, xwOBA 0.403, recent WARM xwOBA 0.494 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM MID-AWAY (W 5.4%, xwOBA 0.434, recent HOT xwOBA 0.656 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-3B (W 12.1%, xwOBA 0.445, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT LO-MID (W 6.5%, xwOBA 0.462, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM HI-MID (W 5.4%, xwOBA 0.43, recent — xwOBA nan BIP 2 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 12.7%, xwOBA 0.2, recent COLD · CONFIRM)
- **Season ∩ recent CONFIRM:** HOT LO-AWAY, COLD OUT-UP-3B, WARM MID-AWAY

### Steven Kwan (stand L, vs RHP, season n=2056, recent n=199)
- Swing 35.9% · whiff/swing 5.3%
- **Top swing (season):** HEART 62.7%; LO-IN 58.2%; MID-IN 55.5%; HI-MID 55.3%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.439 (EV 87.5, brl 0.0%, BIP 16); LO-MID 0.353 (EV 89.4, brl 0.0%, BIP 45); HI-MID 0.350 (EV 82.9, brl 0.0%, BIP 36); LO-IN 0.345 (EV 85.1, brl 0.0%, BIP 32)
- **Top damage recent (30d):** HEART 0.423 (BIP 6); MID-IN 0.266 (BIP 5)
- **HOT/WARM overlap:** WARM HI-MID (W 7.1%, xwOBA 0.35, recent — xwOBA 0.46 BIP 4 · SEASON_ONLY); WARM LO-MID (W 5.3%, xwOBA 0.353, recent — xwOBA nan BIP 1 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-3B (W 14.0%, xwOBA 0.275, recent COLD · CONFIRM); OUT-UP-3B (W 10.8%, xwOBA 0.242, recent COLD · CONFIRM); OUT-UP-1B (W 11.2%, xwOBA 0.247, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-3B, COLD OUT-UP-3B

### Brayan Rocchio (stand L, vs RHP, season n=1750, recent n=133)
- Swing 47.5% · whiff/swing 19.5%
- **Top swing (season):** HI-AWAY (1B) 75.0%; HEART 74.3%; HI-MID 72.9%; LO-MID 71.3%
- **Top damage season (xwOBA BIP):** HI-IN (3B) 0.410 (EV 90.0, brl 5.0%, BIP 20); LO-MID 0.330 (EV 95.1, brl 4.8%, BIP 42); LO-AWAY 0.330 (EV 89.5, brl 9.1%, BIP 11); OUT-UP-1B 0.316 (EV 71.0, brl 0.0%, BIP 9)
- **Top damage recent (30d):** MID-IN 0.099 (BIP 5)
- **COLD vs his tunnel:** OUT-DN-1B (W 10.2%, xwOBA 0.28, recent — · SEASON_ONLY); OUT-UP-3B (W 10.8%, xwOBA 0.231, recent — · SEASON_ONLY)

### Patrick Bailey (stand L, vs RHP, season n=1263, recent n=128)
- Swing 51.1% · whiff/swing 23.4%
- **Top swing (season):** HI-MID 84.5%; MID-IN 73.8%; HEART 72.2%; HI-IN (3B) 71.7%
- **Top damage season (xwOBA BIP):** HI-MID 0.645 (EV 93.7, brl 21.7%, BIP 23); HEART 0.526 (EV 94.8, brl 19.4%, BIP 36); HI-IN (3B) 0.498 (EV 95.6, brl 0.0%, BIP 11); MID-AWAY 0.442 (EV 91.4, brl 6.2%, BIP 16)
- **Top damage recent (30d):** HI-MID 0.743 (BIP 5); OUT-DN-3B 0.507 (BIP 5)
- **HOT/WARM overlap:** WARM MID-IN (W 6.4%, xwOBA 0.378, recent WARM xwOBA 0.769 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HI-MID (W 7.1%, xwOBA 0.645, recent — xwOBA 0.743 BIP 5 · SEASON_ONLY); HOT HEART (W 8.2%, xwOBA 0.526, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM OUT-UP-3B (W 10.8%, xwOBA 0.373, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT MID-AWAY (W 7.3%, xwOBA 0.442 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-1B (W 11.2%, xwOBA 0.234 · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** WARM MID-IN

### Petey Halpin (stand L, vs RHP, season n=652, recent n=89)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 58.3% · whiff/swing 21.8%
- **Top swing (season):** HI-MID 90.3%; MID-IN 86.8%; HEART 86.5%; LO-AWAY 81.6%
- **Top damage season (xwOBA BIP):** OUT-DN-3B 0.525 (EV 84.5, brl 6.7%, BIP 15); MID-AWAY 0.497 (EV 85.9, brl 7.7%, BIP 13); MID-IN 0.470 (EV 90.5, brl 22.2%, BIP 9); LO-IN 0.404 (EV 87.7, brl 7.1%, BIP 14)
- **HOT/WARM overlap:** HOT OUT-DN-3B (W 14.0%, xwOBA 0.525, recent — xwOBA None BIP 1 · SEASON_ONLY); HOT OUT-UP-3B (W 10.8%, xwOBA 0.533, recent — xwOBA None BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT MID-AWAY (W 7.3%, xwOBA 0.497 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT MID-IN (W 6.4%, xwOBA 0.47 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HEART (W 8.2%, xwOBA 0.35 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 10.2%, xwOBA 0.211 · SEASON_ONLY); HI-MID (W 7.1%, xwOBA 0.175 · SEASON_ONLY)

### José Ramírez (stand L, vs RHP, season n=1832, recent n=170)
- Swing 44.9% · whiff/swing 14.9%
- **Top swing (season):** HEART 73.6%; HI-MID 72.5%; LO-IN 67.9%; LO-MID 67.2%
- **Top damage season (xwOBA BIP):** OUT-UP-3B 0.484 (EV 91.8, brl 16.7%, BIP 18); LO-AWAY 0.400 (EV 83.6, brl 7.7%, BIP 13); MID-IN 0.394 (EV 94.5, brl 2.7%, BIP 37); OUT-DN-1B 0.352 (EV 80.4, brl 0.0%, BIP 13)
- **Top damage recent (30d):** LO-MID 0.592 (BIP 5); HEART 0.309 (BIP 5); MID-IN 0.222 (BIP 5); LO-IN 0.142 (BIP 6)
- **HOT/WARM overlap:** HOT OUT-UP-3B (W 10.8%, xwOBA 0.484, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM OUT-DN-1B (W 10.2%, xwOBA 0.352, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM MID-IN (W 6.4%, xwOBA 0.394, recent — xwOBA 0.222 BIP 5 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-3B (W 14.0%, xwOBA 0.236, recent COLD · CONFIRM); OUT-UP-1B (W 11.2%, xwOBA 0.25, recent COLD · CONFIRM); MID-AWAY (W 7.3%, xwOBA 0.23, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-3B, COLD OUT-UP-1B

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | HR/RBI | AVG vs hand | Barrel | HH | Zone note |
|------|--------|------|--------|-------------|--------|----|-----------|
| 3 | Chase DeLauter | 54.5 | 54.2 | 0.269 | 6.3% | 46.3% | CONFIRM HOT MID-AWAY; COLD OUT-DN-3B |
| 5 | Nathaniel Lowe | 54.1 | 53.3 | 0.271 | 8.3% | 41.4% | HOT HEART/MID-AWAY; COLD OUT-UP-1B |
| 6 | Travis Bazzana | 49.3 | 46.6 | 0.274 | 5.2% | 36.2% | HOT MID-AWAY/HEART; COLD OUT-DN-3B |
| 4 | Jo Adell | 48.3 | 50.7 | 0.209 | 8.9% | 44.9% | CONFIRM HOT LO-AWAY/COLD OUT-UP-3B; COLD OUT-UP-3B |
| 1 | Steven Kwan | 47.7 | 42.3 | 0.306 | 0.4% | 10.5% | CONFIRM COLD OUT-DN-3B/COLD OUT-UP-3B; COLD OUT-DN-3B |
| 9 | Brayan Rocchio | 47.1 | 44.0 | 0.272 | 2.8% | 30.0% | COLD OUT-DN-1B |
| 7 | Patrick Bailey | 47.1 | 48.0 | 0.221 | 7.6% | 42.4% | CONFIRM WARM MID-IN; COLD OUT-UP-1B |
| 8 | Petey Halpin | 46.4 | 44.1 | 0.259 | 5.4% | 25.5% | HOT OUT-DN-3B/OUT-UP-3B; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |
| 2 | José Ramírez | 45.2 | 46.5 | 0.212 | 4.1% | 38.8% | CONFIRM COLD OUT-DN-3B/COLD OUT-UP-1B; COLD OUT-DN-3B |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM HOTs; treat `LOW_SAMPLE_*` as sizing FYI.*

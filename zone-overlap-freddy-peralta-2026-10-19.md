# Zone overlap — vs Freddy Peralta (2026 Statcast)

**Game:** CLE@TB
**Pitcher:** Freddy Peralta (RHP, id 642547) · n=3263 pitches
**Windows:** season + **last 30d** (pitcher recent n=364)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter damage; **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** FF 54% / CH 23% / CU 13% / ST 5% / SL 4% / CS 1%
**Velo:** CH ~87.4, CS ~74.7, CU ~79.5, FF ~94.5, SL ~83.1, ST ~82.4

## Where the pitcher throws

### vs LHB — in-zone 42% · heart 6% · mean px=-0.421 (neg=3B) pz=2.396

- Top zones: OUT-UP-3B 23%, OUT-DN-3B 21%, OUT-DN-1B 8%, MID-IN 7%, HEART 6%, HI-IN (3B) 6%
- **Usage vs this hand:** FF 52%, CH 26%, CU 16%, SL 2%, ST 2%, CS 1%
- **CH lands:** OUT-DN-3B 44%, OUT-UP-3B 15%, OUT-DN-1B 10%
- **CU lands:** OUT-DN-3B 31%, OUT-DN-1B 19%, OUT-UP-3B 10%
- **FF lands:** OUT-UP-3B 33%, OUT-UP-1B 11%, HI-IN (3B) 10%
- **SL lands:** OUT-DN-1B 30%, OUT-DN-3B 22%, LO-IN 10%
- **ST lands:** OUT-DN-3B 33%, OUT-UP-3B 15%, LO-AWAY 9%
- **Zone → pitch mix:** OUT-UP-3B (23% throws → FF 74%+CH 17%); OUT-DN-3B (21% throws → CH 55%+CU 24%); OUT-DN-1B (8% throws → CU 39%+CH 35%); MID-IN (7% throws → FF 54%+CU 22%)

### vs RHB — in-zone 45% · heart 7% · mean px=0.025 (neg=3B) pz=2.241

- Top zones: OUT-DN-1B 22%, OUT-UP-3B 15%, OUT-DN-3B 11%, OUT-UP-1B 7%, HEART 7%, MID-IN 6%
- **Usage vs this hand:** FF 56%, CH 18%, ST 12%, SL 7%, CU 7%, CS 1%
- **CH lands:** OUT-DN-3B 30%, OUT-DN-1B 28%, OUT-UP-3B 8%
- **CU lands:** OUT-DN-1B 25%, OUT-DN-3B 13%, MID-IN 9%
- **FF lands:** OUT-UP-3B 22%, OUT-UP-1B 11%, HI-MID 9%
- **SL lands:** OUT-DN-1B 66%, MID-AWAY 6%, MID-IN 6%
- **ST lands:** OUT-DN-1B 46%, LO-AWAY 11%, HEART 9%
- **Zone → pitch mix:** OUT-DN-1B (22% throws → ST 25%+CH 23%); OUT-UP-3B (15% throws → FF 82%+CH 10%); OUT-DN-3B (11% throws → CH 48%+FF 36%); OUT-UP-1B (7% throws → FF 90%+ST 4%)

## Batter heat vs opposing hand → overlap

### Chase DeLauter (stand L, vs RHP, season n=1691, recent n=189)
- Swing 42.0% · whiff/swing 11.8%
- **Top swing (season):** HI-AWAY (1B) 94.9%; HEART 82.7%; HI-MID 76.1%; MID-AWAY 75.7%
- **Top damage season (xwOBA BIP):** HI-AWAY (1B) 0.481 (EV 86.2, brl 7.7%, BIP 13); LO-AWAY 0.457 (EV 96.4, brl 13.3%, BIP 30); MID-AWAY 0.456 (EV 92.7, brl 10.3%, BIP 29); LO-MID 0.442 (EV 97.3, brl 11.5%, BIP 52)
- **Top damage recent (30d):** HEART 0.404 (BIP 7); HI-MID 0.331 (BIP 5)
- **HOT/WARM overlap:** WARM OUT-UP-3B (W 23.2%, xwOBA 0.37, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM OUT-DN-1B (W 7.9%, xwOBA 0.37, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-IN (3B) (W 6.4%, xwOBA 0.428 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM MID-IN (W 6.6%, xwOBA 0.373, recent — xwOBA nan BIP 2 · SEASON_ONLY); WARM LO-MID (W 5.2%, xwOBA 0.442, recent — xwOBA 0.745 BIP 3 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-3B (W 21.1%, xwOBA 0.217, recent — · SEASON_ONLY)

### Nathaniel Lowe (stand L, vs RHP, season n=1803, recent n=143)
- Swing 45.6% · whiff/swing 19.2%
- **Top swing (season):** HI-MID 77.2%; HEART 73.9%; HI-AWAY (1B) 72.8%; MID-AWAY 64.5%
- **Top damage season (xwOBA BIP):** HEART 0.596 (EV 96.7, brl 19.5%, BIP 41); HI-IN (3B) 0.507 (EV 96.1, brl 11.8%, BIP 17); MID-IN 0.502 (EV 95.4, brl 13.6%, BIP 22); LO-AWAY 0.470 (EV 95.1, brl 13.6%, BIP 22)
- **Top damage recent (30d):** MID-AWAY 0.299 (BIP 7)
- **HOT/WARM overlap:** WARM OUT-DN-3B (W 21.1%, xwOBA 0.373 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 6.4%, xwOBA 0.596, recent — xwOBA 0.29 BIP 3 · SEASON_ONLY); HOT MID-IN (W 6.6%, xwOBA 0.502, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT HI-IN (3B) (W 6.4%, xwOBA 0.507, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM LO-MID (W 5.2%, xwOBA 0.464, recent — xwOBA 0.259 BIP 3 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 23.2%, xwOBA 0.135, recent — · SEASON_ONLY)

### Travis Bazzana (stand L, vs RHP, season n=1553, recent n=150)
- Swing 45.9% · whiff/swing 21.7%
- **Top swing (season):** MID-AWAY 86.3%; HEART 82.5%; LO-AWAY 79.7%; HI-AWAY (1B) 78.8%
- **Top damage season (xwOBA BIP):** MID-AWAY 0.497 (EV 94.1, brl 15.8%, BIP 19); HEART 0.429 (EV 96.2, brl 12.0%, BIP 50); MID-IN 0.348 (EV 86.9, brl 6.9%, BIP 29); HI-MID 0.324 (EV 91.9, brl 13.0%, BIP 23)
- **Top damage recent (30d):** LO-IN 0.293 (BIP 6); HEART 0.211 (BIP 7)
- **HOT/WARM overlap:** HOT HEART (W 6.4%, xwOBA 0.429, recent — xwOBA 0.211 BIP 7 · SEASON_ONLY); HOT HI-IN (3B) (W 6.4%, xwOBA 0.43, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM OUT-UP-1B (W 6.0%, xwOBA 0.53, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 21.1%, xwOBA 0.247, recent — · SEASON_ONLY); OUT-UP-3B (W 23.2%, xwOBA 0.161, recent — · SEASON_ONLY)

### Jo Adell (stand R, vs RHP, season n=2101, recent n=184)
- Swing 52.9% · whiff/swing 25.7%
- **Top swing (season):** HEART 83.2%; LO-MID 75.6%; MID-AWAY 74.2%; MID-IN 73.6%
- **Top damage season (xwOBA BIP):** HI-AWAY (1B) 0.470 (EV 99.3, brl 0.0%, BIP 15); LO-MID 0.462 (EV 97.8, brl 11.8%, BIP 34); OUT-DN-3B 0.445 (EV 88.2, brl 15.4%, BIP 13); MID-AWAY 0.434 (EV 95.0, brl 13.2%, BIP 38)
- **Top damage recent (30d):** HEART 0.204 (BIP 10)
- **HOT/WARM overlap:** WARM MID-AWAY (W 5.6%, xwOBA 0.434, recent HOT xwOBA 0.656 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-3B (W 10.8%, xwOBA 0.445, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-MID (W 6.1%, xwOBA 0.43, recent — xwOBA nan BIP 2 · SEASON_ONLY); WARM LO-MID (W 5.3%, xwOBA 0.462, recent — xwOBA nan BIP 0 · SEASON_ONLY); WARM LO-AWAY (W 5.1%, xwOBA 0.403, recent — xwOBA 0.494 BIP 3 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 15.2%, xwOBA 0.2, recent COLD · CONFIRM)
- **Season ∩ recent CONFIRM:** COLD OUT-UP-3B, WARM MID-AWAY

### Steven Kwan (stand L, vs RHP, season n=2081, recent n=199)
- Swing 36.1% · whiff/swing 5.2%
- **Top swing (season):** HEART 62.7%; LO-IN 58.7%; HI-MID 55.6%; MID-IN 55.1%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.439 (EV 87.5, brl 0.0%, BIP 16); LO-MID 0.348 (EV 89.4, brl 0.0%, BIP 46); LO-IN 0.345 (EV 85.1, brl 0.0%, BIP 32); HI-MID 0.341 (EV 82.7, brl 0.0%, BIP 37)
- **Top damage recent (30d):** HEART 0.487 (BIP 9); HI-MID 0.380 (BIP 5); MID-IN 0.266 (BIP 5)
- **COLD vs his tunnel:** OUT-UP-3B (W 23.2%, xwOBA 0.242, recent COLD · CONFIRM); OUT-DN-3B (W 21.1%, xwOBA 0.275, recent — · SEASON_ONLY); OUT-DN-1B (W 7.9%, xwOBA 0.208, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-UP-3B

### Brayan Rocchio (stand L, vs RHP, season n=1761, recent n=125)
- Swing 47.6% · whiff/swing 19.5%
- **Top swing (season):** HI-AWAY (1B) 76.0%; HEART 73.9%; HI-MID 72.9%; LO-MID 71.3%
- **Top damage season (xwOBA BIP):** HI-IN (3B) 0.410 (EV 90.0, brl 5.0%, BIP 20); LO-MID 0.330 (EV 95.1, brl 4.8%, BIP 42); LO-AWAY 0.330 (EV 89.5, brl 9.1%, BIP 11); OUT-UP-1B 0.316 (EV 71.0, brl 0.0%, BIP 9)
- **Top damage recent (30d):** MID-IN 0.099 (BIP 5)
- **HOT/WARM overlap:** HOT HI-IN (3B) (W 6.4%, xwOBA 0.41, recent — xwOBA nan BIP 2 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 23.2%, xwOBA 0.231, recent — · SEASON_ONLY); OUT-DN-1B (W 7.9%, xwOBA 0.28, recent — · SEASON_ONLY)

### Patrick Bailey (stand L, vs RHP, season n=1284, recent n=132)
- Swing 51.4% · whiff/swing 23.6%
- **Top swing (season):** HI-MID 84.9%; MID-IN 73.8%; HEART 72.5%; HI-AWAY (1B) 71.9%
- **Top damage season (xwOBA BIP):** HI-MID 0.645 (EV 93.7, brl 21.7%, BIP 23); HEART 0.526 (EV 94.8, brl 19.4%, BIP 36); HI-IN (3B) 0.498 (EV 95.6, brl 0.0%, BIP 11); MID-AWAY 0.442 (EV 91.4, brl 6.2%, BIP 16)
- **Top damage recent (30d):** HI-MID 0.743 (BIP 5); OUT-DN-3B 0.427 (BIP 5)
- **HOT/WARM overlap:** WARM MID-IN (W 6.6%, xwOBA 0.378, recent WARM xwOBA 0.769 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM LO-IN (W 5.2%, xwOBA 0.352, recent WARM xwOBA 0.516 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM OUT-UP-3B (W 23.2%, xwOBA 0.373, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 6.4%, xwOBA 0.526, recent — xwOBA nan BIP 1 · SEASON_ONLY); HOT HI-IN (3B) (W 6.4%, xwOBA 0.498 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **Season ∩ recent CONFIRM:** WARM MID-IN, WARM LO-IN

### Petey Halpin (stand L, vs RHP, season n=669, recent n=98)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 58.1% · whiff/swing 22.4%
- **Top swing (season):** HI-MID 90.6%; MID-IN 86.8%; HEART 85.2%; LO-AWAY 82.5%
- **Top damage season (xwOBA BIP):** OUT-DN-3B 0.502 (EV 83.9, brl 6.2%, BIP 16); MID-AWAY 0.497 (EV 85.9, brl 7.7%, BIP 13); MID-IN 0.470 (EV 90.5, brl 22.2%, BIP 9); LO-IN 0.404 (EV 87.7, brl 7.1%, BIP 14)
- **HOT/WARM overlap:** HOT OUT-UP-3B (W 23.2%, xwOBA 0.533, recent — xwOBA None BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-DN-3B (W 21.1%, xwOBA 0.502, recent — xwOBA None BIP 2 · SEASON_ONLY); HOT MID-IN (W 6.6%, xwOBA 0.47 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM LO-IN (W 5.2%, xwOBA 0.404 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-1B (W 7.9%, xwOBA 0.211 · SEASON_ONLY)

### José Ramírez (stand L, vs RHP, season n=1868, recent n=182)
- Swing 44.9% · whiff/swing 14.9%
- **Top swing (season):** HEART 74.2%; HI-MID 73.1%; LO-MID 66.7%; LO-IN 65.9%
- **Top damage season (xwOBA BIP):** OUT-UP-3B 0.484 (EV 91.8, brl 16.7%, BIP 18); LO-AWAY 0.400 (EV 83.6, brl 7.7%, BIP 13); MID-IN 0.388 (EV 94.5, brl 2.6%, BIP 38); HEART 0.363 (EV 90.3, brl 8.9%, BIP 45)
- **Top damage recent (30d):** HEART 0.410 (BIP 6); MID-IN 0.262 (BIP 5); OUT-DN-3B 0.113 (BIP 5); LO-IN 0.090 (BIP 6)
- **HOT/WARM overlap:** WARM HEART (W 6.4%, xwOBA 0.363, recent WARM xwOBA 0.41 BIP 6 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-UP-3B (W 23.2%, xwOBA 0.484, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM OUT-DN-1B (W 7.9%, xwOBA 0.352, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM MID-IN (W 6.6%, xwOBA 0.388, recent — xwOBA 0.262 BIP 5 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-3B (W 21.1%, xwOBA 0.232, recent COLD · CONFIRM)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-3B, WARM HEART

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | HR/RBI | AVG vs hand | Barrel | HH | Zone note |
|------|--------|------|--------|-------------|--------|----|-----------|
| 3 | Chase DeLauter | 54.5 | 54.2 | 0.269 | 6.3% | 46.3% | HOT HI-IN (3B); COLD OUT-DN-3B |
| 5 | Nathaniel Lowe | 54.1 | 53.3 | 0.271 | 8.3% | 41.4% | HOT HEART/MID-IN; COLD OUT-UP-3B |
| 6 | Travis Bazzana | 49.3 | 46.6 | 0.274 | 5.2% | 36.2% | HOT HEART/HI-IN (3B); COLD OUT-DN-3B |
| 4 | Jo Adell | 48.3 | 50.7 | 0.209 | 8.9% | 44.9% | CONFIRM COLD OUT-UP-3B/WARM MID-AWAY; COLD OUT-UP-3B |
| 1 | Steven Kwan | 47.7 | 42.3 | 0.306 | 0.4% | 10.5% | CONFIRM COLD OUT-UP-3B; COLD OUT-UP-3B |
| 9 | Brayan Rocchio | 47.1 | 44.0 | 0.272 | 2.8% | 30.0% | HOT HI-IN (3B); COLD OUT-UP-3B |
| 7 | Patrick Bailey | 47.1 | 48.0 | 0.221 | 7.6% | 42.4% | CONFIRM WARM MID-IN/WARM LO-IN |
| 8 | Petey Halpin | 46.4 | 44.1 | 0.259 | 5.4% | 25.5% | HOT OUT-UP-3B/OUT-DN-3B; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |
| 2 | José Ramírez | 45.2 | 46.5 | 0.212 | 4.1% | 38.8% | CONFIRM COLD OUT-DN-3B/WARM HEART; COLD OUT-DN-3B |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM HOTs; treat `LOW_SAMPLE_*` as sizing FYI.*

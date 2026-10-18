# Zone overlap — vs Parker Messick (2026 Statcast)

**Game:** TB@CLE
**Pitcher:** Parker Messick (LHP, id 800048) · n=3496 pitches
**Windows:** season + **last 30d** (pitcher recent n=394)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter damage; **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** FF 42% / CH 24% / SI 15% / CU 8% / SL 7% / FC 5%
**Velo:** CH ~85.8, CU ~79.1, FC ~90.4, FF ~94.3, SI ~92.9, SL ~86.8

## Where the pitcher throws

### vs LHB — in-zone 51% · heart 8% · mean px=-0.18 (neg=3B) pz=2.296

- Top zones: OUT-DN-3B 22%, OUT-UP-1B 11%, OUT-UP-3B 9%, HEART 8%, MID-IN 7%, MID-AWAY 7%
- **Usage vs this hand:** FF 37%, SI 31%, SL 16%, CH 8%, CU 6%, FC 2%
- **CH lands:** OUT-DN-1B 35%, OUT-DN-3B 26%, MID-AWAY 9%
- **CU lands:** OUT-DN-3B 56%, HEART 9%, OUT-DN-1B 9%
- **FF lands:** OUT-UP-3B 21%, OUT-UP-1B 15%, OUT-DN-3B 10%
- **SI lands:** OUT-UP-1B 15%, OUT-DN-3B 14%, MID-AWAY 13%
- **SL lands:** OUT-DN-3B 45%, LO-IN 14%, HEART 12%
- **Zone → pitch mix:** OUT-DN-3B (22% throws → SL 33%+SI 19%); OUT-UP-1B (11% throws → FF 49%+SI 42%); OUT-UP-3B (9% throws → FF 84%+SI 8%); HEART (9% throws → FF 40%+SI 28%)

### vs RHB — in-zone 46% · heart 6% · mean px=0.16 (neg=3B) pz=2.295

- Top zones: OUT-DN-1B 17%, OUT-UP-1B 16%, OUT-DN-3B 13%, OUT-UP-3B 8%, MID-AWAY 7%, HEART 6%
- **Usage vs this hand:** FF 43%, CH 29%, CU 9%, SI 9%, FC 6%, SL 3%
- **CH lands:** OUT-DN-1B 45%, OUT-DN-3B 19%, OUT-UP-1B 8%
- **CU lands:** OUT-DN-3B 33%, LO-MID 11%, OUT-UP-1B 11%
- **FC lands:** OUT-UP-3B 34%, OUT-UP-1B 13%, OUT-DN-3B 10%
- **FF lands:** OUT-UP-1B 23%, OUT-UP-3B 14%, HI-MID 11%
- **SI lands:** OUT-DN-1B 19%, OUT-UP-1B 14%, LO-AWAY 11%
- **SL lands:** OUT-DN-3B 28%, OUT-UP-1B 15%, OUT-DN-1B 11%
- **Zone → pitch mix:** OUT-DN-1B (17% throws → CH 78%+SI 11%); OUT-UP-1B (16% throws → FF 63%+CH 15%); OUT-DN-3B (13% throws → CH 43%+CU 24%); OUT-UP-3B (8% throws → FF 74%+FC 23%)

## Batter heat vs opposing hand → overlap

### Junior Caminero (stand R, vs LHP, season n=815, recent n=107)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 41.6% · whiff/swing 18.9%
- **Top swing (season):** HEART 70.0%; HI-MID 68.9%; MID-AWAY 68.4%; LO-MID 65.7%
- **Top damage season (xwOBA BIP):** HI-MID 0.818 (EV 103.0, brl 33.3%, BIP 12); OUT-UP-1B 0.734 (EV 99.8, brl 33.3%, BIP 9); MID-AWAY 0.425 (EV 96.2, brl 21.4%, BIP 14); OUT-UP-3B 0.401 (EV 86.9, brl 12.5%, BIP 8)
- **HOT/WARM overlap:** HOT OUT-UP-1B (W 15.7%, xwOBA 0.734, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-DN-3B (W 13.0%, xwOBA 0.555, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM OUT-DN-1B (W 16.7%, xwOBA 0.382, recent — xwOBA 0.332 BIP 3 · SEASON_ONLY); HOT HI-MID (W 6.1%, xwOBA 0.818 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-UP-3B (W 8.2%, xwOBA 0.401 · SEASON_ONLY) [LOW_SAMPLE_ZONE]

### Yandy Díaz (stand R, vs LHP, season n=806, recent n=103)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 48.3% · whiff/swing 11.6%
- **Top swing (season):** HI-MID 79.5%; MID-AWAY 77.8%; HI-AWAY (1B) 73.0%; MID-IN 69.8%
- **Top damage season (xwOBA BIP):** OUT-DN-3B 0.568 (EV 98.4, brl 15.4%, BIP 13); HEART 0.461 (EV 98.6, brl 16.0%, BIP 25); HI-AWAY (1B) 0.393 (EV 100.1, brl 12.5%, BIP 8); MID-AWAY 0.372 (EV 95.9, brl 0.0%, BIP 14)
- **HOT/WARM overlap:** HOT OUT-DN-3B (W 13.0%, xwOBA 0.568, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 6.2%, xwOBA 0.461, recent — xwOBA 0.614 BIP 3 · SEASON_ONLY); WARM MID-AWAY (W 6.9%, xwOBA 0.372 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-AWAY (1B) (W 5.4%, xwOBA 0.393 · SEASON_ONLY) [LOW_SAMPLE_ZONE]

### Jonathan Aranda (stand L, vs LHP, season n=844, recent n=97)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 43.7% · whiff/swing 19.0%
- **Top swing (season):** LO-MID 77.5%; MID-AWAY 74.2%; HEART 72.7%; LO-AWAY 72.4%
- **Top damage season (xwOBA BIP):** HI-MID 0.650 (EV 97.3, brl 25.0%, BIP 8); LO-AWAY 0.455 (EV 94.7, brl 0.0%, BIP 11); MID-IN 0.429 (EV 91.7, brl 15.4%, BIP 13); LO-MID 0.417 (EV 95.6, brl 11.8%, BIP 17)
- **HOT/WARM overlap:** HOT MID-IN (W 6.9%, xwOBA 0.429, recent HOT xwOBA 0.971 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM OUT-DN-3B (W 22.0%, xwOBA 0.353, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM OUT-UP-1B (W 11.2%, xwOBA 0.357, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-MID (W 6.0%, xwOBA 0.65 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HEART (W 8.5%, xwOBA 0.375 · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT MID-IN

### Ryan Vilade (stand R, vs LHP, season n=748, recent n=78)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 49.6% · whiff/swing 19.9%
- **Top swing (season):** HI-MID 90.0%; HI-IN (3B) 84.6%; LO-AWAY 83.9%; HEART 80.3%
- **Top damage season (xwOBA BIP):** HI-MID 0.661 (EV 92.1, brl 12.5%, BIP 8); LO-MID 0.615 (EV 94.4, brl 15.4%, BIP 13); MID-IN 0.524 (EV 89.4, brl 10.0%, BIP 20); OUT-DN-3B 0.497 (EV 85.2, brl 11.1%, BIP 9)
- **HOT/WARM overlap:** HOT OUT-DN-1B (W 16.7%, xwOBA 0.416, recent — xwOBA None BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-DN-3B (W 13.0%, xwOBA 0.497, recent — xwOBA None BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-MID (W 6.1%, xwOBA 0.661 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM LO-MID (W 5.1%, xwOBA 0.615, recent — xwOBA None BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM LO-AWAY (W 5.0%, xwOBA 0.441 · SEASON_ONLY) [LOW_SAMPLE_ZONE]

### Jonny DeLuca (stand R, vs LHP, season n=651, recent n=102)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 55.0% · whiff/swing 22.3%
- **Top swing (season):** HI-MID 81.0%; LO-AWAY 79.3%; HEART 78.3%; LO-MID 77.8%
- **Top damage season (xwOBA BIP):** LO-MID 0.486 (EV 97.4, brl 8.3%, BIP 12); HI-MID 0.453 (EV 82.3, brl 6.2%, BIP 16); HEART 0.368 (EV 94.8, brl 0.0%, BIP 11); OUT-DN-3B 0.364 (EV 85.3, brl 0.0%, BIP 8)
- **HOT/WARM overlap:** WARM OUT-DN-3B (W 13.0%, xwOBA 0.364, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-MID (W 6.1%, xwOBA 0.453 · SEASON_ONLY); WARM LO-MID (W 5.1%, xwOBA 0.486 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HEART (W 6.2%, xwOBA 0.368, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-1B (W 16.7%, xwOBA 0.267, recent WARM · CONFLICT); OUT-UP-1B (W 15.7%, xwOBA 0.125, recent — · SEASON_ONLY)
- **Season vs recent CONFLICT:** OUT-DN-1B (COLD→WARM)

### Chandler Simpson (stand L, vs LHP, season n=692, recent n=80)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 51.2% · whiff/swing 10.2%
- **Top swing (season):** HI-MID 81.2%; MID-AWAY 79.2%; LO-AWAY 78.1%; HI-IN (3B) 69.2%
- **Top damage season (xwOBA BIP):** HI-IN (3B) 0.297 (EV 77.9, brl 0.0%, BIP 12); HEART 0.296 (EV 83.6, brl 0.0%, BIP 26); OUT-DN-1B 0.283 (EV 71.4, brl 0.0%, BIP 9); MID-AWAY 0.271 (EV 89.4, brl 0.0%, BIP 25)
- **COLD vs his tunnel:** OUT-UP-1B (W 11.2%, xwOBA 0.243, recent COLD · CONFIRM); OUT-UP-3B (W 9.3%, xwOBA 0.088 · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-UP-1B

### Ben Williamson (stand R, vs LHP, season n=636, recent n=80)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 45.1% · whiff/swing 16.7%
- **Top swing (season):** HI-IN (3B) 73.3%; HI-MID 73.3%; LO-AWAY 67.7%; MID-IN 63.2%
- **Top damage season (xwOBA BIP):** HI-IN (3B) 0.456 (EV 90.7, brl 11.1%, BIP 9); MID-IN 0.368 (EV 91.8, brl 15.4%, BIP 13); HI-MID 0.366 (EV 88.4, brl 0.0%, BIP 9); HEART 0.329 (EV 93.1, brl 0.0%, BIP 20)
- **HOT/WARM overlap:** WARM OUT-DN-3B (W 13.0%, xwOBA 0.369, recent — xwOBA None BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-MID (W 6.1%, xwOBA 0.366 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-UP-3B (W 8.2%, xwOBA 0.193 · SEASON_ONLY)

### Liam Hicks (stand L, vs LHP, season n=491, recent n=61)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 42.2% · whiff/swing 12.6%
- **Top swing (season):** LO-MID 64.9%; HI-MID 56.0%; HEART 51.6%; OUT-DN-1B 50.0%
- **Top damage season (xwOBA BIP):** LO-MID 0.347 (EV 88.8, brl 5.3%, BIP 19); OUT-DN-3B 0.326 (EV 77.3, brl 0.0%, BIP 11); MID-IN 0.320 (EV 87.8, brl 0.0%, BIP 8); HI-MID 0.260 (EV 81.8, brl 0.0%, BIP 8)
- **COLD vs his tunnel:** OUT-UP-3B (W 9.3%, xwOBA 0.264 · SEASON_ONLY); HEART (W 8.5%, xwOBA 0.22 · SEASON_ONLY); OUT-UP-1B (W 11.2%, xwOBA 0.104 · SEASON_ONLY)

### Taylor Walls (stand R, vs LHP, season n=615, recent n=62)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 46.5% · whiff/swing 18.2%
- **Top swing (season):** HI-MID 76.9%; HEART 72.9%; MID-AWAY 71.0%; MID-IN 64.6%
- **Top damage season (xwOBA BIP):** OUT-UP-1B 0.272 (EV 74.3, brl 0.0%, BIP 11); HI-IN (3B) 0.245 (EV 76.5, brl 0.0%, BIP 8); HI-MID 0.235 (EV 84.0, brl 0.0%, BIP 14); LO-MID 0.225 (EV 83.2, brl 0.0%, BIP 14)
- **COLD vs his tunnel:** OUT-UP-1B (W 15.7%, xwOBA 0.272 · SEASON_ONLY); OUT-DN-1B (W 16.7%, xwOBA 0.121, recent — · SEASON_ONLY)

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | HR/RBI | AVG vs hand | Barrel | HH | Zone note |
|------|--------|------|--------|-------------|--------|----|-----------|
| 4 | Junior Caminero | 60.9 | 61.0 | 0.287 | 13.1% | 49.7% | HOT OUT-UP-1B/OUT-DN-3B; LOW_SAMPLE_RECENT |
| 1 | Yandy Díaz | 54.9 | 55.0 | 0.264 | 7.1% | 48.1% | HOT OUT-DN-3B/HEART; LOW_SAMPLE_RECENT |
| 2 | Jonathan Aranda | 53.6 | 54.4 | 0.250 | 9.9% | 46.0% | CONFIRM HOT MID-IN; LOW_SAMPLE_RECENT |
| 3 | Ryan Vilade | 52.5 | 51.2 | 0.272 | 7.1% | 39.9% | HOT OUT-DN-1B/OUT-DN-3B; LOW_SAMPLE_RECENT |
| 6 | Jonny DeLuca | 45.0 | 41.7 | 0.264 | 3.6% | 30.2% | HOT HI-MID; COLD OUT-DN-1B; CONFLICT OUT-DN-1B; LOW_SAMPLE_RECENT |
| 5 | Chandler Simpson | 42.9 | 37.5 | 0.285 | 0.0% | 13.6% | CONFIRM COLD OUT-UP-1B; COLD OUT-UP-1B; LOW_SAMPLE_RECENT |
| 8 | Ben Williamson | 42.1 | 41.4 | 0.224 | 1.9% | 33.2% | WARM OUT-DN-3B/HI-MID; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 7 | Liam Hicks | 40.4 | 41.8 | 0.192 | 3.7% | 27.1% | COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 9 | Taylor Walls | 35.1 | 33.6 | 0.203 | 2.1% | 21.9% | COLD OUT-UP-1B; LOW_SAMPLE_RECENT |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM HOTs; treat `LOW_SAMPLE_*` as sizing FYI.*

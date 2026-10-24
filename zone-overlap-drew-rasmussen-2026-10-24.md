# Zone overlap — vs Drew Rasmussen (2026 Statcast)

**Game:** TB@MIL
**Pitcher:** Drew Rasmussen (RHP, id 656876) · n=3160 pitches
**Windows:** season + **last 30d** (pitcher recent n=287)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter **damage**; **dump fit** adds where they **swing** on his LHB/RHB tunnel. **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** FC 29% / FF 28% / SI 23% / CH 14% / CU 3% / ST 2%
**Velo:** CH ~89.5, CU ~80.1, FC ~89.9, FF ~95.8, SI ~95.2, ST ~84.5

## Where the pitcher throws

### vs LHB — in-zone 51% · heart 9% · mean px=0.097 (neg=3B) pz=2.389

- Top zones: OUT-DN-1B 18%, OUT-UP-3B 13%, OUT-DN-3B 9%, OUT-UP-1B 9%, HEART 9%, MID-AWAY 7%
- **Usage vs this hand:** FF 32%, FC 28%, CH 18%, SI 16%, CU 5%, ST 0%
- **CH lands:** OUT-DN-3B 37%, OUT-DN-1B 16%, OUT-UP-3B 12%
- **CU lands:** OUT-UP-3B 22%, OUT-DN-1B 18%, OUT-DN-3B 15%
- **FC lands:** OUT-DN-1B 37%, LO-AWAY 11%, MID-AWAY 11%
- **FF lands:** OUT-UP-3B 25%, OUT-UP-1B 16%, HI-MID 10%
- **SI lands:** OUT-DN-1B 15%, OUT-UP-1B 15%, MID-AWAY 10%
- **Zone → pitch mix:** OUT-DN-1B (18% throws → FC 58%+CH 17%); OUT-UP-3B (13% throws → FF 59%+CH 17%); OUT-DN-3B (9% throws → CH 73%+FC 10%); OUT-UP-1B (9% throws → FF 56%+SI 26%)
- **Dump (ticket tunnel):** OUT-DN-1B 17.5% FC+CH · chase; OUT-UP-3B 13.5% FF+CH · chase

### vs RHB — in-zone 50% · heart 8% · mean px=0.205 (neg=3B) pz=2.2

- Top zones: OUT-DN-1B 24%, OUT-UP-1B 9%, OUT-UP-3B 9%, OUT-DN-3B 8%, HEART 8%, LO-AWAY 7%
- **Usage vs this hand:** SI 34%, FC 31%, FF 22%, CH 6%, ST 6%, CU 0%
- **CH lands:** OUT-DN-1B 47%, OUT-DN-3B 29%, LO-MID 10%
- **FC lands:** OUT-DN-1B 43%, LO-AWAY 11%, MID-AWAY 8%
- **FF lands:** OUT-UP-1B 27%, OUT-UP-3B 12%, OUT-DN-1B 10%
- **SI lands:** OUT-UP-3B 16%, OUT-DN-3B 15%, HEART 11%
- **ST lands:** OUT-DN-1B 36%, OUT-DN-3B 10%, HEART 8%
- **Zone → pitch mix:** OUT-DN-1B (24% throws → FC 57%+CH 13%); OUT-UP-1B (9% throws → FF 67%+FC 23%); OUT-UP-3B (9% throws → SI 61%+FF 31%); OUT-DN-3B (8% throws → SI 60%+CH 22%)
- **Dump (ticket tunnel):** OUT-DN-1B 23.8% FC+CH · chase

## Dump × swing (vs LHB / RHB)

Pitcher’s #1 throw pocket vs that batter’s hand, crossed with whether they **swing** there. TUNNEL = Hits location. MISTAKE = hunt middle, not the dump. CHASE/TAKE = not a Hits lean on the tunnel (K / take).

| Batter | Stand | Dump | Throw | Swing | Whiff | xwOBA | Fit |
|--------|-------|------|-------|-------|-------|-------|-----|
| Jake Bauers | L | OUT-DN-1B | 17.5% FC+CH | 22.0 | 77.4 | 0.29 | **MISTAKE** |
| Garrett Mitchell | L | OUT-DN-1B | 17.5% FC+CH | 25.3 | 69.9 | 0.421 | **TUNNEL** |
| Jackson Chourio | R | OUT-DN-1B | 23.8% FC+CH | 26.5 | 68.7 | 0.255 | **MISTAKE** |
| Brice Turang | L | OUT-DN-1B | 17.5% FC+CH | 21.9 | 43.8 | 0.517 | **TUNNEL** |
| William Contreras | R | OUT-DN-1B | 23.8% FC+CH | 22.7 | 60.0 | 0.277 | **MISTAKE** |
| Cooper Pratt | R | OUT-DN-1B | 23.8% FC+CH | 26.6 | 48.4 | 0.398 | **TUNNEL** |
| Christian Yelich | L | OUT-DN-1B | 17.5% FC+CH | 32.2 | 63.0 | 0.236 | **MISTAKE** |
| David Hamilton | L | OUT-DN-1B | 17.5% FC+CH | 30.6 | 39.8 | 0.24 | **MISTAKE** |
| Sal Frelick | L | OUT-DN-1B | 17.5% FC+CH | 23.4 | 22.4 | 0.223 | **TAKE** |

## Batter heat vs opposing hand → overlap

### Jake Bauers (stand L, vs RHP, season n=1971, recent n=156)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone HEART/MID-AWAY (swing 22.0% · whiff 77.4% · xwOBA 0.29)
- Swing 39.2% · whiff/swing 28.5%
- **Top swing (season):** HEART 77.6%; HI-MID 73.6%; MID-AWAY 62.5%; HI-AWAY (1B) 61.1%
- **Top damage season (xwOBA BIP):** OUT-UP-1B 0.764 (EV 84.9, brl 20.0%, BIP 10); HI-MID 0.644 (EV 101.6, brl 24.0%, BIP 25); HI-AWAY (1B) 0.566 (EV 83.5, brl 36.4%, BIP 11); MID-IN 0.506 (EV 98.1, brl 16.7%, BIP 30)
- **HOT/WARM overlap:** HOT HEART (W 8.8%, xwOBA 0.447, recent HOT xwOBA 0.426 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT MID-AWAY (W 7.2%, xwOBA 0.437, recent HOT xwOBA 0.475 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-UP-1B (W 9.1%, xwOBA 0.764, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-MID (W 6.4%, xwOBA 0.644 · SEASON_ONLY); WARM HI-AWAY (1B) (W 5.6%, xwOBA 0.566 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 9.3%, xwOBA 0.247, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT HEART, HOT MID-AWAY

### Garrett Mitchell (stand L, vs RHP, season n=1828, recent n=125)
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-1B (W 17.5% FC+CH) (swing 25.3% · whiff 69.9% · xwOBA 0.421)
- Swing 45.6% · whiff/swing 33.9%
- **Top swing (season):** HEART 80.3%; HI-MID 79.0%; MID-IN 69.7%; HI-AWAY (1B) 67.6%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.652 (EV 97.8, brl 11.8%, BIP 17); HI-MID 0.625 (EV 100.2, brl 26.7%, BIP 15); HEART 0.586 (EV 99.8, brl 19.1%, BIP 47); MID-IN 0.554 (EV 97.2, brl 11.1%, BIP 27)
- **HOT/WARM overlap:** HOT OUT-DN-1B (W 17.5%, xwOBA 0.421, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-UP-1B (W 9.1%, xwOBA 0.611, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 8.8%, xwOBA 0.586, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT HI-MID (W 6.4%, xwOBA 0.625 · SEASON_ONLY); HOT LO-AWAY (W 6.2%, xwOBA 0.652 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-3B (W 9.3%, xwOBA 0.206, recent — · SEASON_ONLY)

### Jackson Chourio (stand R, vs RHP, season n=1740, recent n=126)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone MID-AWAY/HEART (swing 26.5% · whiff 68.7% · xwOBA 0.255)
- Swing 49.0% · whiff/swing 24.1%
- **Top swing (season):** MID-IN 77.1%; HI-IN (3B) 74.6%; HEART 72.6%; HI-MID 69.1%
- **Top damage season (xwOBA BIP):** HEART 0.651 (EV 98.6, brl 26.2%, BIP 42); MID-IN 0.548 (EV 96.1, brl 24.3%, BIP 37); HI-MID 0.501 (EV 98.2, brl 22.7%, BIP 22); LO-IN 0.441 (EV 96.5, brl 10.0%, BIP 20)
- **Top damage recent (30d):** LO-AWAY 0.301 (BIP 5)
- **HOT/WARM overlap:** HOT MID-AWAY (W 6.2%, xwOBA 0.407, recent HOT xwOBA 0.678 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HEART (W 8.3%, xwOBA 0.651 · SEASON_ONLY); WARM OUT-UP-3B (W 9.0%, xwOBA 0.358, recent — xwOBA 0.197 BIP 3 · SEASON_ONLY); WARM HI-MID (W 5.0%, xwOBA 0.501 · SEASON_ONLY); WARM LO-MID (W 6.6%, xwOBA 0.368 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 23.8%, xwOBA 0.255, recent — · SEASON_ONLY); OUT-UP-1B (W 9.2%, xwOBA 0.22, recent — · SEASON_ONLY); OUT-DN-3B (W 8.4%, xwOBA 0.194 · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT MID-AWAY

### Brice Turang (stand L, vs RHP, season n=2205, recent n=138)
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-1B (W 17.5% FC+CH) (swing 21.9% · whiff 43.8% · xwOBA 0.517)
- Swing 44.2% · whiff/swing 19.0%
- **Top swing (season):** HI-MID 74.3%; MID-AWAY 71.6%; HI-AWAY (1B) 71.4%; HEART 68.8%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.554 (EV 97.0, brl 17.2%, BIP 29); HEART 0.553 (EV 95.8, brl 17.1%, BIP 41); OUT-DN-1B 0.517 (EV 92.9, brl 7.7%, BIP 13); LO-MID 0.504 (EV 89.6, brl 9.3%, BIP 54)
- **HOT/WARM overlap:** HOT OUT-DN-1B (W 17.5%, xwOBA 0.517, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 8.8%, xwOBA 0.553, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT LO-AWAY (W 6.2%, xwOBA 0.554 · SEASON_ONLY); WARM OUT-UP-1B (W 9.1%, xwOBA 0.351, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT MID-AWAY (W 7.2%, xwOBA 0.422, recent — xwOBA 0.123 BIP 4 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 13.5%, xwOBA 0.262, recent — · SEASON_ONLY)

### William Contreras (stand R, vs RHP, season n=1773, recent n=128)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone HI-MID/HEART (swing 22.7% · whiff 60.0% · xwOBA 0.277)
- Swing 47.9% · whiff/swing 17.5%
- **Top swing (season):** HI-MID 80.8%; HEART 76.5%; MID-IN 74.3%; HI-IN (3B) 73.9%
- **Top damage season (xwOBA BIP):** OUT-DN-3B 0.516 (EV 90.6, brl 6.7%, BIP 15); HI-IN (3B) 0.453 (EV 91.6, brl 20.6%, BIP 34); OUT-UP-1B 0.430 (EV 83.5, brl 16.7%, BIP 12); LO-AWAY 0.428 (EV 90.2, brl 3.7%, BIP 27)
- **HOT/WARM overlap:** WARM HI-MID (W 5.0%, xwOBA 0.41, recent WARM xwOBA 0.571 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-3B (W 8.4%, xwOBA 0.516 · SEASON_ONLY); HOT OUT-UP-1B (W 9.2%, xwOBA 0.43, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HEART (W 8.3%, xwOBA 0.387, recent COLD xwOBA 0.02 BIP 3 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT LO-AWAY (W 7.3%, xwOBA 0.428, recent — xwOBA nan BIP 1 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 23.8%, xwOBA 0.277, recent HOT · CONFLICT); OUT-UP-3B (W 9.0%, xwOBA 0.211, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** WARM HI-MID
- **Season vs recent CONFLICT:** OUT-DN-1B (COLD→HOT), HEART (WARM→COLD)

### Cooper Pratt (stand R, vs RHP, season n=982, recent n=127)
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-1B (W 23.8% FC+CH) (swing 26.6% · whiff 48.4% · xwOBA 0.398)
- Swing 45.2% · whiff/swing 16.9%
- **Top swing (season):** HEART 77.6%; HI-MID 68.8%; MID-IN 64.6%; LO-MID 62.7%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.398 (EV 82.0, brl 0.0%, BIP 17); MID-AWAY 0.368 (EV 91.8, brl 4.5%, BIP 22); HI-IN (3B) 0.358 (EV 80.3, brl 6.7%, BIP 15); HEART 0.355 (EV 94.9, brl 3.8%, BIP 26)
- **Top damage recent (30d):** LO-MID 0.249 (BIP 5); HEART 0.157 (BIP 5)
- **HOT/WARM overlap:** WARM OUT-DN-1B (W 23.8%, xwOBA 0.398, recent — xwOBA nan BIP 2 · SEASON_ONLY); WARM HEART (W 8.3%, xwOBA 0.355, recent COLD xwOBA 0.157 BIP 5 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM MID-AWAY (W 6.2%, xwOBA 0.368, recent — xwOBA 0.285 BIP 3 · SEASON_ONLY); HOT OUT-UP-3B (W 9.0%, xwOBA 0.574, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 8.4%, xwOBA 0.104 · SEASON_ONLY)
- **Season vs recent CONFLICT:** HEART (WARM→COLD)

### Christian Yelich (stand L, vs RHP, season n=1749, recent n=117)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone LO-AWAY/HEART (swing 32.2% · whiff 63.0% · xwOBA 0.236)
- Swing 45.3% · whiff/swing 29.9%
- **Top swing (season):** HEART 75.8%; LO-MID 70.9%; LO-AWAY 70.9%; HI-AWAY (1B) 70.5%
- **Top damage season (xwOBA BIP):** HEART 0.635 (EV 95.4, brl 20.0%, BIP 30); MID-IN 0.560 (EV 98.6, brl 19.0%, BIP 21); HI-MID 0.500 (EV 82.0, brl 30.8%, BIP 13); LO-MID 0.482 (EV 96.5, brl 18.2%, BIP 33)
- **Top damage recent (30d):** LO-MID 0.653 (BIP 5)
- **HOT/WARM overlap:** WARM LO-AWAY (W 6.2%, xwOBA 0.369, recent WARM xwOBA 0.633 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HEART (W 8.8%, xwOBA 0.635, recent — xwOBA nan BIP 1 · SEASON_ONLY); HOT HI-MID (W 6.4%, xwOBA 0.5 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-IN (3B) (W 5.0%, xwOBA 0.394 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-1B (W 17.5%, xwOBA 0.236, recent — · SEASON_ONLY); OUT-DN-3B (W 9.3%, xwOBA 0.226, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** WARM LO-AWAY

### David Hamilton (stand L, vs RHP, season n=1448, recent n=60)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone HEART/LO-AWAY (swing 30.6% · whiff 39.8% · xwOBA 0.24)
- Swing 45.6% · whiff/swing 17.3%
- **Top swing (season):** MID-AWAY 76.3%; HI-MID 76.0%; HEART 70.1%; HI-AWAY (1B) 67.9%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.475 (EV 96.4, brl 11.8%, BIP 17); HEART 0.432 (EV 85.7, brl 18.4%, BIP 38); LO-IN 0.363 (EV 73.9, brl 0.0%, BIP 10); MID-AWAY 0.342 (EV 85.6, brl 8.1%, BIP 37)
- **HOT/WARM overlap:** HOT HEART (W 8.8%, xwOBA 0.432 · SEASON_ONLY); HOT LO-AWAY (W 6.2%, xwOBA 0.475 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 13.5%, xwOBA 0.231, recent COLD · CONFIRM); OUT-DN-1B (W 17.5%, xwOBA 0.24, recent — · SEASON_ONLY); OUT-DN-3B (W 9.3%, xwOBA 0.194 · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-UP-3B

### Sal Frelick (stand L, vs RHP, season n=1329, recent n=112)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TAKE`** — takes dump OUT-DN-1B (swing 23.4%) — not a Hits lean on that pitch (swing 23.4% · whiff 22.4% · xwOBA 0.223)
- Swing 43.0% · whiff/swing 7.5%
- **Top swing (season):** MID-AWAY 66.7%; LO-MID 66.7%; HI-MID 64.0%; HI-AWAY (1B) 62.3%
- **Top damage season (xwOBA BIP):** LO-IN 0.324 (EV 82.3, brl 0.0%, BIP 17); OUT-UP-3B 0.317 (EV 87.7, brl 9.1%, BIP 11); HI-IN (3B) 0.314 (EV 89.1, brl 0.0%, BIP 16); HEART 0.312 (EV 90.9, brl 2.7%, BIP 37)
- **COLD vs his tunnel:** OUT-DN-1B (W 17.5%, xwOBA 0.223, recent COLD · CONFIRM); OUT-DN-3B (W 9.3%, xwOBA 0.2, recent — · SEASON_ONLY); OUT-UP-1B (W 9.1%, xwOBA 0.189, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-1B

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | Exp H | P(1+) | PA | RBI | HR/RBI | Zone note |
|------|--------|------|-------|-------|----|-----|--------|-----------|
| 2 | Jake Bauers | 59.4 | 0.46 | 40% | 3 | good | 60.7 | MISTAKE OUT-DN-1B; CONFIRM HOT HEART/HOT MID-AWAY; COLD OUT-DN-3B |
| 6 | Garrett Mitchell | 58.7 | 0.31 | 28% | 2 | good | 59.3 | TUNNEL OUT-DN-1B; HOT OUT-DN-1B/OUT-UP-1B; COLD OUT-DN-3B |
| 1 | Jackson Chourio | 57.7 | 0.50 | 42% | 3 | thin | 57.8 | MISTAKE OUT-DN-1B; CONFIRM HOT MID-AWAY; COLD OUT-DN-1B |
| 5 | Brice Turang | 55.8 | 0.40 | 36% | 2 | good | 54.0 | TUNNEL OUT-DN-1B; HOT OUT-DN-1B/HEART; COLD OUT-UP-3B |
| 4 | William Contreras | 54.4 | 0.61 | 49% | 3 | prime | 53.8 | MISTAKE OUT-DN-1B; CONFIRM WARM HI-MID; COLD OUT-DN-1B; CONFLICT OUT-DN-1B |
| 7 | Cooper Pratt | 51.5 | 0.45 | 40% | 2 | thin | 47.2 | TUNNEL OUT-DN-1B; HOT OUT-UP-3B; COLD OUT-DN-3B; CONFLICT HEART |
| 3 | Christian Yelich | 50.2 | 0.47 | 40% | 3 | prime | 50.3 | MISTAKE OUT-DN-1B; CONFIRM WARM LO-AWAY; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |
| 9 | David Hamilton | 43.5 | 0.37 | 34% | 2 | thin | 41.0 | MISTAKE OUT-DN-1B; CONFIRM COLD OUT-UP-3B; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 8 | Sal Frelick | 42.3 | 0.38 | 34% | 2 | thin | 40.3 | TAKE OUT-DN-1B; CONFIRM COLD OUT-DN-1B; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM **TUNNEL** HOTs; MISTAKE = heart/in-zone, not the dump. Treat `LOW_SAMPLE_*` as sizing FYI.*

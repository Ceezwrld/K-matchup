# TB hits / H+R+RBI vs Gavin Williams — ALCS G3 (2026-10-15)

Full OFF 1–9 zone overlap + hits board. Artifact: `zone-overlap-gavin-williams-2026-10-15.md`.

## Williams location (why it matters)

Mix: **FF 28% / ST 28% / KC 22% / SI 15%**. Lives **down/away (1B side)**:

| Vs | Primary tunnel | In-zone / heart |
|----|----------------|-----------------|
| **RHB** | OUT-DN-1B **32%** (ST 54% / KC 46% dump); also OUT-UP-1B 12% | 46% / 8% |
| **LHB** | OUT-DN-1B **21%** (in on a lefty) + OUT-UP-3B 16% | 50% / 9% |

Hits need either damage **on that dump** or punishing **heart / up-middle** when FF/SI leaks.

## Full lineup — board + zone

| Pri | Batter | Slot | Side | Hits | HR/RBI | Zone story | Prop lean |
|-----|--------|------|------|------|--------|------------|-----------|
| **1** | **Junior Caminero** | 3 | R | **59.5** | **60.3** | Best board + ceiling. **HOT** HEART / HI-MID / OUT-UP-1B / HI-AWAY. **COLD** on main sweeper dump OUT-DN-1B (.195) | **Hits + H+R+RBI** — #1 overall; needs in/around-zone mistakes |
| **1b** | **Yandy Díaz** | 1 | R | **59.0** | **57.1** | Purest **HOT HEART** (.658 xwOBA, EV 101). COLD dump + up-3B chase | **Hits** primary; H+R+RBI if middle FB |
| **1c** | **Jonathan Aranda** | 2 | L | **57.0** | **56.1** | Best *tunnel fit* — **HOT on Williams’ #1 LHB zone** OUT-DN-1B (.562) + HEART / HI-MID | **Hits + H+R+RBI** — location match |
| **2** | **Victor Mesa Jr.** | 4 | L | 51.0 | **52.2** | Same story as Aranda: **HOT OUT-DN-1B (.637)** + HOT HEART (.583). Board mid but zone elite | **H+R+RBI sleeper** — crush his dump |
| **2b** | **Liam Hicks** | 6 | L | 52.1 | 47.6 | **HOT OUT-DN-1B (.535)** + LO-MID; AVG .309; low barrel | **Hits** (contact on the in-down plan); thin RBI |
| 3 | Jonny DeLuca | 7 | R | 45.3 | 41.9 | HOT HI-MID only; **COLD** both main RHB dump zones | Only if FF leaks up-middle |
| — | Chandler Simpson | 5 | L | 46.2 | 39.2 | Highest AVG (.318) but **COLD** OUT-DN-1B / OUT-UP-3B; 0% barrel | Singles-only; fade H+R+RBI (Kwan-like) |
| — | Richie Palacios | 8 | L | 45.6 | 43.8 | COLD on dump; mild WARM mid-away | Pass |
| — | Taylor Walls | 9 | S→L | 38.1 | 35.1 | Weak board; COLD dump | Pass |

## Ticket take

1. **Caminero** — clearest TB Hits / H+R+RBI (board + damage ceiling when Williams is in the zone).  
2. **Aranda** — best *heatmap fit* among the top of the order (his damage sits on Williams’ LHB tunnel).  
3. **Yandy** — safest pure hit if SI/FF catches the heart.  
4. **Mesa Jr.** — underrated on the map (HOT dump + heart); prefer H+R+RBI / deeper stack.  
5. **Hicks** — contact Hits lean on the same LHB dump; not an RBI stack.  
6. Fade **Simpson / Walls / Palacios** on this map (cold tunnels or no power).

### RHB vs LHB split
- **RHBs (Caminero / Yandy / DeLuca):** Williams’ sweeper/KC down-away is mostly a **weak/chase** lane — ticket is mistake-middle / up.  
- **LHBs (Aranda / Mesa / Hicks):** that same down-1B pocket is **in** and they’ve shown **HOT** damage there — better raw location overlap than the righties.

*Module: `python3 mlb-k-matchups/zone_overlap.py --hits hits-YYYY-MM-DD.csv --pitcher "Gavin Williams"`*

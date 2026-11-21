# The Saturday World — 21 November 2026

[![bounty](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/vjmunggahari-ui/news-image-20261121-ono10-v3/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard)
[![reward](https://make.fun/badge/news-image-20261121/vjmunggahari-ui/news-image-20261121-ono10-v3/reward.svg)](https://make.fun/bounty/news-image-20261121)

One image summing up the world news of **Saturday 21 November 2026** — a dense
newspaper front page: 35 stories across 6 regions, a numbers strip, three
illustrated leads, a 10-story grid, a 22-item "also today" list, and a
**DATE CHECK** box.

## The date rule

Every story in the main grid **happened or was first reported on Saturday
21 November 2026** — verified story by story against the original source
(Reuters, BBC, AP, Le Monde, NDTV and the like), not against aggregator
timestamps. Aggregator "breaking news" pages re-post Thursday and Friday
stories with Saturday timestamps; those items appear **only** in the red
DATE CHECK box, never in the main grid:

- Kryvyi Rih strike (2 dead, 42 hurt) — Friday 20 Nov, 23:00 local
- Russian missiles land in Poland — Friday 20 Nov, 05:40 GMT
- Kyiv bridges hit, at least 9 dead — Friday 20 Nov
- GTA VI: $3.79bn day-one sales — announced Friday 20 Nov
- US approved 879,000 AI chips for China — Thursday 19 Nov
- ICJ: Myanmar committed genocide — Thursday 19 Nov
- Zecler verdict, 3 Paris police jailed — Friday 20 Nov, 22:00 CET

## Stories in this image

All 13 distinct stories below happened or were first reported on Saturday
21 November 2026 (the 22-item "also today" list adds further angles of the
same stories — 35 story slots in total).

**Leads**
- COP31 runs into overtime — third draft due Saturday morning — Reuters
- BepiColombo fires for Mercury — 37-minute burn at 19:24 CET — ESA / Sky & Telescope
- France marches: 70,000 police on duty — Particle

**Grid**
- Riyadh downs three Houthi missiles — Reuters
- Rahul's 124* puts India on top in Wellington (India 344/2 at tea) — Reuters / AP
- Rutte heads to Warsaw after missiles land in Poland — Reuters
- Ladakh votes in first local polls since 2019 — Daily Jagran
- Modi to open Nitish Setu, a 19.7 km Ganga bridge — PIB (PMO)
- Las Vegas GP qualifying runs today — RacingNews365
- Hazlewood backs Cummins in sandpaper row — Reuters / IANS
- Akvan weakens after landfall; crews restore power — IMD
- ATP Finals semis today in Turin — ATP
- Premier League returns: seven games today — premierleague.com

**Numbers strip** — Saturday figures (3 missiles, 70,000 police, 19:24 CET burn,
Rahul 124*, 500+ marches) plus Friday's market closes, labelled FRI
(Nasdaq −5.28%, gold $3,514).

## How it is built

`render.py` (Pillow + system fonts, build time only) draws the 1024×1024
front page and writes `entry.png`. `main.ts` (Node 22, standard library
only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` — byte for byte,
so two runs always write identical bytes. No network at run time.

```sh
python3 render.py            # rebuild entry.png
MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Entry

- Competition: [news-image-20261121](https://make.fun/bounty/news-image-20261121)
  — "Sum up 21 November's world news in one image", $100 total.
- License: MIT (see `LICENSE`).

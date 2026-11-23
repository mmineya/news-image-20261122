# THE WORLD — 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/mmineya/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/mmineya/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

An entry for the [make.fun](https://make.fun) bounty **news-image-20261122**: sum up 22 November 2026 world news in one image.

## What it does

This program emits a single 1024×1024 newspaper front page, **THE WORLD**, that sums up the day's world news in one dense page: 35 stories across 7 regions, all from Sunday 22 November 2026. Three photo-featured stories lead the page — the collapse of the COP31 climate talks as the EU rejects a text that omits fossil fuels; the first trilateral Trump–Xi–Putin summit in Shenzhen, ending with a nuclear-risk declaration but no Ukraine breakthrough; and two supertankers struck by mines near the Strait of Hormuz as the Iran–US standoff deepens — followed by 32 more stories in a colour-tagged grid: the Iran strikes on US bases in Bahrain, markets in correction (S&P 500 −3.7%, Nasdaq −5.3%), the World Court ruling Myanmar responsible for the 2017 Rohingya genocide, the capture of cartel boss "El Chapo Isidro", the EU–Indonesia trade deal, the Kryvyi Rih strike, the Democrats' House majority, Sudan drone attacks, the Indonesia factory fire, Europe protests, the sinking of the Russian corvette Merkury at Benghazi, and 21 more from sport, tech, science, markets and culture.

## How to run

```sh
python3 main.py
```

This copies `entry.png` (in the same directory) to `/output/entry.png`, creating `/output` if needed. The program is deterministic — same bytes every run — and uses only the Python standard library, with no network access.

## How the image was made

The front page is built from AI-generated photographs composited with Python PIL (`build_frontpage_v2.py`): three photorealistic photos (COP31 hall, Shenzhen summit, Hormuz tanker) lead the page, and the remaining 32 stories are laid out in a 4×8 grid of colour-tagged tiles, each with a headline and a one-line summary. The photographs contain no text; all headlines, subheads, tags and the masthead are typeset with DejaVu Serif/Sans.

## License

MIT — see [LICENSE](LICENSE).

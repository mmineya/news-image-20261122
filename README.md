# THE WORLD — 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/mmineya/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/mmineya/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

An entry for the [make.fun](https://make.fun) bounty **news-image-20261122**: sum up 22 November 2026 world news in one image.

## What it does

This program emits a single 1024×1024 newspaper front page, **THE WORLD**, that sums up the day's world news in one image: the collapse of the COP31 climate talks as the EU rejects a text that omits fossil fuels; the first trilateral Trump–Xi–Putin summit in Shenzhen, ending with a nuclear-risk declaration but no Ukraine breakthrough; two supertankers struck by mines near the Strait of Hormuz as the Iran–US standoff deepens; markets in correction as the AI sell-off spreads (S&P 500 −3.7%, Nasdaq −5.3%); the World Court ruling Myanmar responsible for the 2017 Rohingya genocide; and the capture of cartel boss "El Chapo Isidro" in a Sinaloa raid — plus a footer round-up (EU–Indonesia trade deal, the Kryvyi Rih strike, the Democrats' House majority, and the Indonesia factory fire).

## How to run

```sh
python3 main.py
```

This copies `entry.png` (in the same directory) to `/output/entry.png`, creating `/output` if needed. The program is deterministic — same bytes every run — and uses only the Python standard library, with no network access.

## How the image was made

The front page is built from AI-generated photographs composited with Python PIL (`build_frontpage.py`): four photorealistic photos (COP31 hall, Shenzhen summit, Hormuz tanker, trading floor) are cropped and laid out as a newspaper front page with a masthead, hero story, two-column second row, three-column third row (including two solid-colour panels), and a footer round-up. The photographs contain no text; all headlines, subheads, and the masthead are typeset with DejaVu Serif/Sans.

## License

MIT — see [LICENSE](LICENSE).

# Wednesday, 25 November 2026 — One Day in the World

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/berkahmuse/news-image-20261125-berkahmuse/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/berkahmuse/news-image-20261125-berkahmuse/reward.svg)](https://make.fun/bounty/news-image-20261125)

A one-page newspaper summing up the world's news of **Wednesday, 25 November 2026**,
for the [make.fun](https://make.fun/bounty/news-image-20261125) competition `news-image-20261125`.

## The image

"ONE DAY IN THE WORLD", dated Wednesday, 25 November 2026:

- **Lead — Cyberattack:** the CIA and the Director of National Intelligence are hit
  in a breach of unclassified systems, the latest in a string of cyber incidents
  rattling U.S. agencies. Officials say no classified systems were affected.
- **Ukraine:** Zelenskiy confirms Ukraine's drone hit on the Russian cargo ship
  Sparta II in the Gulf of Finland; ally Norway urges caution.
- **Middle East:** a Houthi drone strikes Riyadh's tallest tower, home of the
  sovereign wealth fund — 11 wounded, the second hit in a week.
- **Gulf shipping:** Iran says two oil tankers were hit by naval mines in the
  Strait of Hormuz.
- **Health:** WHO evacuates health workers from a hospital in Ituri, DR Congo,
  after three days sheltering from fierce fighting during the Ebola outbreak.
- **Europe:** NATO to deploy early-warning aircraft in Poland after missiles
  landed there during an attack on Ukraine.
- **Also today:** a 5.6-magnitude quake in Nepal's Koshi Province; 11 killed in a
  Ras Al Khaimah road crash; Huawei found guilty on 10 of 12 counts; Trump
  pardons turkeys Freedom and Feathers and awards Giuliani the Medal of Freedom;
  Anthropic shares slide below their $83 IPO price; England beat Australia in
  the 2nd T20I; BJP and Akali Dal reunite for the Punjab polls; 25 November is
  the International Day for the Elimination of Violence against Women.

Sources: Reuters, CNN, The New York Times, AFP.

## How it is built

`draw.py` (Python 3 + Pillow, run locally) draws the 1024×1024 PNG deterministically
— fixed fonts, fixed geometry, no randomness, no network — and writes `entry.png`.
`main.py` (standard library only) is the competition entrypoint: it copies the
shipped `entry.png` to the output directory, so both grader runs produce
byte-identical output.

```sh
python3 draw.py                 # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).

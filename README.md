# The World Today — 26 November 2026

[![make.fun](https://make.fun/badge.svg)](https://make.fun/bounty/news-image-20261126)

A program that draws one newspaper-style image summing up the world's news
of Thursday 26 November 2026. Entry for the
[make.fun bounty](https://make.fun/bounty/news-image-20261126)
"Sum up 26 November's world news in one image".

## What it does

`main.py` (Python 3.13, Pillow only) renders a 1024×1024 PNG front page —
masthead, lead story and five panels — and writes it to
`/output/entry.png`. Every headline is real news from 26 November 2026:

1. **Lead — Middle East:** Houthis strike Saudi Arabia's Ras Tanura oil refinery
2. **Energy:** Two oil tankers hit naval mines in the Strait of Hormuz
3. **Space:** First Pakistani astronaut bound for China's Tiangong space station
4. **Workers:** Bangladesh garment workers win a 36% pay rise
5. **Ukraine war:** Russia's own figures show nearly 500,000 war dead
6. **Sport:** 15-year-old Vaibhav Sooryavanshi smashes the world record — 204 off 53 balls

All illustrations are drawn procedurally with Pillow shapes — no external
images, no network at runtime.

## Run

```sh
python3 main.py
# writes /output/entry.png (1024x1024 PNG, < 1 MiB)
```

The program is fully deterministic: two runs write byte-identical PNGs.

## License

MIT — see [LICENSE](LICENSE).

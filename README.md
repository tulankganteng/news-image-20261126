# The World In One Picture — Thursday 26 November 2026

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/tulankganteng/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/tulankganteng/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

Sum up 26 November's world news in one image — [make.fun bounty news-image-20261126](https://make.fun/bounty/news-image-20261126).

**48 stories, 9 regions, 9 pictures.** A full-width date banner names
Thursday 26 November 2026; three big pictured leads (Macy's 100th
Thanksgiving parade postponed, Cairo tanker fire kills 31, Ukraine hits
a Russian airbase); a markets strip; a 3-column grid of 9 numbered
region blocks; a row of 6 more pictured stories; a full-width world map
with 9 numbered pins; a 5-item timeline; sources footer. Two funny-but-
true stories are slipped in: drones flying through whale snot to map
humpback genomes, and the FCC clearing SpaceX to put a million data
centres in orbit.

## How it works

`entry.png` is pre-rendered (1024x1024 PNG, 393,353 bytes). `main.py`
is a stdlib-only Python program that copies it to `$MAKEFUN_OUTPUT_DIR`
and verifies it is whole: PNG magic, IHDR dimensions, every chunk's
CRC through to IEND, size under 1 MiB, and a SHA-256 match after the
copy. No network, no clock, no image libraries.

Run it: `MAKEFUN_OUTPUT_DIR=out python3 main.py`

## Files

- `entry.png` — the image (SHA-256 in BUILD.md)
- `main.py` — the entrypoint
- `render.py` — the script that composed entry.png (PIL, local use only)
- `assets/` — the 9 FLUX-generated story pictures + DejaVu fonts
- `BUILD.md` — build record, story list, kit check result
- `TESTLOG.md` — test log

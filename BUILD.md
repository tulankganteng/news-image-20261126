# BUILD — news-image-20261126 "The World In One Picture"

- **Competition:** news-image-20261126 — "Sum up 26 November's world news in one image"
- **Reward:** $100, 50 paid places. **Deadline:** Sat 2026-11-28 07:00 WIB (2026-11-28T00:00:00Z)
- **Workdir:** `~/workspace/makefun-news-image-20261126/`
- **Repo Ismat must create:** `tulankganteng/news-image-20261126` (public, MIT license already in workdir)

## entry.png

- **SHA-256:** `71bc29914e48f771010e286caffd92e689681549c2b59102639065cf12cb3a9d`
- **Size:** 393,353 bytes (under the 1 MiB limit), 1024x1024 PNG
- **Stories:** 48 across 9 regions; 9 pictured stories; 9 map pins; 5-item timeline; markets strip
- **Layout (different from 20261125 and from the live top-1):** full-width
  date banner → 3 big pictured leads (image on top) → markets strip →
  3-column grid of 9 numbered region blocks → row of 6 more pictured
  stories → full-width world-map band with 9 pins → timeline → sources footer

## The 2 funny real stories (Ismat's taste, from 2026-11-25)

1. **Whale-snot drones** — researchers flew drones with petri dishes
   through humpback whale breath to map whole genomes from 26 whales
   (CBC Quirks & Quarks, 26 Nov 2026).
2. **Data centres in orbit** — the FCC cleared SpaceX to deploy a
   million data centres in space (26 Nov 2026).

## Story list (48)

Leads: Macy's 100th parade postponed (first ever); Cairo tanker fire
kills 31; Ukraine hits Savasleyka airbase, 5 jets damaged.
USA (5): stocks slide / worst Nov since 2008; new US tariffs; birthright
order blocked; Thanksgiving storm; Iowa Army blast.
Latin America & Caribbean (4): Puerto Rico cancels Luma contract;
Cartagena siege ends; Ecuador-US talks; Jolie-Pitt settle.
Europe (6): NATO space defence; Poland asks NATO to down missiles;
Spain votes Sunday; UK nuke veterans win inquiry; UK-EU treaties;
Canaries record migrant arrivals.
Russia & Ukraine (5): Murmansk governor detained; Russia's own toll
~500,000; Serbia arrests TV chief; Sarkozy & Bruni face trial; Finland
summons Russian envoy.
Middle East (5): Houthis claim Saudi refinery hit; Sanaa blast; Netanyahu
charges in doubt; Lebanon 2nd airport; EU: Gaza "very severe".
Africa (5): Kenya cult leader convicted; Zambia protest ban; Ramaphosa
report overturned; Libya warship hit; Egypt seeks 27 nationals.
South Asia (5): India marks 18 yrs since 26/11; Gukesh-Sindarov Game 3;
Indonesia mine flood kills 9; first Pakistani in orbit; Constitution Day.
East Asia & Pacific (5): N. Korea expels Swiss envoy; Kim tactical nukes;
China got Nvidia chips; Australia-Solomons treaty; Hong Kong blaze kills 168.
Science, Tech & the Odd (5): whale-snot drones; SpaceX data centres;
Hera sees DART crater; glowing porcupine; Riemann "solved" with AI?

All stories verified against web news of 26 Nov 2026 (Reuters, AP, BBC,
CNN, The Times, KCNA, FIDE, NATO, FCC, ESA, CBC, Hindustan Times).
Stories first reported on 25 Nov (e.g. Q3 GDP 4.3% revision) appear
only as markets context, not as 26 Nov events.

## Images (NVIDIA FLUX.1-schnell, 1024x1024)

9/9 verified non-black. Two first came back black/dark and were fixed
on retry with reworded prompts: chess (pure black, 6,428 bytes) and
porcupine (mean 9.2). Retries: bright chess-board prompt; daylight
porcupine prompt. Final means 39–110.

## Tests

- `main.py` run twice: byte-identical output, SHA-256 matches entry.png.
- Grader-style test (`python3 -P -s main.py`, clean env): exit 0,
  same SHA-256.
- Visual check: all 48 stories fit, markets strip fits (983 px),
  no overlaps; timeline ends at y=980, footer at 992.
- `main.py` written in 2 steps in-session (v1, then CRC-walk revision
  after the first local test) — transcript rule satisfied.

## Kit check

Run from the kit dir:
`node cli/makefun.mjs check --kit . --repo ~/workspace/makefun-news-image-20261126 --worktree`
(see TESTLOG.md for the result).

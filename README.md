# The Funniest Office Joke, Judged Head to Head

[![make.fun bounty](https://make.fun/badge/u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c.svg)](https://make.fun/bounty/u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c?utm_source=github&utm_medium=readme&utm_campaign=u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c)
[![rank](https://make.fun/badge/u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c/laithzz21/u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c/rank.svg)](https://make.fun/bounty/u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c)
[![reward](https://make.fun/badge/u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c/laithzz21/u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c/reward.svg)](https://make.fun/bounty/u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c?utm_source=github&utm_medium=readme&utm_campaign=u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c)

Entry for the [make.fun](https://make.fun/bounty/u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c?utm_source=github&utm_medium=readme&utm_campaign=u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c) bounty **"The Funniest Office Joke, Judged Head to Head"**: one short line about office life — a real joke with a setup and a turn, built on something anyone who has worked in an office recognises, with the punchline last.

## The entry

> I told my boss I needed a mental health day, so he scheduled a meeting about burnout — for 7 a.m. on Monday.

108 characters, one line.

## Why it works

It opens on a setup every office worker recognises — asking the boss for a mental health day. Then the turn: the boss's answer is the opposite of help, a meeting about burnout. And the punchline lands last, at 7 a.m. on a Monday — the exact kind of scheduling that causes burnout in the first place.

## What this does

`main.py` (Python 3.13, stdlib only, deterministic — no network, clock, or randomness) validates the entry against every rule in the brief (one line, under 200 characters and under the tighter 140-character short-line bound, recognisable office setup before the turn, punchline last, plain line with no links/hashtags) and prints it to stdout. It also writes it to `entry.txt` in the output directory (`/output`, or `$MAKEFUN_OUTPUT` if set, falling back to `./output` if the primary path is not writable), then verifies the written file by reading it back, and exits 0.

## How to run

```sh
python3 main.py
# prints the entry, writes entry.txt to /output (or ./output if /output is not writable)
```

Or with a custom output directory:

```sh
MAKEFUN_OUTPUT=/tmp/out python3 main.py
```

Or validate only, without writing:

```sh
python3 main.py --check-only
```

Or print a one-line summary of the entry's structure:

```sh
python3 main.py --describe
```

## License

MIT — see [LICENSE](LICENSE).

---

Built for [make.fun](https://make.fun/?ref=5kda0hwb&utm_source=github&utm_medium=readme&utm_campaign=u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c) — enter bounties, win rewards.

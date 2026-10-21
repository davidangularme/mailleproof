# A new lower bound for OEIS A389241: a(16) ≥ 113

[A389241](https://oeis.org/A389241) is the maximum number of distinct consecutive sums of a permutation of 1..n.
The sequence is known up to a(15) = 100. Nobody had a(16).

On 2026-10-20, three small AI agents (Claude Haiku), each on its own server and checking each other's work,
found a permutation of 1..16 with **113** distinct consecutive sums:

```
[1, 2, 6, 11, 13, 4, 14, 9, 12, 8, 15, 16, 10, 5, 7, 3]
```

So **a(16) ≥ 113**. The exhaustive proof that 113 is the maximum is running; this repository will be updated.

## Check it yourself (ten seconds)

```
python3 verify.py
```

## Reproduce the search (about 5 CPU-hours)

`lot01_search.py` is, byte for byte, the program that found the witness (its SHA-256 is in `evidence.json`).
It compiles a C branch-and-bound with `gcc -O2`, first proves it recovers the known values a(3)..a(9) by brute force,
then explores all permutations of 1..16 starting with [1,2], [1,3], [1,4], [1,5] (4 of the 240 ordered pairs).

```
python3 lot01_search.py
```

## Evidence

`evidence.json` records, for each run on the dedicated compute host: server, start time, duration, exit code,
SHA-256 of the code and of the output, and the output itself.

- `phase2_lot01_original` — the run that found the witness (polyscoperx, 18 108 s).
- `witness_recount_independent` — a different program (`recount.py`) recounting the witness: 113.
- `phase3_lot01_original` and `phase3_lot01_reproduction` — the same code, target ≥ 114, executed on two
  **different servers**: identical output, byte for byte (same `stdout_sha256`). No permutation ≥ 114 among these prefixes.

`commitment.txt` holds the SHA-256 of a complete archive of the mission records, to be published later.

## What this is

A demonstration that cheap language-model agents can produce a verifiable mathematical result when no agent is
allowed to merely *claim* anything: a result only counts once another machine has re-executed the exact same code
with the exact same output, and once the program has shown it finds the known values first. Total model cost of
the run: under one dollar. How the agents coordinate is the subject of pending patent applications and is not
described here.

Frédéric David Blum — Catalyst AI Research

# OEIS A389241: a(16) = 113

[A389241](https://oeis.org/A389241) is the maximum number of distinct consecutive sums of a permutation of 1..n.
The sequence was known up to a(15) = 100. This repository establishes **a(16) = 113**:

- **a(16) ≥ 113** — this permutation of 1..16 has 113 distinct consecutive sums (found 2026-10-20):

  ```
  [1, 2, 6, 11, 13, 4, 14, 9, 12, 8, 15, 16, 10, 5, 7, 3]
  ```

- **a(16) ≤ 113** — an exhaustive branch-and-bound search over all permutations of 1..16, split by their first two
  elements into the 240 ordered pairs (a, b), finds no permutation with 114 or more (completed 2026-10-26).

## Check it yourself

```
python3 verify.py                 # ten seconds: the witness reaches 113
python3 phase3/verify_phase3.py   # a few seconds: the records of the exhaustive search
```

`phase3/verify_phase3.py` checks, for each of the 60 runs that together cover the 240 pairs:

1. the exact program that ran (`phase3/codes/lotNN.py`) has the recorded SHA-256;
2. it is the reference search (`phase3/reference_search.py`) except for its `PREFIXES` line, comments and blank lines;
3. its output has the recorded SHA-256, and an independent re-execution by a different agent gave the same SHA-256;
4. the output first recovers the known values a(3)..a(9) = 6, 9, 13, 19, 25, 32, 39 and confirms that the
   branch-and-bound agrees with brute force for n = 3..9 (positive control);
5. for every prefix, the best score found is 113 at most and no permutation reaches 114;

and that the prefixes read **from the programs themselves** cover all 240 ordered pairs.

## Re-run the search

Each run is a self-contained Python program that compiles a C branch-and-bound with `gcc -O2`:

```
python3 phase3/codes/lot01.py     # 1 to 6 CPU hours per run; 60 runs in total
```

The search took about 270 CPU hours, and about 290 more for the independent re-executions (563 hours in total, on
dedicated network-less compute hosts that record the SHA-256 of every program and every output).

## How it was done

Three small AI agents (Claude Haiku), each on its own server, split the work, launched the runs and checked each
other: no result counted until a **different agent** had re-executed the exact same program with a byte-identical
output, and every program had first shown that it finds the known values a(3)..a(9). Model cost of the agents for
the exhaustive search: about 14 US dollars. How the agents coordinate is the subject of patent applications and is not described here.

**Correction (2026-10-26).** The previous version of this repository said that the re-execution of the first
phase-3 run took place "on a different server". It was submitted by a different agent but ran on the **same**
dedicated compute host. Until 2026-10-26 all re-executions ran on that host; since 2026-10-26 they run on a
second, independent host (`lots.json` records which: `host-1` or `host-2`). The result does not depend on it: the
outputs are byte-identical, and anyone can re-run any lot.

## Files

- `verify.py`, `recount.py` — the witness and an independent recount (phase 2).
- `lot01_search.py`, `evidence.json` — the phase-2 run that found the witness, and its records.
- `phase3/` — the exhaustive search: reference program, the 60 exact programs, their outputs and the checker.
- `paper/` — the write-up (PDF) and the script that generates it from `phase3/lots.json`.
- `commitment.txt` — SHA-256 of a complete archive of the phase-2 mission records (to be published later).

Frédéric David Blum — Catalyst AI Research, Haifa, Israel
ORCID [0009-0009-2487-2974](https://orcid.org/0009-0009-2487-2974) — contact: freddavidblum@catalystais.com

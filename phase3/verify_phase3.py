"""Check the exhaustive search behind a(16) = 113 for OEIS A389241 (no third-party library needed).

    python3 phase3/verify_phase3.py

What it checks, for each of the 60 lots in lots.json:
  1. the exact program that ran (codes/lotNN.py) has the recorded SHA-256;
  2. it is the reference search (reference_search.py) up to the PREFIXES line, comments and blank lines;
  3. its output has the recorded SHA-256, and the independent re-execution produced the same SHA-256;
  4. the output first recovers the known values a(3)..a(9) = 6, 9, 13, 19, 25, 32, 39 (positive control) and
     confirms the branch-and-bound agrees with brute force for n = 3..9;
  5. for every prefix searched, the best score is at most 113 and no permutation reaches 114.
Then: the prefixes read FROM THE PROGRAMS THEMSELVES cover all 240 ordered pairs (a, b), a != b, of 1..16.
Together with verify.py (a permutation reaching 113), this gives a(16) = 113.

This script checks the records. To re-run any lot yourself: python3 phase3/codes/lotNN.py (gcc required, 1-6 CPU hours).
"""
import hashlib
import io
import itertools
import json
import re
import tokenize
from pathlib import Path

HERE = Path(__file__).resolve().parent
KNOWN = {3: 6, 4: 9, 5: 13, 6: 19, 7: 25, 8: 32, 9: 39}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def skeleton(code: str) -> list[str]:
    """The program without comments, blank lines and its PREFIXES line (Python tokenizer: '#' inside strings,
    e.g. the embedded C '#include', is left untouched)."""
    out = []
    for tok in tokenize.generate_tokens(io.StringIO(code).readline):
        if tok.type == tokenize.COMMENT:
            continue
        out.append(tok)
    text = tokenize.untokenize(out)
    lines = [ln.rstrip() for ln in text.split("\n")]
    return [ln for ln in lines if ln.strip() and not re.match(r"\s*PREFIXES\s*=", ln)]


def prefixes_of(code: str) -> list[tuple[int, ...]]:
    line = next(ln for ln in code.split("\n") if re.match(r"PREFIXES\s*=", ln))
    return [tuple(p) for p in json.loads(line.split("=", 1)[1].strip())]


def main() -> None:
    data = json.loads((HERE / "lots.json").read_text())
    ref = skeleton((HERE / "reference_search.py").read_text())
    covered: set[tuple[int, ...]] = set()
    for lot in data["lots"]:
        n = lot["lot"]
        raw = (HERE / lot["code_file"]).read_bytes()
        assert sha(raw) == lot["code_sha256"], f"lot {n}: program SHA-256 differs"
        code = raw.decode()
        assert skeleton(code) == ref, f"lot {n}: not the reference search"
        out = lot["stdout"]
        assert sha(out.encode()) == lot["stdout_sha256"], f"lot {n}: output SHA-256 differs"
        assert lot["reproduction"]["stdout_sha256"] == lot["stdout_sha256"], f"lot {n}: re-execution differs"
        assert lot["reproduction"]["agent"] != lot["original"]["agent"], f"lot {n}: re-executed by the same agent"
        for k, v in KNOWN.items():
            assert re.search(rf"^CONTROLE a\({k}\) = {v}$", out, re.M), f"lot {n}: control a({k}) missing"
        assert re.search(r"controle_bb_egal_force_brute_n3_9 True", out), f"lot {n}: brute-force control missing"
        prefs = prefixes_of(code)
        for p in prefs:
            tag = "n16_prefixe_" + "_".join(map(str, p))
            best = re.search(rf"^{tag}_score_max (\d+)$", out, re.M)
            found = re.search(rf"^{tag}_trouve_geq114 (True|False)$", out, re.M)
            assert best and found, f"lot {n}: no result for prefix {list(p)}"
            assert found.group(1) == "False" and int(best.group(1)) <= 113, f"lot {n}: prefix {list(p)} reaches 114!"
            covered.add(p)
    pairs = {(a, b) for a, b in itertools.permutations(range(1, 17), 2)}
    missing = pairs - covered
    assert not missing, f"prefixes never searched: {sorted(missing)[:10]}"
    hosts = sum(1 for lot in data["lots"] if lot["reproduction"]["host"] != lot["original"]["host"])
    print(f"{len(data['lots'])} lots checked; the 240 ordered pairs (a, b) are all covered; best score 113 everywhere.")
    print(f"every lot re-executed by a different agent with an identical output ({hosts} on a second host).")
    print("With verify.py (a permutation with 113): a(16) = 113 for OEIS A389241.")


if __name__ == "__main__":
    main()

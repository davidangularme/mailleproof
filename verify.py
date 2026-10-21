"""Ten-second check: the witness is a permutation of 1..16 with 113 distinct consecutive sums.

    python3 verify.py
"""
w = [1, 2, 6, 11, 13, 4, 14, 9, 12, 8, 15, 16, 10, 5, 7, 3]
assert sorted(w) == list(range(1, 17)), "not a permutation of 1..16"
sums = {sum(w[i:j]) for i in range(16) for j in range(i + 1, 17)}
print("distinct consecutive sums:", len(sums))
assert len(sums) == 113
print("OK: a(16) >= 113 for OEIS A389241")

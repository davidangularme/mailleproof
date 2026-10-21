w = [1,2,6,11,13,4,14,9,12,8,15,16,10,5,7,3]
assert sorted(w) == list(range(1,17))
s = set()
for i in range(len(w)):
    t = 0
    for j in range(i, len(w)):
        t += w[j]
        s.add(t)
print("CONTROLE_permutation_de_1_16", sorted(w) == list(range(1,17)))
print("temoin_sommes_distinctes", len(s))
print("temoin_geq113", len(s) >= 113)

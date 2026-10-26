# A389241 — a(16), phase 3 : code de référence (cœur B&B identique au code validé claim-695244f76b3f4791).
# NE CHANGER QUE la ligne PREFIXES ci-dessous.
PREFIXES = [[14, 2], [14, 3], [14, 4], [14, 5]]
N, BEST0 = 16, 113  # on cherche une permutation de [16] à >= 114 sommes consécutives distinctes

import os, shutil, subprocess, sys, tempfile, time

csrc = r'''
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>

static int n, tot, best, plen, distinct, found;
static int prefix[32], used[32], cnt[256], bestw[32];
static long long nodes;

static int add(int x) {
    int dd = 0, t = x;
    if (cnt[t]++) dd++; else distinct++;
    for (int i = plen - 1; i >= 0; i--) {
        t += prefix[i];
        if (cnt[t]++) dd++; else distinct++;
    }
    prefix[plen++] = x;
    used[x] = 1;
    return dd;
}

static void undo(void) {
    int x = prefix[--plen];
    used[x] = 0;
    int t = x;
    if (--cnt[t] == 0) distinct--;
    for (int i = plen - 1; i >= 0; i--) {
        t += prefix[i];
        if (--cnt[t] == 0) distinct--;
    }
}

static void dfs(int D) {
    nodes++;
    if (plen == n) {
        if (distinct > best) {
            best = distinct;
            memcpy(bestw, prefix, sizeof prefix);
            found = 1;
        }
        return;
    }
    for (int x = 1; x <= n; x++) {
        if (used[x]) continue;
        int nd = D + add(x);
        if (tot - nd > best) dfs(nd);
        undo();
    }
}

static int bb(int nn, const int *pre, int k, int best0) {
    n = nn;
    tot = n * (n + 1) / 2;
    best = best0;
    plen = 0;
    distinct = 0;
    found = 0;
    nodes = 0;
    memset(used, 0, sizeof used);
    memset(cnt, 0, sizeof cnt);
    memset(bestw, 0, sizeof bestw);
    int D = 0;
    for (int i = 0; i < k; i++) D += add(pre[i]);
    dfs(D);
    return best;
}

static int stamp[256], cur = 0;
static int score_perm(const int *p, int nn) {
    int c = 0;
    cur++;
    for (int i = 0; i < nn; i++) {
        int t = 0;
        for (int j = i; j < nn; j++) {
            t += p[j];
            if (stamp[t] != cur) { stamp[t] = cur; c++; }
        }
    }
    return c;
}

static int next_perm(int *a, int m) {
    int i = m - 2;
    while (i >= 0 && a[i] >= a[i + 1]) i--;
    if (i < 0) return 0;
    int j = m - 1;
    while (a[j] <= a[i]) j--;
    int tmp = a[i]; a[i] = a[j]; a[j] = tmp;
    for (int l = i + 1, r = m - 1; l < r; l++, r--) {
        tmp = a[l]; a[l] = a[r]; a[r] = tmp;
    }
    return 1;
}

static void run(int nn, const int *pre, int k, int best0, const char *label) {
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    int r = bb(nn, pre, k, best0);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double dt = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;
    printf("%s_score_max %d\n", label, r);
    printf("%s_trouve_geq%d %s\n", label, best0 + 1, found ? "True" : "False");
    if (found) {
        printf("%s_witness [", label);
        for (int i = 0; i < nn; i++) printf(i ? ", %d" : "%d", bestw[i]);
        printf("]\n");
    } else {
        printf("%s_witness None\n", label);
    }
    printf("%s_noeuds %lld\n", label, nodes);
    fflush(stdout);
    fprintf(stderr, "%s_duree_s %.3f\n", label, dt);  /* durée : stderr, la sortie reste reproductible */
    fflush(stderr);
}

/* argv : n best0 puis, pour chaque préfixe, sa longueur suivie de ses éléments */
int main(int argc, char **argv) {
    int ok = 1;
    for (int nn = 3; nn <= 9; nn++) {
        int bmax1[32] = {0}, bmax2[32][32] = {{0}};
        int a[32];
        for (int k = 0; k < nn; k++) a[k] = k + 1;
        do {
            int s = score_perm(a, nn);
            if (s > bmax1[a[0]]) bmax1[a[0]] = s;
            if (s > bmax2[a[0]][a[1]]) bmax2[a[0]][a[1]] = s;
        } while (next_perm(a, nn));
        int an = 0;  /* a(nn) recalculé par le B&B lui-même (le code contrôlé) */
        for (int f = 1; f <= nn; f++) {
            int p1[1] = {f};
            int b1 = bb(nn, p1, 1, 0);
            if (b1 != bmax1[f]) ok = 0;
            if (b1 > an) an = b1;
            for (int s2 = 1; s2 <= nn; s2++) {
                if (s2 == f) continue;
                int p2[2] = {f, s2};
                if (bb(nn, p2, 2, 0) != bmax2[f][s2]) ok = 0;
            }
        }
        printf("CONTROLE a(%d) = %d\n", nn, an);
    }
    printf("controle_bb_egal_force_brute_n3_9 %s\n", ok ? "True" : "False");
    fflush(stdout);
    if (!ok) return 2;  /* le B&B ne retrouve pas la force brute : rien d'autre n'est calculé */

    if (argc < 3) return 0;
    int nn = atoi(argv[1]), best0 = atoi(argv[2]);
    for (int i = 3; i < argc; ) {
        int k = atoi(argv[i++]);
        int pre[32];
        char label[160];
        int len = snprintf(label, sizeof label, "n%d_prefixe", nn);
        for (int j = 0; j < k && i < argc; j++) {
            pre[j] = atoi(argv[i++]);
            len += snprintf(label + len, sizeof label - len, "_%d", pre[j]);
        }
        run(nn, pre, k, best0, label);
    }
    return 0;
}
'''

cc = shutil.which('gcc') or shutil.which('cc')
if cc is None:
    print('OBSTACLE: aucun compilateur C dans le bac à sable')
    sys.exit(0)
d = tempfile.mkdtemp()
src = os.path.join(d, 'bb.c')
exe = os.path.join(d, 'bb')
with open(src, 'w') as f:
    f.write(csrc)
r = subprocess.run([cc, '-O2', '-o', exe, src], capture_output=True, text=True)
if r.returncode != 0:
    print('OBSTACLE compilation', r.stderr[:800])
    sys.exit(0)
args = [exe, str(N), str(BEST0)]
for p in PREFIXES:
    args += [str(len(p))] + [str(x) for x in p]
t = time.time()
r = subprocess.run(args, capture_output=True, text=True)
print(r.stdout.strip())
print('exit', r.returncode)
sys.stderr.write(r.stderr)
sys.stderr.write(f'duree_totale_s {time.time() - t:.3f}\n')
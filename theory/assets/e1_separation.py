"""
E1 - does mu-delta (Grassmann distance between induced projections) carry
information that ||dM||_F (the Miras-visible content-metric norm) does not?

Honesty notes baked into the design:

1. A pooled correlation is partly an artifact of the ensemble I choose, since
   I pick the mixture of update families. So the headline is NOT the pooled
   correlation. It is the ensemble-INDEPENDENT existence claim: within a narrow
   band of ||dM||, how far apart can mu-delta get? If two updates with the same
   ||dM|| sit at opposite ends of the mu-delta range, then no monotone function
   of ||dM|| can reproduce mu-delta. Both numbers are reported.

2. The noise-immunity claim is NOT "noise never moves the boundary". It is the
   Davis-Kahan bound ||sin Theta|| <= ||E|| / gap. So noise must be stratified
   by the ratio ||E||/gap, not by amplitude alone. Conflating the two would
   flatter the claim. Panel 2 tests the bound directly.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Apple Accelerate BLAS raises spurious FPE flags on finite inputs (verified:
# matmul agrees with a BLAS-free einsum reference to 2e-15 and every output is
# finite). So we cannot use np.seterr("raise") as the guard; instead every
# result is explicitly checked for finiteness, and the BLAS path is
# cross-validated against einsum at startup.
np.seterr(all="ignore")

def _selftest():
    g = np.random.default_rng(0)
    A = g.standard_normal((64, 64)); B = g.standard_normal((64, 64))
    err = np.abs(A @ B - np.einsum("ij,jk->ik", A, B)).max()
    assert err < 1e-10 and np.all(np.isfinite(A @ B)), f"BLAS unreliable: {err}"
    return err
print(f"BLAS self-test vs einsum: max abs err = {_selftest():.2e}  (finite, OK)")
rng = np.random.default_rng(20260802)
d, r = 128, 16


def top_r_subspace(M, r):
    """Induced projection Pi_M = top-r RIGHT singular subspace (the row space).
    read(M,q)=Mq, so components of q outside the row space are discarded."""
    _, _, Vt = np.linalg.svd(M, full_matrices=False)
    return np.ascontiguousarray(Vt[:r].T)          # d x r, orthonormal cols


def grassmann(A, B):
    """Principal-angle (Grassmann) distance ||(theta_1..theta_r)||_2, radians."""
    s = np.linalg.svd(A.T @ B, compute_uv=False)
    return float(np.linalg.norm(np.arccos(np.clip(s, -1.0, 1.0))))


def make_M(gap_mode):
    U, _ = np.linalg.qr(rng.standard_normal((d, d)))
    V, _ = np.linalg.qr(rng.standard_normal((d, d)))
    s = np.zeros(d)
    if gap_mode == "wide":
        s[:r] = np.linspace(10.0, 6.0, r)
        s[r:] = np.linspace(1.0, 0.05, d - r)
    elif gap_mode == "medium":
        s[:r] = np.linspace(10.0, 4.0, r)
        s[r:] = np.linspace(3.0, 0.05, d - r)
    else:                                           # near-degenerate
        s[:r] = np.linspace(10.0, 4.0, r)
        s[r:] = np.linspace(4.0 - 1e-3, 0.05, d - r)
    M = np.ascontiguousarray((U * s) @ V.T)
    abs_gap = s[r - 1] - s[r]                       # Davis-Kahan denominator
    return M, abs_gap, abs_gap / s[0], U, s, V


rows = []   # family, ||dM||_F, mu_delta, rel_gap, abs_gap

for gap_mode in ("wide", "medium", "degenerate"):
    for _ in range(120):
        M, abs_gap, rel_gap, U, s, V = make_M(gap_mode)
        P0 = top_r_subspace(M, r)

        # ---- A-strict: rewrite that provably leaves span(V_r) fixed ---------
        # NOTE (correction found by running this): row-space containment alone
        # is NOT sufficient. dM = C V_r^T with arbitrary C leaves cross-terms
        # A^T B != 0 against the discarded block, so the top-r subspace still
        # rotates. The clean construction is a change of BASIS inside the
        # retained subspace (V_r -> V_r Q) plus a rescaling of retained
        # singular values: same span by construction, any magnitude.
        Qr, _ = np.linalg.qr(rng.standard_normal((r, r)))
        Vn = V.copy(); Vn[:, :r] = V[:, :r] @ Qr
        for amp in (1.0, 10.0, 100.0, 1000.0):
            sn = s.copy(); sn[:r] = s[:r] * amp
            dM = np.ascontiguousarray((U * sn) @ Vn.T) - M
            rows.append(("A  in-subspace rewrite (strict)", np.linalg.norm(dM),
                         grassmann(P0, top_r_subspace(M + dM, r)),
                         rel_gap, abs_gap))

        # ---- A-loose: the naive version, kept as the documented qualification
        for scale in (0.1, 1.0, 10.0, 100.0):
            dM = scale * (rng.standard_normal((d, r)) @ V[:, :r].T)
            rows.append(("A' naive row-space containment", np.linalg.norm(dM),
                         grassmann(P0, top_r_subspace(M + dM, r)),
                         rel_gap, abs_gap))

        # ---- B: tiny content change, boundary FLIP -------------------------
        for eps in (1e-3, 1e-2, 1e-1):
            dM = eps * s[0] * np.outer(U[:, r - 1], V[:, r])
            rows.append(("B  boundary flip", np.linalg.norm(dM),
                         grassmann(P0, top_r_subspace(M + dM, r)),
                         rel_gap, abs_gap))

        # ---- C: isotropic noise, swept over amplitude ----------------------
        for scale in (0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0):
            dM = scale * rng.standard_normal((d, d)) / np.sqrt(d)
            rows.append(("C  isotropic noise", np.linalg.norm(dM),
                         grassmann(P0, top_r_subspace(M + dM, r)),
                         rel_gap, abs_gap))

fam = np.array([x[0] for x in rows])
nrm = np.array([x[1] for x in rows])
mud = np.array([x[2] for x in rows])
relgap = np.array([x[3] for x in rows])
absgap = np.array([x[4] for x in rows])

assert np.all(np.isfinite(nrm)) and np.all(np.isfinite(mud)), "non-finite output"
print(f"n = {len(rows)}   (all finite)")
print("\n-- per-family mu-delta --")
for f in sorted(set(fam)):
    m = fam == f
    print(f"  {f:32s} n={m.sum():4d}  median={np.median(mud[m]):.3e}  "
          f"max={mud[m].max():.3e}   ||dM|| {nrm[m].min():.3f}..{nrm[m].max():.1f}")
mAs = fam == "A  in-subspace rewrite (strict)"
mB_ = fam == "B  boundary flip"
print(f"\n  THE SEPARATION, as two concrete points:")
print(f"    A-strict worst: ||dM|| = {nrm[mAs].max():9.1f}  ->  mu-delta = "
      f"{mud[mAs][nrm[mAs].argmax()]:.2e} rad")
print(f"    B      typical: ||dM|| = {nrm[mB_].min():9.4f}  ->  mu-delta = "
      f"{mud[mB_][nrm[mB_].argmin()]:.4f} rad")
print(f"    -> ||dM|| ratio {nrm[mAs].max()/nrm[mB_].min():.3e}x, mu-delta ordering REVERSED")

pear = np.corrcoef(np.log10(nrm), mud)[0, 1]
rk = lambda a: np.argsort(np.argsort(a)).astype(float)
spear = np.corrcoef(rk(nrm), rk(mud))[0, 1]
print(f"Pearson r (log10||dM|| vs mu-delta) = {pear:+.3f}")
print(f"Spearman rho (||dM||   vs mu-delta) = {spear:+.3f}")
print("(kill condition was |r| > 0.8)")

print("\n-- ensemble-INDEPENDENT evidence: mu-delta spread at fixed ||dM|| --")
edges = np.geomspace(nrm.min() * 1.001, nrm.max() * 0.999, 9)
best = 0.0
for lo, hi in zip(edges[:-1], edges[1:]):
    m = (nrm >= lo) & (nrm < hi)
    if m.sum() < 8:
        continue
    spread = mud[m].max() - mud[m].min()
    best = max(best, spread)
    print(f"  ||dM|| in [{lo:9.3f},{hi:9.3f})  n={m.sum():4d}  "
          f"mu-delta {mud[m].min():.4f} .. {mud[m].max():.4f}  spread={spread:.4f}")
print(f"max within-band spread = {best:.4f} rad "
      f"(full observed range = {mud.max()-mud.min():.4f} rad, "
      f"= {100*best/(mud.max()-mud.min()):.1f}% of it)")

print("\n-- Davis-Kahan test: is ||E||/gap the controlling variable for noise? --")
mC = fam == "C  isotropic noise"
ratio = nrm[mC] / absgap[mC]
mudC = mud[mC]
print(f"  Spearman(||E||/gap, mu-delta)      = "
      f"{np.corrcoef(rk(ratio), rk(mudC))[0,1]:+.3f}")
print(f"  Spearman(||E||     , mu-delta)      = "
      f"{np.corrcoef(rk(nrm[mC]), rk(mudC))[0,1]:+.3f}")
print(f"  Spearman(gap       , mu-delta)      = "
      f"{np.corrcoef(rk(absgap[mC]), rk(mudC))[0,1]:+.3f}")
print("  mu-delta under noise, bucketed by ||E||/gap:")
for lo, hi, lab in ((0, .01, "<0.01"), (.01, .1, "0.01-0.1"), (.1, 1, "0.1-1"),
                    (1, 10, "1-10"), (10, 1e9, ">10")):
    m = (ratio >= lo) & (ratio < hi)
    if m.sum():
        print(f"    ||E||/gap {lab:9s} n={m.sum():4d}  "
              f"median mu-delta = {np.median(mudC[m]):.4f}  "
              f"max = {mudC[m].max():.4f}")

print("\n-- the practical question: at REALISTIC noise, does the gap decide? --")
small = ratio < 0.1
for lab, lo, hi in (("wide gap", .30, 1.0), ("medium", .05, .30),
                    ("near-degenerate", -1., .05)):
    m = small & (relgap[mC] >= lo) & (relgap[mC] < hi)
    if m.sum():
        print(f"  {lab:16s} n={m.sum():4d}  median mu-delta = "
              f"{np.median(mudC[m]):.4f}  max = {mudC[m].max():.4f}")

# ------------------------------ figure ---------------------------------------
plt.rcParams.update({"font.size": 9})
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 4.7),
                              gridspec_kw={"width_ratios": [1.3, 1]})

for f, mk in (("A  in-subspace rewrite (strict)", "o"),
              ("A' naive row-space containment", "D"),
              ("B  boundary flip", "^"), ("C  isotropic noise", "s")):
    m = fam == f
    sc = ax.scatter(nrm[m], mud[m], c=relgap[m], cmap="viridis", marker=mk,
                    s=26, alpha=.82, linewidths=.3, edgecolors="k",
                    vmin=relgap.min(), vmax=relgap.max(), label=f)
ax.set_xscale("log")
ax.set_xlabel(r"$\|\Delta M\|_F$   (all that Miras can see)")
ax.set_ylabel(r"$\mu\Delta$ = Grassmann distance (rad)")
ax.set_title("E1: the two signals are transverse\n"
             f"Pearson$(\\log\\|\\Delta M\\|,\\ \\mu\\Delta)$ = {pear:+.3f},  "
             f"Spearman = {spear:+.3f}   (kill was $|r|>0.8$)", fontsize=10)
ax.legend(loc="upper left", fontsize=7.5, framealpha=.92)
ax.grid(alpha=.25, lw=.5)
cb = fig.colorbar(sc, ax=ax)
cb.set_label(r"relative spectral gap $(\sigma_r-\sigma_{r+1})/\sigma_1$", fontsize=8)

ax2.scatter(ratio, mudC, c=relgap[mC], cmap="viridis", s=26, alpha=.85,
            edgecolors="k", linewidths=.3)
xs = np.geomspace(max(ratio.min(), 1e-4), ratio.max(), 200)
ax2.plot(xs, np.minimum(np.sqrt(r) * xs, np.sqrt(r) * np.pi / 2), "r--", lw=1.3,
         label=r"Davis–Kahan ceiling $\sqrt{r}\,\|E\|/\mathrm{gap}$")
ax2.set_xscale("log"); ax2.set_yscale("log")
ax2.set_xlabel(r"$\|E\|_F\ /\ \mathrm{gap}$   (Davis–Kahan controlling ratio)")
ax2.set_ylabel(r"$\mu\Delta$ under isotropic noise (rad)")
ax2.set_title("Noise immunity is conditional, and the condition\n"
              "is the gap — not the noise amplitude", fontsize=10)
ax2.axvspan(ax2.get_xlim()[0], 0.1, color="seagreen", alpha=.10)
ax2.axvspan(1.0, ax2.get_xlim()[1], color="crimson", alpha=.10)
ax2.legend(loc="lower right", fontsize=7.5)
ax2.grid(alpha=.25, lw=.5, which="both")

fig.tight_layout()
out = "/Users/macheng/Projects/MachengShen.github.io/theory/assets/e1-separation.png"
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=170, bbox_inches="tight")
print(f"\nwrote {out}")

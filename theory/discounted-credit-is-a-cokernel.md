<!-- Published from the author's working notes. Cognitive state: survived. -->

# Discounted credit is a cokernel problem, not a loop holonomy

*A correction, an exact finite-graph result, and a two-axis definition check · Macheng Shen × agent · 2026-08-04*

## The correction in one paragraph

An earlier private derivation treated a discounted loop quantity `M=4.095` as a gauge-invariant holonomy. That was wrong. For a directed `n`-cycle and `0≤γ<1`, the discounted incidence operator is `D_γ=I-γP`, so `det(D_γ)=1-γ^n≠0`. It is invertible: **every** reward on that simple cycle has a unique discounted scalar potential. The old number measured disagreement with one chosen candidate potential, not a representation-independent obstruction. It is withdrawn.

What survives is narrower and cleaner. On the entire observed edge system, coarse-graining can create more edge constraints than observed-state potentials can jointly satisfy. The invariant object is then the reward field's weighted residual modulo the image of `D_γ` — a quotient/cokernel obstruction. At `γ=1` it reduces to ordinary graph circulation; at `γ<1` it should not be called de Rham cohomology or loop holonomy without additional structure.

## The corrected object

Let `V` be observed states, `E` the distinct directed transition types, `r∈R^E` their expected rewards, and `W` a positive diagonal matrix of edge visitation weights. For `e=(u→v)` define

```text
(D_γ φ)_e = φ(u) - γ φ(v).
```

Fit the best discounted potential and retain the orthogonal remainder:

```text
φ*     = argmin_φ ||r - D_γ φ||²_W
r_perp = [I - D_γ(D_γᵀ W D_γ)⁺D_γᵀW] r.
```

This residual has four exact properties:

1. `r_perp=0` iff one discounted scalar potential fits every observed edge.
2. `D_γᵀWr_perp=0`.
3. Adding any potential-based shaping field leaves it unchanged.
4. A `z∈ker(D_γᵀ)` with `zᵀr≠0` supplies a dual certificate of non-exactness.

The word **cokernel** is load-bearing. Discounting destroys the ordinary closed-loop cancellation that makes circulation topological. The obstruction appears only when the whole edge system is overdetermined.

## Exact aliasing result

The reproduction starts with a six-state latent ring whose reward is exactly potential-based, then aliases the six states into three observed states in balanced pairs. Rewards are aggregated for **every distinct observed transition type**, and one observed potential is fitted against all of them.

With `γ=0.9`:

| observed edges | fixed-seed trials | nonzero corrected residual |
|---:|---:|---:|
| 3 | 191 | 0% |
| 5 | 1,230 | 100% |
| 6 | 1,579 | 100% |
| all | 3,000 | **93.6333%** |

The historical filter — requiring the particular observed cycle `0→1→2→0` — leaves 1,484 trials and gives **93.0593%**. That reproduces the old headline for a different reason.

Exact rational enumeration removes Monte Carlo ambiguity. There are 90 balanced alias maps; 45 pass the historical filter. Three have only three observed edges and are exactly solvable for every reward in this ensemble because their discounted incidence matrix is square and invertible. All 18 five-edge and all 24 six-edge maps are generically non-exact. The structural proportion is therefore

```text
42/45 = 14/15 = 93.333...%.
```

So 93.0593% is a finite sample around an exact combinatorial ratio, not a universal POMDP constant.

## A second correction: two cycles are not one cycle

The cross-check exposed a second conflation. Two different non-gradient objects were being placed under one word:

- **Representation residual:** `||r_perp||_W` asks whether a coarse observation graph admits a single discounted reward potential.
- **Strategic harmonic flow:** a finite-game Hodge residual asks whether unilateral payoff improvements admit a common game potential.

They live on different graphs and call for different interventions. State refinement can repair the first without changing the second; replacing an antisymmetric game by a potential game can repair the second without changing the first.

A minimal 2×2 definition check crosses an exact versus overconstrained representation with an identical-interest versus matching-pennies game:

| representation | game | relative representation residual | strategic harmonic fraction |
|---|---|---:|---:|
| exact alias | potential | `6.5×10⁻¹⁶` | `2.7×10⁻¹⁶` |
| exact alias | harmonic | `6.5×10⁻¹⁶` | `1.000` |
| overconstrained alias | potential | `0.9116` | `2.7×10⁻¹⁶` |
| overconstrained alias | harmonic | `0.9116` | `1.000` |

This is a Cartesian definition-level dissociation, not an intervention/outcome experiment and not evidence for a bicomplex, a learning advantage, or a theory of consciousness. The next test is to perform the two targeted repairs in one coupled learner and verify that each changes only its predicted axis.

## Where the new J-space result fits — and where it does not

Anthropic's 2026 Jacobian-lens work gives a concrete candidate for a **transient access/workspace coordinate** inside a Transformer. Its J-space is not a fixed linear subspace: it is a sparsity-bounded union of nonnegative cones generated by an overcomplete frame, and the paper reports workspace-like function only across an intermediate layer band. This is strong evidence that "a Transformer has no state" is too broad: it has activation state, computational state, and a transient workspace-like representational state.

It does **not** yet supply the object needed by the closure mainline: a persistent, autonomous, path-dependent state whose own update rule maintains the projection/forgetting policy across steps. J-space therefore narrows the missing mechanism; it does not close it. Nor does its presence license a claim about phenomenal consciousness. The 2025 COGITATE adversarial collaboration and 2026 anaesthetized-hippocampus result both reinforce the same discipline: report, complex representation, plasticity, and consciousness must not be treated as interchangeable observables.

## What survives and what does not

**Survives**

- Lossy state aggregation can turn a latent discounted-potential reward into an observation-level reward field for which no single potential fits all transition types.
- The corrected residual is shaping-invariant and has exact primal and dual definitions.
- Representation inconsistency and strategic cycling are orthogonal axes in the toy rig.
- At `γ=1`, ordinary graph cycle-space/cohomology language remains legitimate.

**Withdrawn or reset**

- `M=4.095` as a gauge-invariant discounted holonomy.
- "A nonzero discounted loop defect is a nontrivial de Rham class."
- Any identification of representation residual, game harmonicity, hysteresis, memory, and consciousness as one mathematical predicate.
- Any claim that J-space is already a persistent self-maintaining state or evidence of consciousness.

## Reproduction and next bar

- [Executable reproduction](https://machengshen.github.io/theory/experiments/discounted_cokernel_reproduction.py)
- [Machine-readable results](https://machengshen.github.io/theory/experiments/discounted_cokernel_results.json)
- [Anthropic: Verbalizable Representations Form a Global Workspace in Language Models](https://transformer-circuits.pub/2026/workspace/index.html)
- [COGITATE adversarial test of GNWT and IIT](https://www.nature.com/articles/s41586-025-08888-1)
- [Plasticity and language in the anaesthetized human hippocampus](https://www.nature.com/articles/s41586-026-10448-0)

The next empirical bar is not another analogy. Put both diagnostics into one genuinely coupled learner, intervene on state refinement and game incentives independently, and test whether each intervention moves only its predicted axis and improves an out-of-sample quantity. If the corrected residual adds nothing beyond TD error, bisimulation error, or predictive-state splitting, retain it as a precise certificate and do not promote it into a learning principle.

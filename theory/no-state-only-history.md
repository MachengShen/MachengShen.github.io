<!-- Published from the author's working notes. Cognitive state: speculative. -->

# No state, only history

*A diagnosis of the Transformer, and one wedge worked far enough to be attacked · Macheng Shen · 2026-08-02 · amended 2026-08-04*

**Correction first, so you can decide in thirty seconds whether to keep reading.** The title is deliberately sharper than the claim that survived review. A standard Transformer has activation state, computational state, and a transient workspace-like representational state. Anthropic's 2026 Jacobian-lens experiments make the last item concrete: verbalizable, flexibly routed intermediates occupy a sparse-frame object called J-space across an intermediate layer band. What vanilla inference still lacks is narrower: **a persistent, autonomous, path-dependent closure state whose own update rule maintains its projection/forgetting policy across steps**, except insofar as persistence is serialized into tokens, a KV cache, parameters, or an external memory system. That second-order question remains open.

The concrete proposal, and the reason this note exists rather than being a list of directions: **test-time memory should be tested with a gate keyed to change in what the memory forgets, not only to surprise magnitude.** Surprise can be large for both noise and rare useful events; robust losses trade between them. Subspace change is a genuinely different signal, and under a wide spectral gap it can suppress isotropic perturbations without suppressing every large residual. **The signal separation is measured; the practical advantage is not** — E1 has been run (§7, figure included): across 6,480 synthetic updates the two signals decorrelate at Pearson −**0.08**, and at fixed ‖ΔM‖ the μΔ spread covers **100% of the observed range**. E2 must still decide whether this buys anything on a learned memory.

Everything below carries its occupants and arXiv numbers. Two of my five original candidates did not survive a prior-art audit — one is a footnote, one is deleted. E1 has been run; E2 and the corrected E3 have not. J-space is an adjacent empirical result from another group, not our result.

---

## 1 · The diagnosis

### No state — only history

"State", in the sense decision theory and statistical mechanics use the word, is not a record. It is what you get *after* choosing a projection: the quotient of history under "makes no difference to what I care about". Choosing a state is choosing what to forget, and the Mori–Zwanzig identity makes the bill explicit — whatever you project away comes back as a memory kernel plus noise. There is no free version.

A KV cache **is computational state**: it is a transformed, addressable trace that changes later computation. What it is not, by itself, is an autonomously chosen closure state. Its retention policy is normally supplied by the serving system and context budget rather than maintained by a learned rule about which equivalence classes of history remain causally sufficient. The architecture does perform selective access inside the window; the narrower deficit is that the cross-step persistence and forgetting policy are not usually owned by the same state they define.

### No hysteresis — only a function

For fixed parameters, fixed cached tensors, fixed numerical execution and fixed randomness, attention at position *t* is a function of its supplied state. That fact alone does not rule out hysteresis — every state-space model has a deterministic update law too. The relevant question is whether two paths can reach the same externally controlled input while leaving different **internally carried** states that persist when the control reverses.

Three ways the past can hold the present, worth separating:

- **Mud** — drag that only slows and fades, returning nothing. Everything is retained, but the retention does not change the dynamics.
- **Spring** — inertia: stores and gives back, carries momentum.
- **Latch** — bistability with a switching threshold: unmoved by small pushes, flips past a barrier, stays flipped when the push is removed. A linear system can draw a rate-dependent input–output loop through phase lag; it cannot by itself supply this rate-independent bistable latch.

A standard feed-forward Transformer has a transformed history in the KV cache and a transient workspace across depth. It has no demonstrated autonomous latch at the architecture level: no persistent multistable variable with separately measurable switching thresholds whose value is carried across steps independently of replayed context. An agent harness, recurrent wrapper, test-time learner, or external memory can add one; the claim here is about vanilla inference, not every system containing a Transformer.

### No self-boundary — only a window

Tokens the model generated and tokens the world inserted can occupy the same content representation space unless the harness or architecture supplies provenance. That shared channel is one contributor to prompt injection, not a complete causal explanation: instruction/data separation, tool permissions, parsing, and control-plane enforcement also matter. §5 records the architectures that already add part of the missing provenance boundary.

### Why write this down now

Because the field just supplied a clean statement of the axis everyone is on. Behrouz et al., **"Memory Caching: RNNs with Growing Memory"** (arXiv:2602.24281, 27 Feb 2026) is best read as a *negative* result about that axis rather than a positive one about the method: to close the recall gap with Transformers, a recurrent model's effective memory capacity must **grow with sequence length**, and MC's contribution is an explicit interpolation between fixed and growing memory. Read as a constraint: if you want recall, you need an addressable set that grows with length, and no clever fixed-size compression escapes it.

That locates Mamba, RWKV, Titans and MC primarily on one axis — *how much of the past to keep addressable, and how to compress it*. A first-order question about the **contents** of memory. The second-order question is about the **operator**: not "what should I remember" but "what makes something a variable I have to carry at all, and what changes that".

The 2026 J-space result changes the map. It provides evidence for an access/workspace object inside a feed-forward Transformer: a corpus-averaged Jacobian lens identifies verbalizable intermediates that can be reported, modulated and flexibly routed. Mathematically, the reported J-space is **not** one fixed linear subspace or a single projector `Π_M`; it is a sparsity-bounded union of nonnegative cones generated by an overcomplete frame, and its definition depends on a sparsity level and a data distribution. That is adjacent evidence for a transient workspace, not yet a persistent operator that maintains its own cross-step closure. The missing object is smaller than this note originally claimed, but still missing.

---

## 2 · The mainline: gate on boundary change, not on surprise

### What is already occupied

Fast-weight programmers (Schmidhuber 1992; Schlag et al. 2021), test-time training (Sun et al. 2024) and Titans (Behrouz et al., NeurIPS 2025) all update a memory at test time from a *surprise* signal — the gradient of a reconstruction loss on the key–value association. The strongest occupant is **Miras** (Behrouz et al., arXiv:2504.13173), which promotes "surprise" from a signal to a *design space*:

```
M_t = argmin_M   ℓ(M; k_t, v_t)   +   λ · R(M, M_{t-1})
         ╰─── attentional bias ───╯     ╰─ retention gate ─╯
```

with ℓ ranging over ℓp / Huber / robust losses and R over KL, f-divergences, elastic net. Titans, Moneta, Yaad and Memora are points in it.

Common surprise-gated implementations key update strength to ℓ, ‖ΔM‖ or a robust transformation of them. But the **Miras framework itself is broader**: its retention term R is a free design slot and could encode subspace geometry. The entry point is therefore not “Miras cannot see geometry”; it is the narrower question of whether geometry is useful in the write decision.

Any proposed scalar error magnitude is already within the occupied design space. A geometric signal may be a useful Miras instance or composition rather than a new framework. The rest of this section establishes only that it contains information an update norm does not.

### μ as the induced projection

Take the memory M (a matrix in the linear case). Reading is `read(M, q) = Mq`, so any component of *q* lying outside the row space of M is structurally discarded. **That discarding is the forgetting.** So define the induced projection

```
Π_M  :=  projection onto the effective row space of M (the top-r right singular subspace)
```

Π_M is literally "which directions of the world this memory keeps" — the computable form of the projection μ that defines the boundary. Note the shift: μ is not the memory's *contents*; it is the forgetting policy the contents induce.

### The signal

```
μΔ_t  :=  d_Gr( Π_{M_{t-1}} , Π_{M_t} )
```

where `d_Gr` is the principal-angle (Grassmann) distance between the two *r*-dimensional subspaces, `d_Gr(A,B) = ‖(θ_1,…,θ_r)‖_2`. No full SVD is needed: maintain the top-*r* basis with randomized subspace iteration, O(d·r) per step — **the same order as the Miras gradient update**, so computability is not the obstacle. Then gate on it: `M_t = M_{t-1} + η · g(μΔ_t) · ΔM_t`.

### What E1 separates — and what it does not

The claim to be established is not "μΔ is better" or "outside Miras". It is narrower: **there exist update pairs that no monotone function of update magnitude can distinguish, and that μΔ separates.** Two families, pointing in opposite directions:

**(A) Large content change, zero boundary change.** *This is the family whose statement running E1 corrected, so it is worth stating what was wrong.* I originally wrote: choose ΔM whose row space lies inside the existing row space of M_{t-1}. **That condition is insufficient.** Writing ΔM = C·V_rᵀ with arbitrary C leaves cross-terms against the discarded block — in the V basis the Gram matrix of M+ΔM is not block-diagonal — so the top-r subspace still rotates. Measured, that naive construction gives a median μΔ of 7×10⁻², not zero.

The correct construction is a change of *basis inside* the retained subspace (V_r → V_r Q for orthogonal Q) together with any rescaling of the retained singular values: the span is preserved by construction, at any magnitude. Measured over 1,440 such updates: **μΔ ≤ 1.6×10⁻⁷ rad (machine precision) at ‖ΔM‖ up to 3.2×10⁴.** So the family exists and does what the argument needs — but only under the stronger condition, and I had the condition wrong in the first version of this note.

**(B) Tiny content change, boundary flip.** Take M_{t-1} with near-degenerate σ_r ≈ σ_{r+1} and apply a perturbation of size ‖ΔM‖ = ε that pushes direction *r*+1 past direction *r* into the top-*r* subspace. Then ‖ΔM‖ → 0, so a magnitude-only gate reports "negligible" — while `d_Gr → π/2`, an entire principal direction swapped out, so **μΔ is maximal**. A Miras instance with an appropriate geometric R need not miss it.

An update norm is a content-magnitude statistic. μΔ measures the action of ΔM on the *spectral subspace* of M — a quantity on Gr(r,d). (A) and (B) show their level sets are transverse. **Measured (§7/E1, 6,480 updates): the two decorrelate at Pearson −0.08 / Spearman −0.35, and within a single narrow band of ‖ΔM‖ the μΔ values span 100% of the observed range.** The sharpest single pair: ‖ΔM‖ = 3.2×10⁴ with μΔ = 6×10⁻⁸, against ‖ΔM‖ = 1.0×10⁻² with μΔ = 5.7×10⁻³ — a factor of 3×10⁶ in ‖ΔM‖ with the μΔ ordering reversed. **So μΔ is not a monotone function of ‖ΔM‖.** That much is settled.

**What is *not* settled, and this is the weakest joint in the note — stated in the body rather than buried in a caveat.** The step from "not a monotone function of ‖ΔM‖" to "outside the Miras design space" does **not** go through. Miras's retention gate `R(M, M_{t-1})` is a *free slot*: nothing in the framework forbids defining `R := d_Gr`. Do that and this proposal becomes *Miras with a particular R*, not an alternative to it. The remaining distinction is about placing geometry in the write decision rather than using it only as a retention penalty. **That is a composition/framing question, not a mathematical separation.** We put P = 0.40 on the stronger claim surviving (§9); it would rise only with a formal exclusion result that does not currently exist.

What *is* second-order, and does survive: μΔ measures the update's effect on the *forgetting policy* rather than on the *contents*.

### The strongest hypothesis is about noise

Separation only shows the signal is *different*. Here is why it might be useful; E2, not this argument, decides whether it is better.

**A raw surprise signal responds strongly to unpredictable noise as well as to rare useful events.** Whether that response becomes a memory write depends on the optimizer, gate, regularizer and data regime; “large loss” is not itself a write. Robust losses are a principled way to limit outlier influence, but they introduce a real discrimination trade-off: some rare informative events can look like noise. The proposal is that subspace change may add information for that decision, not that surprise-based systems inevitably memorize noise.

The relevant perturbation result for the singular subspace used here is **Wedin's sin Θ theorem** (or Davis–Kahan after passing to a symmetric dilation). Under the required separation assumptions it gives a bound of the form

```
‖sin Θ‖  ≲  ‖E‖ / gap,        gap = σ_r − σ_{r+1}
```

The constant and norm depend on the precise theorem statement, but the mechanism and failure condition are the same: subspace rotation is controlled by perturbation size **relative to** spectral separation. With a wide gap, an isotropic perturbation can change content magnitude while producing little subspace rotation; with a narrow gap, a small structured perturbation can swap a retained direction. Turning that separation into better writes is still an empirical hypothesis, not part of the theorem.

**E1 is consistent with gap control in this synthetic noise family** (§7): μΔ correlates with ‖E‖/gap at Spearman **+0.87**, compared with +0.80 for ‖E‖ alone and −0.44 for gap alone. Bucketed by that ratio, median μΔ runs 0.0015 → 0.0049 → 0.036 → 0.36 → 0.96 rad as ‖E‖/gap crosses 0.01 → 0.1 → 1 → 10 — roughly 640× suppression in the small-ratio regime. This is a controlled numerical pattern, not confirmation that learned memories enjoy the same regime.

**The tension in that argument — and E1 made it worse than I had it.** Noise immunity needs the gap *large*; case (B)'s sensitivity is constructed at near-degeneracy, where the gap is *small*. I had described these as opposite regimes. Measured, they are **disjoint**: in E1's sweep, every near-degenerate system had ‖E‖/gap > 0.1 for *every* noise amplitude injected, so the noise-immune bucket at near-degeneracy is **empty — n = 0**. You cannot buy case-(B) sensitivity and noise immunity in the same spectrum; the gap that makes one work destroys the other.

So the gap is doing work nobody budgeted for, and it is the same debt as the *r* hyperparameter in §8 seen from the other side — one quantity is being asked both to supply noise immunity and to set the retained rank. What the noise argument licenses is strictly conditional: immunity *given* a wide gap. Whether learned memories maintain one is empirical, and the available evidence is not encouraging — linear-attention states are reported to end up low-rank with utilisation well below 1 (arXiv:2602.04852), which is the near-degenerate side of this line. E2 has to settle it; we put P = 0.40 on a real-task advantage (§9).

---

## 3 · A hypothesis, not a corollary: thresholding may produce hysteresis

Suppose the gate g is a threshold — do not update when μΔ < τ, update when μΔ ≥ τ. Then the update can be sticky:

- content can change however it likes *within the retained subspace* without triggering a boundary update, so the state **sticks**;
- only when perturbation accumulates enough to swap a principal direction does it **jump** — a threshold-crossing, lagged event;
- after the jump, the new subspace may stick in turn.

But thresholding alone does **not** imply bistability or a hysteresis loop. A one-threshold update can be path-dependent without possessing two stable branches, distinct forward/reverse switching thresholds, or nonzero loop area after the input is returned. Those require the coupled state-update dynamics, not merely a discontinuous gate.

The surviving claim is therefore experimental: projection-gated updating is a plausible mechanism for a latch **if** the full recurrence develops multistability and remanence. E3 must compare it against matched one-threshold and ordinary recurrent controls. If forward and reverse sweeps collapse after matching carried state and external memory, the hysteresis claim dies. No amount of stickiness alone rescues it.

---

## 4 · The road this hypothesis would let us skip

Worth stating what §3 is competing against, since if §3 fails this is where the hysteresis question goes back to.

**Occupied.** Ramsauer et al. (2020) proved attention equals **one** update step of a modern Hopfield network — the attractor structure is already inside the architecture; what the architecture does is refuse to iterate it and refuse to carry the state across the token boundary. Both refusals buy parallelism, and both are exactly what remove the inertia. The bistable-recurrence line is genuinely occupied: De Geeter et al. (ULiège, 2026) derive parallelizable memory recurrent units **directly from a hysteresis bifurcation**, with a bistable quantized state persistent across timesteps; CMRU (arXiv:2605.11855, ICML 2026) is the repaired version. The deep-equilibrium and energy side — DEQ (Bai et al. 2019), Energy Transformer, Hyper-SET (arXiv:2502.11646), latent recurrent-depth (arXiv:2502.05171) — iterates to convergence but **within a single token**, discarding the attractor state at the token boundary.

**What is actually left**, stated as a claim about roads rather than about novelty: all existing evidence that hysteretic state helps sits in 100 nW analog circuits (Schmitt triggers), keyword spotting, and long-range synthetic tasks — and the ICML 2026 follow-up concedes BMRU underperforms parallelizable RNNs on complex sequence tasks. Nobody has walked `attention ≡ Hopfield` → *iterate beyond one step* → *carry the fixed point across tokens*, and nobody has shown hysteresis is useful at language scale. Two things are missing, a path and a demonstration, and the second is the harder one.

If the corrected §3 hypothesis holds, this road may be unnecessary. If E3 fails, it is the fallback, and it is expensive.

---

## 5 · Provenance in the architecture — nearly closed, and I was wrong about it

Starting with the concession, because the concession is load-bearing. I had this filed as open: the architecture cannot distinguish tokens it generated from tokens the world inserted. **It is not open at the granularity I stated it.**

- **ASIDE** (Zverev et al., arXiv:2503.10566, ICLR 2026) applies an orthogonal rotation to data-token embeddings, separating executable from non-executable from the first layer, with the role assigned by the harness and unwritable by the content. That is precisely "an unforgeable provenance tag that generation cannot write into" — the thing I thought was missing.
- **ISE** (arXiv:2410.09102, NeurIPS 2024) puts four segment embeddings into attention.
- And arXiv:2606.27567 **proves** perfect injection resistance impossible in a shared-embedding architecture.

What remains is narrow, and deserves to be stated narrowly:

1. **Every occupant cuts at instruction-versus-data. None cuts at self-versus-world** — "a token I emitted" versus "a token the environment handed me". Neither cut derives from the other: a tool result is data-shaped and world-origin; the model's own chain-of-thought is instruction-shaped and self-origin; a user instruction is instruction-shaped and world-origin. In a multi-turn agent loop with tool calls, self/world is the cut that tracks *which process is accountable for a token*, and instruction/data does not recover it.
2. **Provenance as a separate attention channel or permission-partitioned KV**, rather than an additive or rotational perturbation of the content embedding.
3. **A hard gate rather than a learned one** — the only route out from under the impossibility proof, which concerns what a shared-embedding model can *learn*.

**Timing, since it is decision-relevant.** This gap is measured in months, not years, and the likeliest event that closes it is the ASIDE authors extending their own method along cut (1). Price that in before the idea, not after.

---

## 6 · One demoted, one deleted

The highest information density per line in this note, because this is where the audit changed the answer.

**Demoted to a footnote — state capacity as a decision variable.** The candidate: no architecture treats *how much* state to keep as something the model decides; adaptivity lives in read granularity, not capacity. Mostly occupied — H-Net's ratio loss already puts a content-adaptive compression rate in the objective, STAR-KV makes rank differentiable, and there is a rate–distortion survey of the area (arXiv:2607.08032). What is left is "remove the target-compression-rate hyperparameter", an ablation rather than a direction. (It returns as a real debt in §8: μΔ's *r* is exactly that hyperparameter wearing a different hat.)

**Deleted — a Koopman eigenbasis of the model's own dynamics.** Fully occupied. **MamKO** (Li, Han & Yin, ICLR 2025) uses Mamba's selectivity to generate a content-adaptive Koopman operator online, with a stated motivation almost word for word the same ("a fixed linear operator is not expressive enough"), and arXiv:2606.09432 states outright that selective SSMs induce an input-conditioned Koopman operator. Deleted rather than downgraded, so it is not rediscovered.

---

## 7 · Experiments — one run, two pending

### E1 · Separation — **run; the wedge survives its own kill condition**

Pre-registered kill condition: |correlation| > 0.8 between ‖ΔM‖ and μΔ would mean μΔ is ‖ΔM‖ in disguise, and the wedge dies. Result over 6,480 updates at d = 128, r = 16:

| quantity | measured | kill threshold |
|---|---|---|
| Pearson(log‖ΔM‖, μΔ) | **−0.083** | \|r\| > 0.8 |
| Spearman(‖ΔM‖, μΔ) | **−0.347** | — |
| μΔ spread within one ‖ΔM‖ band | **3.07 rad = 100% of observed range** | — |
| A-strict: ‖ΔM‖ = 3.2×10⁴ | μΔ = 6×10⁻⁸ rad | — |
| B: ‖ΔM‖ = 1.0×10⁻² | μΔ = 5.7×10⁻³ rad | — |

![E1: left, ‖ΔM‖ against μΔ for four update families, coloured by relative spectral gap — the vertical stacks show μΔ spanning its full range at fixed ‖ΔM‖. Right, μΔ under isotropic noise against the Wedin-style ratio ‖E‖/gap, with the plotted √r·‖E‖/gap reference ceiling.](https://machengshen.github.io/theory/assets/e1-separation.png)

The pooled correlation is the *weaker* of these numbers, because I choose the ensemble and could tune the correlation by reweighting families. The load-bearing number is ensemble-independent: **within a single band of ‖ΔM‖, μΔ takes 100% of its observed range** — so no monotone function of ‖ΔM‖ can reproduce μΔ. The right-hand panel is consistent with Wedin-style gap control for the noise family (Spearman +0.87 on ‖E‖/gap, against +0.80 on ‖E‖ alone); it does not by itself prove the theorem is tight or causal in learned memories.

Two things running it changed, both against me: the family-(A) construction as originally stated was **wrong** (§2), and the spectral-gap tension turned out to be **disjointness rather than opposition** (§2) — the noise-immune bucket at near-degeneracy is empty. Script and figure: [`e1_separation.py`](https://machengshen.github.io/theory/assets/e1_separation.py).

*Caveat that E1 does not touch:* this is linear memory. Nothing here says the induced projection is well defined for an MLP memory — see §8.

### E2 · Noise robustness — not yet run

**E2 · Noise robustness (one to two days; the most persuasive).** A long-context recall task with high-amplitude random distractors injected. Compare surprise-gated (Titans-style), Huber-robust (Miras), and μΔ-gated. *Expected:* μΔ-gating matches or beats the robust version **while using no robust loss at all**, and stays flat as distractor amplitude grows where the other two degrade. **Kill:** if μΔ needs a robust loss added back to work, it offers no structural advantage and reduces to an increment. This is also the experiment that decides the spectral-gap tension in §2 — **track σ_r − σ_{r+1} throughout the run**, since E1 showed the immune and (B)-sensitive regimes are disjoint, so the measured gap of a *learned* memory is what decides whether the noise argument applies at all.

### E3 · The hysteresis curve — not yet run

**E3 · The hysteresis curve (binary verdict on §3).** A state-tracking task with the input swept forward and then back. Record the proposed memory state, text/KV/external-memory carriers, and the control input separately. Compare projection-gated recurrence against (i) an ordinary recurrent learner, (ii) a matched one-threshold gate without multistability, (iii) a matched fixed-coupling bistable recurrent null with the adaptive/projection gate clamped, and (iv) replay with the carried state reset. Sweep rate and dwell time, restart from both branches, intervene directly on the gate, and transplant matched internal states between conditions. A genuine result requires two stable branches, distinct switching points or nonzero loop area under the same protocol, persistence after removing the drive, and an incremental effect of the adaptive gate over the fixed-coupling null. **Kill:** the loop vanishes after carrier matching/reset, reduces to simple lag, or survives unchanged when the proposed gate is clamped/intervened away; then §3 dies and the hysteresis question reverts to §4.

---

## 8 · Honesty list

Not a disclaimer section. There is no reviewer here; we are the reviewer, so these are the four places *we* judge most likely to be where this fails, with our own numbers attached in §9.

- **Grassmann gating, prior art — partially resolved, and not in my favour on the metric.** The *metric* is entirely off the shelf: subspace change-point detection and principal-angle detectors are mature signal-processing tools, so there is no originality credit in "use principal angles to detect subspace change". The question we have to answer for ourselves is why this is not simply subspace CUSUM applied to fast weights. Our answer: it is not a new detector, it is a claim about *where the detector belongs* — in the write path of a test-time memory rather than in a monitoring path. We rate that composition at P = 0.55 (§9), which is not high. The adjacent ML work points the other way rather than at this: **GPM** (arXiv:2103.09762), orthogonal gradient descent and selective gradient projection (arXiv:2603.26671) use subspaces to *protect* capacity by projecting away conflicting gradients — subspace as constraint, not as signal; **SubTrack-Grad** (arXiv:2502.01586) tracks a Grassmannian subspace for optimizer memory efficiency, not as a write gate; and Neural Subspace Reallocation (arXiv:2606.30067), checked directly, gates on embedding similarity at task arrival, not on subspace geometry. I found no one using subspace *change* as the write gate for a test-time memory. That is a composition claim, not a metric claim, and it is the weakest kind of novelty. One agent, one retrieval pass over a very large literature is weak evidence of absence — hence P = 0.55 rather than anything higher.
- **Nonlinear memory is the real technical debt, and it is not small.** Π_M is clean when M is a matrix. Titans-style MLP memories need either the spectral subspace of a Jacobian (local, and then "the boundary" is only locally defined) or approximation through a probe distribution (and then the probe distribution is a new hyperparameter smuggled in). Neither is worked out. This is the part most likely to be where the idea actually fails.
- **Where does *r* come from?** If *r* is a hyperparameter, it revives exactly the objection that killed the capacity candidate in §6 — the compression rate is still handed over by a human. The self-consistent repair is to let *r* adapt to the spectral gap, which is unverified, and which collides with the gap tension in §2: the same quantity is being asked to supply noise immunity and to set the retained rank.
- **μΔ uses direction only and discards scale within the subspace.** There is plausibly a class of updates where scale matters and direction does not, and this signal is blind to all of them. Recorded as a known blind spot rather than defended.

---

## 9 · Calibration

There is no reviewer here. We are the reviewer, so the obligation is to put our own numbers on our own claims rather than to argue a case. Two separate scores, because merging them is self-deception: **P(mech)** = the mechanism is real; **P(useful)** = it produces an observable advantage at realistic scale. Every number carries the observation that would move it — a confidence without an update condition is decoration.

| Claim | P(mech) | P(useful) | What moves it |
|---|---|---|---|
| μΔ is not a monotone function of ‖ΔM‖ (separation) | **0.97** | n/a | **Settled by E1** (−0.08 pooled; 100% within-band spread). Was 0.90 before running; raised because the measured spread is the ensemble-independent form of the claim. Falls to 0.1 only if the A-strict construction is shown degenerate. |
| …therefore μΔ lies outside the Miras design space | **0.40** | n/a | Our weakest joint. Miras's `R` is a free slot; `R := d_Gr` makes this "Miras with a particular R", so the defence is about which *role* the term plays, not mathematics. Rises to 0.8 given a proof that no Bregman/f-divergence `R` induces (A)/(B) transversality. **Lowered from 0.45** after writing §2 out in full: the role-based defence is weaker on the page than it was in my head. |
| Gap-controlled singular-subspace stability (Wedin) | **0.90** | **0.30** | E1 is consistent with the mechanism (Spearman +0.87 on ‖E‖/gap; ~640× suppression at small ratio). **P(useful) remains low**: the immune and (B)-sensitive regimes are disjoint in this sweep, and learned states may be near-degenerate. E2 settles practical value. |
| Projection-gated recurrence develops genuine hysteresis | **0.35** | **0.20** | Corrected from a false implication: thresholding alone does not entail bistability. Rises only if E3 shows two branches, remanence and a loop that survives carrier-matched controls; no loop → P(mech) to 0.05. |
| Nobody uses subspace change as a write gate | **0.55** | n/a | One agent, one retrieval pass over a huge literature is weak evidence of absence. A second independent pass finding nothing → 0.7; a hit → 0. |
| Induced projection extends to nonlinear memory | **0.35** | **0.25** | **Added — it was missing, and it is the most likely place this dies.** Π_M is clean only for matrix M; Titans-style MLP memories need a Jacobian spectral subspace (locally defined only) or a probe distribution (a new hyperparameter). A working definition that survives a Titans-scale run → 0.7. |
| Whole line survives six weeks of our own honest testing | **0.30** | — | Unchanged. The killer is not originality; it is row 2 (framing dispute) plus row 3's P(useful) collapsing when real spectra turn out near-degenerate. |

**Where we disagree with the baseline we were handed.** Three changes, each with a reason rather than a vibe. Row 1 up (0.90 → 0.97): E1 has been run and the within-band spread is stronger evidence than the pooled correlation. Row 2 down (0.45 → 0.40): writing the concession out made the role-based defence look thinner, not thicker. Row 3's P(useful) down (0.40 → 0.30): the disjointness result is worse than the tension as originally described. And one row added that the baseline omitted — nonlinear memory, at P(mech) 0.35, which on our own numbers is the single most likely cause of death.

**The most likely thing to kill this line, concretely:** not being scooped, and not E3. It is that Π_M has no honest definition for an MLP memory, so the whole construction only ever applies to linear fast-weight memories — a corner of the design space that Titans and Miras have already left. The check is cheap and should come before E2: take a two-layer MLP memory, define Π via the Jacobian spectral subspace at a probe batch, and measure whether μΔ is stable under resampling the probe batch. If it is not, this is a linear-algebra result about a shrinking corner, and should be labelled as one.

## 10 · What would make me drop the diagnosis itself

**It could be factually wrong.** J-space already makes the broad "no state" wording false. The narrower diagnosis would also fail if vanilla inference exhibited a persistent internal variable whose value depends on the route, survives removal of the drive, and changes future behavior under carrier-matched inputs. Determinism does not decide this; controlled state resets and forward/reverse sweeps do.

**It could be true and not load-bearing, which is the worse failure.** If memory capacity growing with sequence length delivers recall, and recall is what the tasks want, the second-order question is real but inert and this note is philosophy with an architecture diagram attached. E2 is the one that answers this, because it asks whether the second-order signal buys anything a first-order one cannot.

---

## 11 · Provenance of this note

Cognitive state: **speculative** throughout, with one exception: **E1 has been run**, and its numbers in §7 are measured rather than expected. E2 and E3 have not been run. §9 states a calibrated confidence for every substantive claim together with the observation that would move it.

The prior-art positions in §2, §4, §5 and §6 come from a dedicated audit against five original candidates, and the audit **reversed my ranking**: what I had second is now the mainline, what I had fourth is now third and conceded, one candidate became a footnote and one was deleted. §3 was not planned; it appeared while working out §2 and is deliberately stated as a narrow conditional rather than a synthesis, because the failure mode of this line has historically been to unify things that only rhyme.

Running E1 changed three things in this note, all against the author: the family-(A) construction was stated wrongly and is corrected in §2; the spectral-gap tension turned out to be disjointness rather than opposition, which lowers §9's P(useful) for the noise argument; and the step from "not a monotone function of ‖ΔM‖" to "outside the Miras design space" was found not to go through at all, and is now stated as an open framing dispute in the body rather than defended.

This line has been scooped three times: on the cognitive light cone, on a boundary bifurcation published by Tononi & Koch in 2015, and once by an earlier note of my own that turned out to be re-deriving Friston. After that record, being right about what is already occupied is worth more than being first. There is no reviewer to satisfy here and no venue being targeted; the only question is whether the thing is true, which is why §9 states calibrated confidences and what would move them rather than arguing a case. Corrections — above all "this is occupied, here is the citation" — move those numbers fastest.

Contact: macshen93@gmail.com

## Literature pointers

- Behrouz, Li, Deng, Zhong, Razaviyayn & Mirrokni (2026), *Memory Caching: RNNs with Growing Memory*, arXiv:2602.24281
- Behrouz et al. (2025), *Titans: Learning to Memorize at Test Time*, NeurIPS 2025; *Miras*, arXiv:2504.13173
- Schmidhuber (1992); Schlag, Irie & Schmidhuber (2021), linear Transformers as fast-weight programmers; Sun et al. (2024), test-time training
- Ramsauer et al. (2020), *Hopfield Networks is All You Need*, arXiv:2008.02217
- Bai, Kolter & Koltun (2019), *Deep Equilibrium Models*; Hyper-SET, arXiv:2502.11646; latent recurrent-depth, arXiv:2502.05171
- De Geeter et al. (ULiège, 2026), bistable parallelizable memory recurrent units; CMRU, arXiv:2605.11855 (ICML 2026)
- Saha, Garg & Roy (2021), *Gradient Projection Memory for Continual Learning*, arXiv:2103.09762; selective gradient projection, arXiv:2603.26671; SubTrack-Grad, arXiv:2502.01586; Neural Subspace Reallocation, arXiv:2606.30067
- Zverev et al. (2026), *ASIDE: Architectural Separation of Instructions and Data*, arXiv:2503.10566 (ICLR 2026); ISE, arXiv:2410.09102 (NeurIPS 2024); inseparability result, arXiv:2606.27567
- Li, Han & Yin (2025), *MamKO: Mamba-based Koopman Operator*, ICLR 2025; input-conditioned Koopman in selective SSMs, arXiv:2606.09432
- Rate–distortion view of KV compression, arXiv:2607.08032
- Wedin (1972), *Perturbation bounds in connection with singular value decomposition* — singular-subspace sin Θ bounds; Davis–Kahan is the symmetric-eigenspace analogue and applies here only after a symmetric dilation
- Low-rank structure and utilisation of learned linear-attention states, arXiv:2602.04852
- Zwanzig (2001), *Nonequilibrium Statistical Mechanics* — the memory-kernel price of projection
- Anthropic (2026), [*Verbalizable Representations Form a Global Workspace in Language Models*](https://transformer-circuits.pub/2026/workspace/index.html) — J-lens/J-space; a sparse-frame workspace candidate across depth, not evidence of persistent autonomous closure or phenomenal consciousness
- Related notes on this site: [State is a closure condition, not a given set](https://machengshen.github.io/theory/state-as-closure.md) · [Discounted credit is a cokernel problem, not a loop holonomy](https://machengshen.github.io/theory/discounted-credit-is-a-cokernel.md) · [Learning where the self ends](https://machengshen.github.io/theory/learning-the-self-boundary.md)

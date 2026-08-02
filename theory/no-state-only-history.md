<!-- Published from the author's working notes. Cognitive state: speculative. -->

# No state, only history

*A diagnosis of the Transformer, and one wedge worked far enough to be attacked · Macheng Shen · 2026-08-02*

**The short version, so you can decide in thirty seconds whether to keep reading.** A Transformer has no *state*, only *history*; no *hysteresis*, only a *function*; no *self-boundary*, only a *window*. Every serious alternative on the table — Mamba, RWKV, Titans, Memory Caching — competes on a *first-order* version of the first one: how much of the past to keep addressable and how to compress it. The second-order question is untouched: **how does a state maintain the projection that defines it?**

The concrete claim, and the reason this note exists rather than being a list of directions: **test-time memory should be gated on change in what the memory forgets, not on how surprised it was.** Surprise-gated memory is structurally attracted to noise — noise is by definition the least predictable thing, so it produces the largest write signal, and the thing that should be forgotten hardest gets written hardest. Robust losses patch the symptom by assuming large residuals are usually noise, which is exactly false for the rare events that matter. A gate keyed on subspace change is immune by construction rather than by assumption. **The separation between the two signals is a constructive argument you can check in twenty lines of numpy, and §7/E1 tells you how.**

Everything below carries its occupants and arXiv numbers. Two of my five original candidates did not survive a prior-art audit — one is a footnote, one is deleted. Nothing here has been run. Nothing here is a result.

---

## 1 · The diagnosis

### No state — only history

"State", in the sense decision theory and statistical mechanics use the word, is not a record. It is what you get *after* choosing a projection: the quotient of history under "makes no difference to what I care about". Choosing a state is choosing what to forget, and the Mori–Zwanzig identity makes the bill explicit — whatever you project away comes back as a memory kernel plus noise. There is no free version.

A KV cache is not a state. It is an unprojected record of everything, in which no such choice has been made. The Transformer *declines to choose*. Because something must nevertheless do the forgetting, the job falls to the context window: a knife applied from outside, at a length the architecture had no opinion about, cutting on recency rather than on relevance to the closure condition. The architecture does not forget; it gets truncated.

### No hysteresis — only a function

Attention at position *t* is a pure function of the context. Same context, same output, regardless of the route by which that context was assembled. Nothing latches.

Three ways the past can hold the present, worth separating:

- **Mud** — drag that only slows and fades, returning nothing. Everything is retained, but the retention does not change the dynamics.
- **Spring** — inertia: stores and gives back, carries momentum.
- **Latch** — bistability with a switching threshold: unmoved by small pushes, flips past a barrier, stays flipped when the push is removed. Necessarily nonlinear; linear systems cannot have hysteresis.

A Transformer has mud in the KV cache, and something spring-like in the residual stream within a single forward pass. It has **no latch** — no mechanism by which where the system has been changes where the same input takes it next.

### No self-boundary — only a window

Tokens the model generated and tokens the world inserted occupy the same representation space with no architectural mark separating them. There is a window, and everything inside it is equally the model's own. This is not an aesthetic complaint; it is, fairly directly, the root cause of prompt injection.

### Why write this down now

Because the field just supplied a clean statement of the axis everyone is on. Behrouz et al., **"Memory Caching: RNNs with Growing Memory"** (arXiv:2602.24281, 27 Feb 2026) is best read as a *negative* result about that axis rather than a positive one about the method: to close the recall gap with Transformers, a recurrent model's effective memory capacity must **grow with sequence length**, and MC's contribution is an explicit interpolation between fixed and growing memory. Read as a constraint: if you want recall, you need an addressable set that grows with length, and no clever fixed-size compression escapes it.

That locates Mamba, RWKV, Titans and MC on a single axis — *how much of the past to keep addressable, and how to compress it*. A first-order question about the **contents** of memory. The second-order question is about the **operator**: not "what should I remember" but "what makes something a variable I have to carry at all, and what changes that". Nothing on the current list touches it.

---

## 2 · The mainline: gate on boundary change, not on surprise

### What is already occupied

Fast-weight programmers (Schmidhuber 1992; Schlag et al. 2021), test-time training (Sun et al. 2024) and Titans (Behrouz et al., NeurIPS 2025) all update a memory at test time from a *surprise* signal — the gradient of a reconstruction loss on the key–value association. The strongest occupant is **Miras** (Behrouz et al., arXiv:2504.13173), which promotes "surprise" from a signal to a *design space*:

```
M_t = argmin_M   ℓ(M; k_t, v_t)   +   λ · R(M, M_{t-1})
         ╰─── attentional bias ───╯     ╰─ retention gate ─╯
```

with ℓ ranging over ℓp / Huber / robust losses and R over KL, f-divergences, elastic net. Titans, Moneta, Yaad and Memora are points in it.

The load-bearing observation about that space: **the strength of an update is always determined by the size of ‖ΔM‖ or of ℓ.** Miras can see *how much changed*. It cannot see *what kind of thing changed*. That is the entry point.

This matters because it means the bar for a genuine alternative is high and precise: any proposed signal that is a scalar error magnitude is already a point in Miras, and proposing it is a rename. The rest of this section is an attempt to clear that bar rather than talk around it.

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

### Why it is not a Miras instance — a constructive separation

The claim to be established is not "μΔ is better". It is the sharper and more attackable one: **there exist update pairs that no (attentional bias, retention gate) combination in Miras can distinguish, and that μΔ separates.** Two families, pointing in opposite directions:

**(A) Large content change, zero boundary change.** Choose ΔM whose column space lies entirely *inside* the existing row space of M_{t-1} — a rotation or rescaling within the already-retained subspace. Then ‖ΔM‖ can be made arbitrarily large, so every ℓp / Huber ℓ and every content-metric R reports a large update — while `Π_{M_t} = Π_{M_{t-1}}`, so **μΔ = 0**. What is kept has not changed at all; only what is stored inside it was rewritten.

**(B) Tiny content change, boundary flip.** Take M_{t-1} with near-degenerate σ_r ≈ σ_{r+1} and apply a perturbation of size ‖ΔM‖ = ε that pushes direction *r*+1 past direction *r* into the top-*r* subspace. Then ‖ΔM‖ → 0, so Miras reports "negligible" — while `d_Gr → π/2`, an entire principal direction swapped out, so **μΔ is maximal**. What is kept was rewritten completely.

The Miras signal is a norm of ΔM under a *content* metric (or a monotone function of one). μΔ is the action of ΔM on the *spectral subspace* of M — a quantity on the quotient Gr(r,d). (A) and (B) show their level sets are transverse: there are update pairs with identical ‖ΔM‖ and μΔ spanning its whole range, and vice versa. **Therefore μΔ is not a monotone function of ℓ or R, and does not lie in the Miras design space.** It is second-order: it measures the update's effect on the *forgetting policy*, not on the *contents*.

### The strongest argument is about noise

Separation only shows the signal is *different*. Here is why it should be *better*, and it is an argument from principle rather than from a benchmark.

**Surprise-gated memory is structurally attracted to noise.** Noise is by definition the least predictable thing present, so it maximises ℓ and maximises the gradient: the material that most deserves to be forgotten receives the strongest write. Titans and Miras address this with robust losses that suppress large residuals — but that is a patch on the symptom, and it rests on the statistical assumption that large residuals are *usually* noise. That assumption is precisely wrong for the case anyone actually cares about: the rare event that genuinely matters, which the robust loss suppresses along with the noise.

μΔ does not need the assumption. In high dimension, isotropic noise barely rotates the top-*r* subspace — the effect of a random perturbation on the principal angles decays as *d* grows. So noise gives a large content change and **μΔ ≈ 0**: no write, with no robust loss anywhere in the system. Meanwhile a rare event that actually *changes the structure of the world* swaps a principal direction, so μΔ is large even when its magnitude is small: write. **That is the trade-off one wants, derived from what the quantity measures rather than tuned into it.**

**The honest tension in that argument, which I would rather state than have found.** Noise immunity holds when the spectral gap σ_r − σ_{r+1} is *large*; case (B)'s sensitivity is constructed at near-degeneracy, where the gap is *small*. The two properties therefore live in opposite spectral regimes, and a system whose spectrum sits near degeneracy is one where μΔ is noise-sensitive rather than noise-immune. The gap is doing work that no one has budgeted for, and it is close kin to the *r*-hyperparameter debt in §8. What the noise argument actually licenses is a *conditional* claim — immunity given a gap — and whether real memories maintain that gap is an empirical question E2 has to answer, not a theorem.

---

## 3 · An unexpected corollary: thresholding this gate produces hysteresis

Suppose the gate g is a threshold — do not update when μΔ < τ, update when μΔ ≥ τ. Then:

- content can change however it likes *within the retained subspace* without triggering a boundary update, so the state **sticks**;
- only when perturbation accumulates enough to swap a principal direction does it **jump** — a threshold-crossing, lagged event;
- after the jump, the new subspace sticks in turn — **bistability**.

Stickiness, a threshold, and remanence. That is literally a latch: **the hysteresis §1 says the architecture lacks falls out of projection gating as a by-product, without building it out of multi-step Hopfield iteration.**

**Guarding this claim explicitly, because the failure mode here is a known one.** This is *not* two lines merging into a unified theory, and it should not be read as one. It is a narrow structural conditional — *projection-gated updating implies bistability* — whose entire value is that it makes one road unnecessary, not that it explains anything else. It is falsifiable in the only way that counts: **if E3 produces no hysteresis loop, this dies, and it does not get patched.** A corollary that survives by acquiring epicycles is worth less than no corollary.

---

## 4 · The road this corollary would let us skip

Worth stating what §3 is competing against, since if §3 fails this is where the hysteresis question goes back to.

**Occupied.** Ramsauer et al. (2020) proved attention equals **one** update step of a modern Hopfield network — the attractor structure is already inside the architecture; what the architecture does is refuse to iterate it and refuse to carry the state across the token boundary. Both refusals buy parallelism, and both are exactly what remove the inertia. The bistable-recurrence line is genuinely occupied: De Geeter et al. (ULiège, 2026) derive parallelizable memory recurrent units **directly from a hysteresis bifurcation**, with a bistable quantized state persistent across timesteps; CMRU (arXiv:2605.11855, ICML 2026) is the repaired version. The deep-equilibrium and energy side — DEQ (Bai et al. 2019), Energy Transformer, Hyper-SET (arXiv:2502.11646), latent recurrent-depth (arXiv:2502.05171) — iterates to convergence but **within a single token**, discarding the attractor state at the token boundary.

**What is actually left**, stated as a claim about roads rather than about novelty: all existing evidence that hysteretic state helps sits in 100 nW analog circuits (Schmitt triggers), keyword spotting, and long-range synthetic tasks — and the ICML 2026 follow-up concedes BMRU underperforms parallelizable RNNs on complex sequence tasks. Nobody has walked `attention ≡ Hopfield` → *iterate beyond one step* → *carry the fixed point across tokens*, and nobody has shown hysteresis is useful at language scale. Two things are missing, a path and a demonstration, and the second is the harder one.

If §3 holds, this road is unnecessary. If E3 fails, it is the fallback, and it is expensive.

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

## 7 · Three minimal experiments, each with its kill condition

**E1 · Numerical check of the separation argument (half a day; the foundation).** Construct families (A) and (B) from §2 and scatter ‖ΔM‖ against μΔ. *Expected:* the axes are near-uncorrelated, with samples at fixed ‖ΔM‖ whose μΔ spans the whole range. **Kill:** if the two are strongly correlated, μΔ is ‖ΔM‖ in disguise and the wedge dies on the spot. This is twenty lines of numpy and it is the first thing to run, because it is the cheapest way for the idea to be wrong.

**E2 · Noise robustness (one to two days; the most persuasive).** A long-context recall task with high-amplitude random distractors injected. Compare surprise-gated (Titans-style), Huber-robust (Miras), and μΔ-gated. *Expected:* μΔ-gating matches or beats the robust version **while using no robust loss at all**, and stays flat as distractor amplitude grows where the other two degrade. **Kill:** if μΔ needs a robust loss added back to work, it offers no structural advantage and reduces to an increment. This is also the experiment that decides the spectral-gap tension in §2 — track the gap during the run.

**E3 · The hysteresis curve (binary verdict on §3).** A state-tracking task with the input swept along a path forward and then back. *Expected:* at the same input point, the forward and reverse sweeps occupy different states — a visible loop. **Kill:** no loop, and §3 dies; the hysteresis question reverts to §4, which is expensive.

---

## 8 · Honesty list

Not a disclaimer section. These are the four places a good reviewer should attack first, and I would rather point at them.

- **Grassmann gating, prior art — partially resolved, and not in my favour on the metric.** The *metric* is entirely off the shelf: subspace change-point detection and principal-angle detectors are mature signal-processing tools, so there is no originality credit in "use principal angles to detect subspace change", and a fair reviewer should ask why this is not simply subspace CUSUM applied to fast weights. The adjacent ML work points the other way rather than at this: **GPM** (arXiv:2103.09762), orthogonal gradient descent and selective gradient projection (arXiv:2603.26671) use subspaces to *protect* capacity by projecting away conflicting gradients — subspace as constraint, not as signal; **SubTrack-Grad** (arXiv:2502.01586) tracks a Grassmannian subspace for optimizer memory efficiency, not as a write gate; and Neural Subspace Reallocation (arXiv:2606.30067), checked directly, gates on embedding similarity at task arrival, not on subspace geometry. I found no one using subspace *change* as the write gate for a test-time memory. That is a composition claim, not a metric claim, and it is the weakest kind of novelty — it survives only until someone points at the paper I missed. Pointing at it is the single most useful reply this note could receive.
- **Nonlinear memory is the real technical debt, and it is not small.** Π_M is clean when M is a matrix. Titans-style MLP memories need either the spectral subspace of a Jacobian (local, and then "the boundary" is only locally defined) or approximation through a probe distribution (and then the probe distribution is a new hyperparameter smuggled in). Neither is worked out. This is the part most likely to be where the idea actually fails.
- **Where does *r* come from?** If *r* is a hyperparameter, it revives exactly the objection that killed the capacity candidate in §6 — the compression rate is still handed over by a human. The self-consistent repair is to let *r* adapt to the spectral gap, which is unverified, and which collides with the gap tension in §2: the same quantity is being asked to supply noise immunity and to set the retained rank.
- **μΔ uses direction only and discards scale within the subspace.** There is plausibly a class of updates where scale matters and direction does not, and this signal is blind to all of them. Recorded as a known blind spot rather than defended.

---

## 9 · What would make me drop the diagnosis itself

**It could be factually wrong.** If a model with no latch, no boundary and no chosen projection nonetheless shows behavioural path-dependence not attributable to context *contents* — two runs with token-identical contexts assembled by different routes, behaving differently — then "no hysteresis, only a function" is false as stated. I do not expect it, since a forward pass is deterministic given its context and that is close to definitional. It costs an afternoon, so check it first anyway.

**It could be true and not load-bearing, which is the worse failure.** If memory capacity growing with sequence length delivers recall, and recall is what the tasks want, the second-order question is real but inert and this note is philosophy with an architecture diagram attached. E2 is the one that answers this, because it asks whether the second-order signal buys anything a first-order one cannot.

---

## 10 · Provenance of this note

Cognitive state: **speculative** throughout. No experiment here has been run. Nothing here is a result.

The prior-art positions in §2, §4, §5 and §6 come from a dedicated audit against five original candidates, and the audit **reversed my ranking**: what I had second is now the mainline, what I had fourth is now third and conceded, one candidate became a footnote and one was deleted. §3 was not planned; it appeared while working out §2 and is deliberately stated as a narrow conditional rather than a synthesis, because the failure mode of this line has historically been to unify things that only rhyme.

This line has been scooped three times: on the cognitive light cone, on a boundary bifurcation published by Tononi & Koch in 2015, and once by an earlier note of my own that turned out to be re-deriving Friston. After that record, being right about what is already occupied is worth more than being first. Corrections — above all "this is occupied, here is the citation" — are the most valuable thing anyone can send back.

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
- Zwanzig (2001), *Nonequilibrium Statistical Mechanics* — the memory-kernel price of projection
- Related notes on this site: [State is a closure condition, not a given set](https://machengshen.github.io/theory/state-as-closure.md) · [Learning where the self ends](https://machengshen.github.io/theory/learning-the-self-boundary.md)

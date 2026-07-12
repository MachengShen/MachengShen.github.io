<!-- Published from the author's working notes. Cognitive state: speculative. -->

# Theory note: holography, the Koopman inverse problem, and "optimal forgetting"
*A theory line still under iteration · 2026-07-06 · full context, written for external AI reviewers*

## Context for the reviewer (read this first)

This records one iteration of a personal theory line, taken from the "general learning machine" (GLM) point of view. The line's standing position: **knowledge = a generator (a seed), not a list of facts (fallen leaves); memory = dynamics; forgetting = compression, not deletion**. This iteration starts from a popular-science article about holography and Indra's net, and ends at an open question we believe nobody in the literature has answered head-on.

Research discipline (reviewers, please hold to this frame too):

- Everything below is **exploratory understanding**. It carries no engineering commitment to go build a new architecture on top of it.
- Every assertion is tagged at one of four honesty levels: **[theorem]** (theorem-grade in the source) / **[empirical]** (at the level of an experiment or an explicit statement in a paper) / **[inference]** (our own inference from the literature) / **[rhyme]** (a structural analogy, explicitly *not* claiming that truth transfers).
- We are actively defending against two errors: taking a beautiful analogy for evidence ("a rhyme smuggling in truth"), and the reflex of forcing everything into a single unified framework.

**The most valuable review** would point out which **[inference]** has in fact already been answered head-on in the literature (with the citation), which **[rhyme]** is smuggling in truth, and which **[theorem]** we have applied outside its domain of validity. A specific list of review questions is at the end.

---

## 1. The holography side: how entanglement "grows" geometry (four bricks)

**Brick one: the Ryu–Takayanagi formula (2006) — the dictionary itself.** Bekenstein's "black-hole information ∝ surface area" was originally a special case. RT upgrades it into a general dictionary: the entanglement entropy of any region on the boundary = the area of some minimal surface in the bulk. Pure information on the left, pure geometry on the right, welded together by one equals sign **[theorem, within the AdS/CFT framework]**.

**Brick two: Van Raamsdonk's thought experiment (2010) — entanglement is the glue of spacetime.** Dial down the entanglement between the two halves of the boundary and the bulk geometry stretches thin; take the entanglement to zero and spacetime snaps into two pieces. Connectivity of space = the existence of entanglement; the rigorous version of "relations precede entities" **[empirical-grade argument]**.

**Brick three: the MERA tensor network (Vidal 2007; Swingle 2012 noticed its geometry ≈ AdS) — how a seed unrolls into space.** A tensor network is a "generator pipeline diagram": starting from a small seed, it weaves out a quantum state layer by layer, each layer corresponding to one observation scale (renormalization). Swingle noticed that the shape of the pipeline diagram *itself* is a patch of discrete hyperbolic space, isomorphic-looking to a slice of AdS **[empirical-grade correspondence, not a theorem]**. That is: the "extra dimension" in the bulk = the number of layers the generator unrolls = scale itself. Space is not a stage; it is the trace left by unrolling — the physics version of "the seed gives rise to the manifest" **[rhyme]**.

**Brick four: the HaPPY holographic error-correcting code (Pastawski–Yoshida–Harlow–Preskill 2015) — the theorem-grade version of "the local contains the whole".** The mathematical structure of the holographic dictionary just *is* a quantum error-correcting code: bulk information is redundantly encoded on the boundary, and any sufficiently large boundary fragment can reconstruct the deep bulk; the smaller the fragment, the shallower it can see — what is lost is resolution, not information **[theorem, within the toy model]**. This is the twin structure, on the physics side, of the position that **forgetting = compression, not deletion** **[rhyme]**.

Bonus: the quantum extremal surface / island formula (2019–2020) computed the Page curve at the semiclassical level — black-hole information conservation now has a ledger you can audit **[empirical/theorem-grade progress]**.

**Honest boundaries:** (i) all the rigorous mathematics above lives in an AdS universe, ours is dS (accelerating expansion), and the generalization is an open problem; (ii) MERA ≈ AdS is "strikingly alike", not an isomorphism theorem; (iii) we explicitly do not take up directions of the form "the ancient scriptures already understood holography" — a shared mathematical skeleton ≠ a claim on the source.

## 2. The Koopman inverse problem: when nobody hands you a symmetry, you have to learn the eigenbasis yourself

**Step one: having a symmetry = the eigenbasis is free.** Fourier modes and spherical harmonics are not learned; they are handed to you by symmetry (group theory): a system is invariant under some transformation, and the corresponding eigenbasis arrives automatically. A calendrical system (such as the sixty-term ganzhi cycle) can be viewed as hand-encoding **already known** astronomical periods into a Z/60 harmonic eigenbasis — the same cell of the table: given structure → free basis **[mathematical fact + an inferential characterization]**.

**Step two: Koopman's shift (1931).** For a nonlinear dynamical system, switch to watching how *all observation functions of the state* evolve — that evolution operator is **always linear** (at the price of being infinite-dimensional) **[theorem]**. A Koopman eigenfunction = the "most carefree observable", one that merely gets multiplied by a fixed number at each step; find a set of them and you have found a set of coordinates in which the entangled dynamics decomposes into non-interacting dials turning at constant rates.

**Step three (the crux): the inverse problem.** When the symmetry is not in hand — which is almost always the case in the real world — this eigenbasis can only be learned from trajectory data: DMD → extended DMD → deep Koopman (Lusch–Kutz–Brunton 2018, an autoencoder learning linearizing coordinates end to end) **[empirical]**. The GLM crux, stated: **the core task of a general learning machine = learn, from the stream of experience, the coordinates in which the world's dynamics becomes simple; memory = the seed state in those coordinates; understanding = having found the right eigenbasis** **[position/inference]**.

The honest shortcoming: genuine chaos → the Koopman spectrum becomes continuous → no finite set of dials can simplify it, and no amount of data will yield a clean eigenbasis **[theorem-grade picture, Mezić spectral theory]**. The crux is a question that must be answered, not one that has been answered.

## 3. SSMs (HiPPO/S4/Mamba) ↔ Koopman: surveying the bridge (literature-mining digest)

*This section is the output of a dedicated literature dig: four questions, four answers.*

### Q1. What "given structure" does HiPPO trade for its eigenbasis?

It trades a **forgetting measure** for it: first declare "how much each past moment matters to me" (a measure μ(t)), and the family of orthogonal polynomials under that measure is **uniquely determined** **[theorem]**. The three variants correspond to three forgetting dials: LegT (uniform sliding window → translated Legendre), LagT (exponential decay → Laguerre), LegS (uniform over the whole history → scaled Legendre). The evolution of the projection coefficients compresses into an ODE: dc/dt = Ac + Bf, with A and B derived in closed form, not learned **[theorem]**. *How to Train Your HiPPO* (2022) pushes this all the way: every SSM state can be read as "the projection coefficients of the input history onto some basis", with each basis corresponding to a measure **[empirical]**. S4 merely finds a numerically stable coordinate system for a fixed A (the DPLR decomposition) **[empirical]**.

LegS has a covariance with genuine group-theoretic meaning: under a rescaling of time the output rescales in step (timescale invariance) **[theorem]**. The key difference **[inference]**: the symmetry of the calendrical code comes from **the world** (astronomical periods, given externally), whereas HiPPO's measure comes from **the agent's own choice** (I decide how to forget). Both are "free bases", but the giver is different — and that is the seed of the open question in section 4.

### Q2. What does Mamba's selectivity learn, and what does it not learn?

Facts from the paper **[empirical]**: what is input-dependent is Δ, B, C; **A stays fixed** (diagonal, real). Discretization Ā = exp(ΔA): the effective decay rate at each step = a fixed spectrum × an input-determined time step. Theorem 1: at N=1 it degenerates exactly into the RNN forget gate **[theorem]**.

Translated into the language of measures **[inference]**: Δ is a **knob on the rate of time**. Selectivity does not change the basis — the eigendirections are welded in place from beginning to end — it only tunes "how fast time passes" per token, with B/C determining the read/write directions. **Mamba is the first large-scale success at "learning the measure", not at "learning the basis".**

Theorem-grade corroboration: *The Illusion of State in State-Space Models* (ICML 2024) proves that SSMs with diagonal/commuting transitions are all trapped in the complexity class TC⁰ and cannot even compose permutations; to cross that line, the transition matrix must depend on the input **non-diagonally** **[theorem]**. The dividing line between "learning the measure" and "learning the basis" happens to coincide with this complexity boundary **[inference]**.

### Q3. "The eigenbasis of memory decay" vs "the eigenbasis of world dynamics": what does the gap look like?

- An SSM's basis is **input-generic**: Legendre polynomials do not care what world produced the signal; they are optimal for compressing an *arbitrary* signal under a given forgetting measure. State = the compressed archive of my past.
- Koopman's basis is **system-specific**: the eigenfunctions live on the state space of the world, and the eigenvalues are the natural frequencies of **this particular world**. State = the world's position in its own eigencoordinates.

The two coincide in exactly one case **[inference]**: when the input happens to be generated by purely point-spectrum dynamics, the optimal compression basis = the Koopman modes (this is precisely where DMD gets its legitimacy). In the general case they do not coincide: a memory basis can compress the signal without knowing the causal structure behind it.

How the literature circles it (not one paper names the gap head-on; three characterize it from the side): (i) the Koopman form of a *controlled* system necessarily contains a **bilinear term** (state × input), and the Mamba recursion is purely linear in the hidden state and lacks that term; adding it improves multiplicative-memory tasks by factors of several to a hundred (2026, toy scale) **[empirical, small scale]**; (ii) *Illusion of State*: an SSM's "state", taken as a world-state, is an illusion in the sense of a complexity lower bound **[theorem]**; (iii) MamKO: running it the other way, using the Mamba architecture to generate a time-varying Koopman operator online for control — both ends are under construction, the bridge has not met in the middle **[empirical]**.

### Q4. Continuous spectrum / genuine chaos: the honest boundary

Mezić's spectral picture **[theorem]**: quasiperiodic / attractor-approaching systems have a pure point spectrum, and "learning the eigenbasis" is well-posed; chaotic/mixing systems develop a **continuous spectrum** on the attractor — no countable set of eigenfunctions can span the dynamics, any finite basis is only a truncation, and the prediction horizon is nailed down by the Lyapunov time. The continuous-spectrum part corresponds to nontrivial memory effects (the Mori–Zwanzig memory kernel).

The pragmatic workaround in deep Koopman: parameterize the eigenvalues as functions of the state, λ(x) — a sliding pointer instead of a fixed dial — verified only on small systems **[empirical, small scale]**.

The boundary this puts on the GLM thesis **[inference]**: "you must learn the eigenbasis" is an exact thesis in a pure-point-spectrum world; in a chaotic world it is demoted to "learn a good-enough truncation and own the residual". And the residual comes back precisely in the form of a memory kernel — while an SSM's convolution kernel is by birth a machine for representing memory kernels. This may be the genuinely deep weld between the two towers.

## 4. The open question: should the forgetting measure be determined by the spectrum of the world?

Two degrees of freedom on the table: **μ (the forgetting measure)** = my scoring curve for "how much I care about each past moment" (freely chosen in HiPPO); and **the world's spectrum** = the world's own list of dials (which modes turn how fast, how long correlations drag on). The question: is μ an a priori free choice, or should it be a derived quantity, (near-)uniquely determined by the world's spectrum? Is there an "optimal forgetting theorem"?

**Orienting intuition: this is the dynamical version of a rate-distortion commonplace.** Memory = lossy compression of the past; and lesson one of rate-distortion theory is that the optimal code is fixed by the source statistics + the distortion measure, not by the coder's taste **[theorem]**. Swap the source for the world's dynamics and the distortion for future prediction error, and directionally the answer is "it should be" — what is open is the precise shape of the theorem.

**Four anchors supporting the coupling (hard to soft):**

1. **In the linear special zone this beam already exists = balanced truncation / Hankel theory [theorem]**: given a linear world, "what an N-dimensional memory should optimally remember" is uniquely given by the SVD of the Hankel operator, with closed-form error bounds; the timescales of the optimal memory are determined directly by the world's eigenvalues. Inside a known linear world, "forgetting is determined by the world's spectrum" is a theorem, not a conjecture.
2. **Human empirics = Anderson & Schooler 1991 [empirical]**: the human power-law forgetting curve precisely matches the statistics of how often things recur in the environment — evolution has already tuned μ into a mirror of environmental statistics.
3. **S4's success can be read backwards as a natural experiment [empirical + inference]**: of the three HiPPO variants, the one that won at scale is LegS — exactly the timescale-invariant measure; and natural signals are broadly approximately scale-free (1/f spectra). S4 did not learn μ, but it happened to pick a μ matched to the world's symmetry, and then it won.
4. **The predictive information bottleneck [semi-theorem]**: "compress the past, keep only what carries information about the future" has an analytic solution in the linear-Gaussian case, and its structure follows the world's spectrum exactly; in the general case there are only variational approximations.

**Three obstacles blocking a general theorem:**

1. Chaotic continuous spectra demolish the "world's spectrum" end first. The demoted version of the coupling **[inference, with hard evidence on each half]**: chaotic systems often have metastable structure (slow modes / almost-invariant sets, a spectral gap of the transfer operator), and detail beyond the Lyapunov horizon is worthless → "forget the fast continuous-spectrum part as soon as possible, remember the slow, near-point-spectrum part" — what forgetting should track is **the part of the spectrum that survives**.
2. **The chicken and the egg**: the agent does not know the world's spectrum and has to learn it; learning the spectrum relies on memory; and memory's μ is supposed to be set by the spectrum. The real theorem will not be a static formula but a **fixed point** of this loop — μ and the spectrum learned under μ's support being mutually consistent **[inference]**.
3. **Telos is not only prediction**: balanced truncation balances two Gramians — observability (which past events affect the future) and controllability (which things I can do anything about). μ should be a conspiracy between the world's spectrum and the value function **[inference]**.

**The honest opposition (why it should *not* be fully determined by the world's spectrum):** in a nonstationary / black-swan world, a μ locked onto the current spectrum is the most fragile — a robust μ should keep a fatter tail than the world's correlation decay (insurance) **[inference]**; the value of a rare event lies in "how much it changes the model" (Bayesian surprise), not in its correlational weight, and a purely second-order spectrum would wash it out. The refined proposition: **what μ should track is "the predictable structure of the world + my uncertainty about that structure"; the spectrum is only the linear shadow of the former** **[inference]**.

**Conjectured shape of the theorem [inference]:** given a capacity N, a stationary world-spectrum measure ρ, and a telos (a distortion measure), the distribution of timescales of the optimal forgetting measure μ\* = a rearrangement of ρ's dominant timescales, weighted by the telos; in the linear-Gaussian case it degenerates to balanced truncation; in the online version, μ and the learned spectrum are each other's fixed point, and when uncertainty is high μ automatically fattens its tail. A small falsifiable corollary: within a fixed architecture, tuning μ's decay distribution into a mirror of the autocorrelation decay of the training data should systematically improve long-range tasks (this is a deduction, not an engineering proposal).

**The rhyme (flagged explicitly as a rhyme):** this question is the theorem-ification of "the compression code is a mirror of the world" — an agent's forgetting curve is the reflection of the spectrum of the world it inhabits.

## Specific questions for the reviewer

1. Is the citation of balanced truncation / Hankel theory as the "linear special-zone theorem" appropriate? Is there a stronger or more apt existing result (AAK theory, predictive state representations)?
2. Is the gap between "the memory-decay basis" and "the world-dynamics basis" really unnamed and unaddressed in the literature? Please try hard to find counterexamples (keyword hints: predictive state representations, observable operator models, the intersection of Wiener/Kalman with online basis learning).
3. Has an optimal-forgetting theorem of the form "μ and the learned spectrum are each other's fixed point" already been written down in the predictive-coding / free-energy / meta-learning literature?
4. In the chaotic case, has the demoted coupling (tracking only the metastable / slow modes) already been given a close formalization in the transfer-operator spectral-gap or Mori–Zwanzig reduction literature?
5. In section 3, Q2's characterization of Mamba as "learning the measure, not the basis", and its alignment with the TC⁰ result of *Illusion of State* and with the bilinear term of controlled Koopman — is there a hole in it we have not seen?
6. Where does the analogy on the holography side (sections 1 and 4) as a "same-family inverse problem" risk smuggling in truth?

## Literature

1. HiPPO — Gu, Dao, Ermon, Rudra, Ré 2020, arXiv:2008.07669
2. S4 — Gu, Goel, Ré 2021, arXiv:2111.00396
3. How to Train Your HiPPO — Gu et al. 2022, arXiv:2206.12037
4. Mamba — Gu & Dao 2023, arXiv:2312.00752
5. Deep Koopman — Lusch, Kutz, Brunton 2018, arXiv:1712.09707 (Nature Comm.)
6. Mezić Koopman spectral theory — arXiv:1702.07597; Annu. Rev. Fluid Mech. (annurev-fluid-011212-140652)
7. Bilinear Input Modulation for Mamba: Koopman Bilinear Forms — arXiv:2604.17221
8. The Illusion of State in State-Space Models — Merrill, Petty, Sabharwal, ICML 2024, arXiv:2404.08819
9. MamKO: Mamba-based Koopman operator — OpenReview hNjCVVm0EQ
10. Ryu & Takayanagi 2006 (hep-th/0603001); Van Raamsdonk 2010 (arXiv:1005.3035); Swingle 2012 (arXiv:0905.1317); Pastawski–Yoshida–Harlow–Preskill 2015 (arXiv:1503.06237)
11. Anderson & Schooler 1991, "Reflections of the environment in memory", Psychological Science

<!-- Published from the author's working notes. Cognitive state: speculative. -->

# Learning where the self ends — a research line that broke three of its own four pillars in one day

*Notes from one line of work · 2026-07-27 → 2026-07-28 · **not ratified, not a result***

---

## Part I — For readers who are not in this field

This half has no formulas, no Greek letters and no paper numbers. Every technical word is explained where it first appears. The second half has all the numbers, commands, citations and falsification conditions, and is written for machines and specialists. If you only read Part I, you should still be able to tell someone else what we found.

### The one-paragraph version

We thought we had found the thing that is wrong with how robots are built today: nobody ever lets the robot work out **where it ends and the world begins**. We proposed that a machine should learn that boundary rather than be handed it, and we said the signature of a *real* boundary is that it **sticks** — it is hard to move once it has settled. Over one long day we attacked our own proposal from four directions with our own simulator and our own re-analysis of other people's public data. **Three of the four supporting claims died, and every one of them was killed by our own instruments.** What survived is thin but real: the sticking behaviour *can* appear on its own, without us secretly installing it. What replaced the original claim is a sharper and harder question, which is written at the end.

### 1 · What we believed

Two families of robot learning dominate right now.

- One family learns by **copying**: show the machine thousands of human demonstrations and have it imitate the mapping from what it sees to what it does.
- The other learns by **scoring**: define a number that says how well the robot is doing, and have it search for the behaviour that pushes that number up.

Both are given, for free, an answer to a question nobody asks them out loud: *which parts of the world are me?* An engineer answers it by hand when they decide what counts as a joint, which motors exist, and what the machine's "action" is. The machine never has to ask.

Our claim was that this hand-drawn line is not a detail, it is **the** bottleneck. A robot that could work out its own boundary would do two things that today's robots do badly:

- pick up an unfamiliar tool and treat it as part of its arm, rather than as an object it has memorised;
- lose a motor mid-task and *redraw the line* — "that limb is not mine any more" — instead of needing to be retrained.

### 2 · Why we thought it was more than a slogan

Because in humans the boundary appears to have a very particular mechanical character: it **sticks**.

> **Sticking — the word for it is "hysteresis".** Think of a thermostat set to 26°C. It does not switch on at 26.1 and off at 25.9. It waits until the room reaches 27 to start cooling, and until 25 to stop. The temperature at which it turns on and the temperature at which it turns off are *different*, and the gap between them is what stops it chattering on and off every few seconds. That gap is hysteresis. A system with hysteresis remembers which side it came from.

Everyone has felt the human version. Hold a stick long enough and you start feeling the table through the stick's tip rather than feeling the stick in your palm. Sit on your arm until it goes numb and for a few seconds it is not yours; it is a foreign object in the bed. And there is a classic laboratory illusion — a rubber hand stroked in time with your hidden real hand until you feel the rubber one is yours — which seems to show the boundary snapping across in one piece.

If the boundary really sticks, then a whole class of machine designs is ruled out at a stroke. Any mechanism whose rule is "at each moment, compute the best boundary given what I see right now" **cannot** stick, because recomputing the best answer has no memory of which answer you held a moment ago. That would mean the right implementation is not an optimiser at all but something closer to a physical system with inertia. That was the structural argument, and it is the kind of argument that is cheap to say and expensive to earn.

### 3 · How we went after it

We wrote down, in advance, four ways the idea could die, and then we spent the day trying to trigger them ourselves. In parallel we ran two campaigns:

- **The literature campaign.** Not "has anyone had this idea before" — that question is nearly useless. The question we actually asked was: *when someone says they showed this, what did their experiment support, and where does the support stop?* We hold to a rule that "somebody already did it" is a lead, never a verdict; most papers are written to be published, not to be true, so the honest move is to go and attack their evidence rather than politely stand aside.
- **The simulation campaign.** A simple simulated arm with a detachable tool, a breakable motor, and a wind-blown ball that the arm cannot control — so that "not me" has something to point at.

### 4 · How it fell — in the order it happened

**(a) The "obviously true" fact turned out to be neither obvious nor established.**
Our whole motivation rested on the sentence "in humans this is empirically well established". It is not. Nobody has ever run the decisive experiment — sweeping a knob up and then down and checking whether the boundary flips at different points on the way up and the way down. Worse, there is a specialist re-analysis of the tool-use literature whose conclusion is that the tool effect *may not exist at all* at the strength people assume, with small effect sizes and low statistical power. And the one supportive number we could find — the illusion builds in about twenty seconds and fades in about a minute — is exactly the kind of number we had already declared meaningless, because a perfectly ordinary system with no stickiness gives you that automatically when you switch its input off.

**(b) When we went looking for the decisive data, we found the opposite sign.**
Two independent public datasets, different countries, different manipulations, hundreds of participants between them, both let us ask a weaker but related question: does what you experienced a moment ago pull your next judgement *toward* it (sticking) or *away* from it (contrast)? Both said **away**. That is not a clean refutation — both used end-of-block questionnaires rather than moment-by-moment answers, and one of them measured what people *expected* to feel rather than what they felt — but two independent things pointing the same wrong way is worse for us than one.

**(c) Then, good news: in our own simulator, the sticking appeared without us installing it.**
This matters because the cheap way to get stickiness is to write it into the equations by hand — the equivalent of writing the answer at the bottom of the page. We removed the hand-installed part entirely and left only the mechanism we were actually proposing: *the more a channel is treated as part of me, the better it gets predicted; the better it gets predicted, the more it is trusted; the more it is trusted, the more it is treated as part of me.* A loop that reinforces itself. With that loop and nothing else, the boundary stuck, and it kept sticking even when we slowed the experiment down by a factor of ten thousand — which is the test that separates real stickiness from the fake kind you get just from things taking time to settle. **This is the one pillar still standing.**

**(d) Then the control experiment we had demanded of ourselves went off in our face.**
We had written down: give the identical treatment to something that is obviously *not* part of the robot — the wind-blown ball — and check that it does not stick. Half of that worked: with the ball's own measured numbers, no stickiness. But the other half is fatal. There is one free knob in the equations that nobody's data pins down. Turn that knob up on the ball, and the ball's boundary sticks **exactly as much as the arm's — identical to every digit we printed**. There is a reason, and it is provable rather than accidental: after rescaling, the equations only care about one combined quantity, and the "self" part only decides how far you have to turn the knob, not whether the effect appears at all.

> Said plainly: **stickiness is not a signature of selfhood. It is a generic property of any slowly-changing quantity with a gate on it.** Our arm and a wind-blown ball are indistinguishable on this measure; the only difference is a factor of seven in a knob that is free to be set.

**(e) And the one sharp, specific prediction came out backwards. Twice.**
The prediction was intuitive and it was the reason to prefer our mechanism to a hand-built switch: *hard to adopt, harder to let go* — a tool should be slow to become part of you and slower still to stop being part of you. In the first implementation there was no asymmetry at all (adoption and release took the same time to three decimal places), and the asymmetry we thought we saw turned out to be an artefact of how we had compressed three quantities into one. So we implemented it the other way, the way that ought to produce the asymmetry — and the asymmetry appeared **pointing the wrong way**: letting go was *faster* than adopting, and it took *less* provocation to leave than to join.

The reason is computable, and in hindsight obvious. Our mechanism amplifies the *evidence* about a channel. Evidence is not partisan. Amplifying the evidence about your own hand amplifies the evidence that it is **not** your hand just as much. To get "easy in, hard out" you would have to additionally assume that trust only amplifies evidence in its own favour — and that assumption is another hand-installed thing, which is what we were trying to avoid.

**(f) Finally: even the surviving stickiness needs a dial set to within about two percent.**
For the loop to have two stable settings rather than one, a cost and a benefit inside it have to cancel to a precision of roughly two percent. Our own objective function — the thing that was supposed to make all this emerge naturally — places every single channel *outside* that window, by anywhere from two to four hundred window-widths. So "it can emerge" and "it will emerge" are separated by an argument nobody has made yet.

### 5 · Three mistakes that were ours, not the world's

Worth writing down because each one is a repeatable species of error, not bad luck.

1. **We measured the wrong object and then shipped the misdiagnosis downstream as a premise.** An early run gave a weak result. We diagnosed the cause as "our simulated arm is too weakly coupled to the world", and handed that diagnosis to the next stage as an established fact. It was wrong. The weak reading came from a flaw in the measurement protocol, and the probe we were using ran along a path that never touched the part of the rig we blamed — so it was structurally incapable of detecting the problem we attributed to it. We had read our *probe's* signal-to-noise as the *system's* coupling strength. The general lesson: any time you argue "indicator X tells me about property Y", first check that X is sensitive to Y at all, and if you cannot show it, build a second probe that does not share X's assumptions. (A real coupling flaw *did* exist — it was found by a different probe, and the first indicator was blind to it.)
2. **We believed data availability statements three separate times.** Three published studies advertised "trial-level data available". We downloaded all three and opened every file. All three contained per-participant summary tables with no trial index and no ordering column, which makes the question we wanted to ask structurally uncomputable. Twice more the same shape: a dataset whose parameter column looked exactly like the sweep we needed, with a response column that was blank for every row. **Do not trust the task name or the abstract; open the columns.**
3. **We let "empirically well established" stand as a premise without a citation.** That single unreferenced clause was the load-bearing member under the entire architectural conclusion. Removing it left the conclusion hanging in the air, and it should never have been allowed in.

### 6 · What is left, and the better question underneath

What survived: **stickiness can emerge from a self-reinforcing trust loop without being hand-installed**, and it survives the slow-down test. That is a real, if modest, positive result.

What replaced the original claim is sharper, and we would not have found it without the failures:

> **Stickiness is cheap. Almost any slowly-changing quantity with a gate on it has it. So the question was never "does the boundary stick?" — it is: *what would make a boundary's stickiness be about that boundary itself, rather than being a generic property it happens to share with a ball blowing in the wind?***

That is a harder question, and it is a better one, and it is the one we would work on next. The honest state of this line is: **an open question with most of its original motivation removed, kept alive by one positive simulation result and one reformulated problem.** Nothing here is settled. Nothing here has been ratified.

---
---

## Part II — Technical record

Everything below is measured or cited. Numbers that were not measured are marked as such. Claims are tagged **[measured]** (we ran it), **[cited]** (someone else's published number, verified against the source text), **[inference]** (our synthesis), **[open]** (not done).

Cognitive state of the whole note: **speculative**, with the specific sub-claims graded in §7.

### 0 · Notation

- **μ** — the agent/environment boundary, treated as a first-class learned variable: a partition of all sensorimotor channels into (self, blanket, world). "Blanket" is the screening surface: world influences self only through it.
- **Hysteresis** — bistability of μ under a swept parameter, with distinct up-sweep and down-sweep transition points. The operational criterion adopted here (see §5) is **loop area extrapolated to zero sweep rate remains > 0** (rate-independent), *not* merely "non-zero loop area at some finite sweep rate".
- **Δπ / s** — the precision swing: how much better a channel is predicted when it is inside the boundary versus outside, expressed as the relative swing `s = 1 − ε_in/ε_out`.
- **G** — the loop gain of the precision→assignment→precision feedback, `G = κ·Δπ·(g−c)/(4γτ_π)`.

### 1 · The original proposal

Unified diagnosis: vision-language-action models (VLA) and reinforcement learning (RL) share **one** defect — μ is exogenous.

- VLA: the action space is hand-drawn by an engineer (e.g. a 27-dimensional joint action space with noop padding — a hand-drawn μ frozen into a vocabulary; the whole cross-embodiment codec is a patch for that hand-drawn μ). The model is never required to answer "what am I".
- RL: scalar objective under argmax. Argmax is memoryless ⟹ structurally cannot exhibit hysteresis ⟹ cannot maintain a boundary. A first-order homeostat is a thermostat.

Proposal: learn state / learn μ, not policy.

1. Training signal = **closure violation**, not reward and not action imitation. `z` is a state iff the dynamics close on `z`. Maximise forgetting subject to closure. No rewards, no demonstrations.
2. μ as a first-class variable: partition all channels into (self, blanket, world); criteria = self side internally predictable and controllable, world side reachable only via blanket, partition stable under perturbation.
3. The objective is **second-order**: not "maximise within μ" but "maintain the condition under which μ remains a solution" — self-seal.

Executable specification (loss functions, analytic bistability conditions, MuJoCo rig, measurement protocol with sweep-rate control): `robotics-mu-experiment-spec-20260727` (working document, not published here).

### 2 · Prior art, audited rather than surveyed

Method note: the governing rule for this line is that **"someone already did this" is evidence, not a verdict**. The correct output of a prior-art pass is not "who owns which sentence" but "how far does their evidence actually reach, and where does rhetoric begin". The same blade is then turned on our own claims; a double standard here degrades into claim-defence.

- **Crutchfield causal states / computational mechanics (1989); PSR** — owns "state = minimal sufficient statistic for prediction", i.e. closure itself. **[cited]**
- **Klyubin & Polani, empowerment (2005)** — owns "derive an intrinsic objective from channel structure". **[cited]**
- **Maturana & Varela, autopoiesis** — owns "the self makes its own boundary" (no algorithm). **[cited]**
- **von Foerster (1976) eigenbehavior; Spencer-Brown (1969) re-entry; Kauffman, eigenform** — owns "the self/object is a fixed point of its own operation, and self-reference is generative rather than paradoxical". We add this entry because §0 makes μ a first-class learned variable and §1.3 speaks of maintaining the condition under which μ remains a solution; that *sentence* is theirs, and it predates us by fifty years. **The disanalogy is load-bearing, which is why we do not treat this as pre-emption:** their fixed point lives in a *value/form* domain, is *universally guaranteed* to exist (Kauffman's reflexive-domain fixed point theorem, after Lawvere's diagonal argument), and is *not required to be dynamically stable* — Kauffman states outright that the living process "never goes to the fixed point, is never fully stable", and still calls a non-convergent oscillation an eigenform. Ours lives on a *set-valued* channel-membership object, may fail to exist (hence D0), and must be an attractor with a basin. A universally guaranteed fixed point carries no selection information; our whole question is which of several solutions gets selected, and whether it latches. **[cited]**
  - Scope of that claim, stated honestly: a mechanical keyword sweep of a ~380k-character Kauffman corpus returns **zero** occurrences of hysteresis, bistability, bifurcation, attractor, or differential equation (the single "bifurcate" is ordinary English). *Form Dynamics* (1980) — the one title in this lineage that advertises dynamics — was read page by page: it delivers a brownian (De Morgan) algebra, periodic-sequence algebra, lcm waveform interference, and Scott-style least fixed points, and its bibliography contains **no** dynamical-systems reference. We flag this pre-emptively because it is the paper most likely to be cited against us. **We did not obtain Spencer-Brown's original book, Varela (1975), or von Foerster (1976) in full**; those readings are via Kauffman's formula-level reconstruction, so the negative claim above is scoped to the corpus actually swept, not to the lineage in principle. **[cited, with the stated gap]**
- **Beuria, arXiv:2510.23688** — owns state-dependent coupling gain plus a swept hysteresis loop, but on a *scalar* Vicsek-type order parameter. Recorded here because it also supplies a caveat aimed straight at us: it calls loop area "a protocol-dependent measure of history dependence". Our zero-sweep-rate extrapolation in §5 exists precisely to make the stronger, protocol-**independent** claim; if we did not say so, their caveat would sweep our criterion away with it. **[cited]**
- **Ikegami et al., arXiv:2001.09641** — owns the *object* "the self/non-self partition is determined by controllability", with no dynamical-systems content. Cited to make the division of labour explicit: the object is not ours, the dynamics is what we are claiming. **[cited]**
- **Hoffmann / Lanillos, body-schema learning** — owns "a robot learns its own body from sensorimotor data". **[cited]**
- **Tononi & Koch, Φ-argmax boundary** — owns "the boundary is the optimum of some quantity", **and is precisely the object we must be distinguished from**. **[cited]**
- **Friston FEP / Markov blanket / self-evidencing** — **downgraded on audit 2026-07-28**: it is not a proven result but a framework whose premises have not been shown to be satisfied.
  - Biehl, Pollock & Kanai 2021 (*Entropy* 23(3):293) removes the step "has a blanket ⟹ internal states perform variational inference": *"not generally correct without additional (previously unstated) assumptions"*, with counterexamples. **[cited]**
  - Friston et al. 2021 (*Entropy* 23(8):1076) supplies the missing premises and relaxes *exact* to *approximate* — a repair, not a refutation. **[cited]**
  - Aguilera et al. 2022 (*Physics of Life Reviews* 40:24–50): the blanket + solenoidal conditions are *"only valid for a very narrow space of parameters"* and require *"an absence of perception-action asymmetries that is highly unusual for living systems"*. **[cited]**
  - **This cuts both ways (see §3, D0).** Our §1.2 uses the *same* blanket three-way structure, so if blankets barely exist on systems with perception-action asymmetry, "learn a stable blanket partition" is a question of *solution existence*, not of learning quality.
  - Also: "argmax/FEP is memoryless" — the first half of our own kill-shot — **is already published**: Aguilera et al. 2022 write that the FEP conclusion *"is in general a poor description of the behaviour of a system as it ignores the history of interactions"*. Our increment is only the second half (attaching it to boundary maintenance). **[cited]**
- **Dynamic Markov Blanket Detection, arXiv:2502.21217 (2026-02)** — the nearest thing to this proposal, closer than anything listed above. Full text verified, not abstract-inferred. **[cited]**
  - Its assignments *do* have their own state: one first-order discrete HMM per observational node ("*the labels associated with every observational node i has its own discrete HMM*", §3). ⟹ **we may no longer say "FEP-family blankets have no temporal state"**; that was wrong.
  - But: the implemented version explicitly decouples label transitions from macroscopic state (*"transition probabilities for the assignment variables are a priori independent of the macroscopic latents"*), inference is acausal forward-backward smoothing, and the paper states in Future Directions that *"latent assignment variables quickly diffuse to a uniform stationary distribution in the absence of observed data"* — the textbook definition of monostable, no latch. Zero occurrences of hysteresis / bistability / bifurcation / saddle-node in the full text; no incorporation-vs-release asymmetry experiment.
  - **However**: their *general* form (eq. 21) lets label transition rates depend on the macroscopic blanket variables — exactly the state-dependent coupling loop required for bistability. They assume it away for tractability and list it as future work. **Our wedge lands in the next cell of their roadmap.** Not pre-empted; not a wide window.
  - Open threat, still unanswered: "training signal = closure violation" is highly isomorphic to their surprise/ELBO. If we cannot say why it is **not** ELBO, the proposal is a rename, and that lands before any hysteresis question does. **[open]**
- **The scale narrative (falsifier #4).** Audited separately. Verdict: **the falsifier is not triggered, but only because of an evidence vacuum, not because we won.** **[cited]**
  - Tool use: the scale camp has demonstrated *environment* generalisation (π0.5 across ~104 homes) and *novel object instances* (π0 drops ~13pp). From there to "an unseen tool used as a body extension" there is **no experiment at all**. FORGE (2026-07) still opens with robots that *"fail to transfer the same function to novel"* tools, and buys its 2× with **structure** (keypoint intermediate representation).
  - Damage recovery: the only positive claim is a vendor blog with video — zero success rates, zero trial counts, zero error bars — and its "damage" is made in-distribution by training across "a universe with 100,000 different robots" (amortisation, not re-solving μ), all locomotion, no manipulation. **Cully et al. 2015 (Nature)** — 5 leg damage conditions plus a **14-condition** robot-arm damage matrix, <2 min online adaptation, no self-diagnosis — is still the most rigorous evaluation of this capability eleven years later. That is not progress; that is nobody doing it seriously any more.
  - Disclosure-quality yardstick: Gemini Robotics reports n=20 per task (binomial 95% CI ≈ ±22pp) and is among the better disclosures in the field. On the real-world general benchmark GM-100, 2026 SOTA absolute success is **17.30%** (π0.5 13.02%, GR00T N1.6 7.59%, WALL-OSS 4.05%). **[cited, second-hand for GM-100 composition]**
  - Third-party audit (Epoch AI, *Where Autonomy Works*, 2026): *"Transfer is rarely demonstrated… Unless transfer is explicitly shown, it should not be assumed."*
  - **Reverse audit, recorded because it is against us**: we found **no** paper in which "better structure" beats a 10× larger VLA on the same task and hardware with trial counts and error bars, and **no** empirical performance advantage for any *learned* self-boundary on a real robot. The scale camp has real curves; we have a mechanism hypothesis.
  - ⟹ Strategic inference: the minimal experiment sits in a **public evidence vacuum** — not because it is hard, but because nobody measures it. **The thing worth claiming is the measurement protocol** (incorporation/release asymmetric threshold curves; episode-to-recovery distributions under online actuator failure, with error bars), **not the architecture**. On architecture we lose to scale; on methodology the other side is empty. Corollary obligation: the 100k-morphology domain randomisation is an **amortisation baseline that must be beaten**, so the damage types in any minimal experiment must provably fall outside any pretraining coverage.

### 3 · Simulation: D0 — does a non-trivial blanket partition even exist?

Rig: MuJoCo 3.10, 2–3 DoF arm, detachable tool, breakable actuator, wind-driven ball; N=34 scalar channels (9 proprioceptive, 10 tactile, 12 visual keypoint, 3 action readback). Actions are OU-correlated babbling — no policy learning, so that any hysteresis cannot be attributed to a learned controller. All runs CPU-only, `mujoco==3.10.0`, Python 3.12.

**A · D0-pos (positive control, passed).** Hand-installed double well, zero-sweep-rate extrapolation `A₀ = +0.36 … +0.62` (varies with fit form). Linear negative arm: `|A₀| ≤ 0.008` with the sign flipping across fit forms ⟹ indistinguishable from zero. **[measured]**
- **Criterion correction, self-inflicted**: the negative arm's bootstrap CI also excludes zero, but that only reflects seed noise (SEM ≈ 1e-4) and not the systematic bias from having only 4–7 sweep-rate points with degenerate `β`/`c`. **The correct criterion is not the CI; it is treating 0.008 as the resolution floor and asking by what factor the positive arm exceeds it** (measured 44–75×).
- Analytic anchors reproduced: `h_c = 0.38490`, `x* = ±0.57735`; numerically `h_up = +0.3950`, `h_dn = −0.3939` (2.6% error). Saddle-node scalings `r^{2/3}`, `r^{1/3}` reproduced within 5%. Direct bistable coexistence 1.00/1.00 versus 0.47/0.43 for the negative arm.
- ⟹ **the instrument works**; subsequent negative results can be attributed to the system rather than the ruler.

**B · D0 v1 — a non-trivial blanket partition exists, but the finding is nearly information-free.** **[measured]**
- Yes: a 22 self / 10 blanket / 2 world partition gives peek gain `Δ_peek = −0.0032 ± 0.0016` (6/6 seeds negative) ⟹ adding world channels back does not improve prediction of self ⟹ the hysteresis discussion has an object.
- But: a deliberately leaky calibration partition gives only +0.012, so the dynamic range (0.015) is **smaller than the across-seed std** (0.021). ⟹ This is Aguilera's blade in our rig, but pointing the other way: not "the blanket condition holds only in a narrow parameter region" but "it holds so easily that it selects nothing".
- Degenerate basin dominance: 72 random restarts, **87% collapse to |S| = 1**, and every time to the quietest, best-predicted taxel. Computable diagnosis: the only term pulling controllable channels into self measures ≤0.007 while partitions differ by ~0.3 in closure loss ⟹ the coefficient is off by ~1.5 orders of magnitude; the fix is recalibration, not a different search algorithm.

**C · D0 v2 — this stage falsified our own diagnosis, which is the part most worth keeping.** **[measured]**
- **The v1 diagnosis ("ratio < 1 because the contact rate is too low") — which we issued and then passed downstream as a premise — was wrong.** The low ratio was a *protocol* defect (prediction horizon K=10 too short; ridge grid truncated at its upper bound), not a rig defect: after fixing the protocol **both rigs pass 3** (v2 rig ratio 3.64; the supposedly "bad" v1 rig 3.94). Root cause: the leak calibration probe probes arm→tool leakage, and that path **never passes through the ball**, so it is insensitive to contact rate by construction. **We read the probe's signal-to-noise as the rig's coupling strength.**
- Both things are true and must be recorded separately: the protocol defect (fixed, ratio 3.08 → 3.64) *and* a real rig defect (ball out of reach, y-drift) that `Δ_peek` **cannot see**, confirmed independently by an **estimator-agnostic counterfactual probe**: same action sequence, only the wind seed changed, trajectory divergence **D: 0.045 → 0.203 (4.5×)**.
- Second-layer rig root cause missed by v1: the ball had no restoring force in y and drifted out of plane, so contact rate decayed monotonically with rollout length (3.8% at 2000 steps → 0.56% at 12000). With a y-tether and the ball moved into the arm's occupied region: contact rate **27%** (honestly flagged as above the 5–20% target band), no longer decaying with duration.
- **γ_c auto-calibrated from data**: `γ_c = std(L_clo)/std(controllability term) = 0.0826/0.00374 ≈ 22.1`. The specification default of 1.0 is **wrong on dimensional grounds**.
- Measurement pitfalls found empirically: `actuatorfrc ≡ ctrl` in MuJoCo motor mode (failing to drop it collapses the controllability gain to ≤0.0018 and looks like "actions do nothing"); peek gain is **structurally blind at K=1** (after 20 ms every channel is extrapolable from its own lag); a fixed ridge λ is not comparable across differing column counts, so λ must be selected on validation per predictor.
- Two measurement-theoretic findings that invert the specification's own worries: **(i)** the spec's instruction to give `f⁺` a *smaller* λ manufactures false positives — an overfit `f⁺` yields negative `Δ_peek` and thereby *fakes* blanket satisfaction; **(ii)** contiguous temporal splitting with non-stationary babbling fabricates conclusions (`Δ_peek` reached −0.46 once); interleaved block splitting is mandatory. ⟹ **`Δ_peek` is more sensitive to estimator regularisation and data splitting than to the partition itself; any experiment concluding from it must first run a deliberately leaky calibration partition as a positive control.**

### 4 · Simulation: D1 — is the loop gain criterion reachable?

```
PYTHONPATH=. python scripts/run_d1_gain.py --n-rollouts 6 --steps 12000 --controls-seeds 2
PYTHONPATH=. python scripts/run_d1_featureclass.py --n-rollouts 6
```
v2 rig defaults, D0-v2 protocol (K=20, λ grid to 1e2, interleaved 2:1:1 blocks, ±8σ winsorisation, per-predictor λ selection on validation). `γ_c` auto-calibrated per rollout, mean **28.75** over 6 seeds.

**4.1 What Δπ measures.** The loop is `x_i↑ ⟹ channel i enters z's prediction target ⟹ ε_i↓ ⟹ π_i↑ ⟹ drive amplified`. What sets π is not the label but *whether channel i's history is inside z*. So the measurement is a **same-channel counterfactual**: `ε_i^in` (predict `c_i(t+K)` from features of (S∪B)∪{i}) versus `ε_i^out` (from (S∪B)\{i}). With `π = 1/(1+ε/ε₀)`, the relative swing `s ≡ Δπ/π_max` is monotone in ε₀ with supremum `s = 1 − ε_in/ε_out`, independent of ε₀. All quoted `s` are that supremum — i.e. **the reading most favourable to the theory**. **[measured]**

- The specification's literal reading (π of self channels minus π of world channels) **overestimates by 7×**: 0.233 versus a same-channel 0.0329 ± 0.0037. The difference is entirely *channel identity* (taxels are intrinsically predictable; the ball intrinsically is not), not the loop quantity.

**4.2 Measured values** (6 seeds × 12000 control steps). Test normalised MSE (channels standardised, so ε ≈ 1 means nothing learned):

| | ε_in | ε_out | ε_own |
|---|---|---|---|
| 32 in-boundary channels | 0.500 | 0.551 | 0.534 |
| 2 ball channels | 1.026 | 1.018 | 0.947 |

Relative swing `s = 1 − ε_in/ε_out`, mean ± std over seeds, and under an information-preserving change of representation:

| group | s (cartesian) | s (polar) |
|---|---|---|
| in-boundary mean | **0.0787 ± 0.0071** | 0.0489 |
| proprioception | 0.2291 | 0.0379 |
| tactile (arm) | 0.0016 | 0.0009 |
| tactile (tool) | 0.0086 | 0.0134 |
| keypoints (arm) | 0.0571 | 0.1779 |
| keypoints (tool) | 0.0130 | 0.0257 |
| keypoints (ball, world) | −0.0096 ± 0.0248 | 0.2189 (artefact) |
| action | 0.0104 | 0.0062 |

**Feature-class control — mandatory, else artefacts read as signal.** `q1` shows s = 0.9844 ± 0.0135 in cartesian coordinates, which looks like a rescue. But `q1` is geometrically *determined* by keypoint 1 (`kp1 = 0.25·(cos q1, sin q1)`); the relation is `atan2`, which a linear-plus-quadratic feature class cannot express. Re-express the six keypoints in **polar** coordinates — an invertible transform carrying identical information — and `q1` collapses to **0.0072 ± 0.0171**; `q3` 0.624 → 0.183; `q2` 0.421 → 0.114. The reverse holds too (polar introduces its own artefacts: kp1's radius is constant by construction; ball angle unwrapping drifts, giving ball_x 0.46 ± 0.44). **Representation-invariant reading: max s ≈ 0.18, in-boundary mean ≈ 0.05–0.08, tool-related channels 0.002–0.045.**

Estimator two-way control (2 seeds, substituting a channel): white noise ⟹ s = −1.4e-5 / +1.7e-6 (≈0, the estimator does not manufacture swing); an unrelated AR(1) ρ=0.98 ⟹ s = 0.373 / 0.368 against a theoretical 0.446 (83% recovery). ⟹ the estimator is **attenuating** by ~17%, i.e. conservative with respect to our "the swing is too small" conclusion.

**4.3 The specification's literal H-B form cannot be tristable — as mathematics, not as numerics.** With `τẋ = −γx + κ·π(x)·(g−c)` and `π(x) = π₀ + Δπ·σ(x/τ_π)`, three self-consistent solutions require both `F(0) = κπ₀(g−c)` and `F′(0) = κΔπ(g−c)/(4τ_π) − γ > 0`; with π₀ > 0 these demand opposite signs of `(g−c)` — mutually exclusive. Numerically: κ = 1/10/100 ⟹ G = 0.08/0.82/8.22 with **1/0/0** fixed points, never 3; a regression test pushes κ to 1e4 (G ≈ 1e3) and still gets <3. **[measured]**
Minimal repair (used in D2): gate the *benefit* only, not the cost — `τẋ = −γx + κ(π(x)·g − c)`. Justification is structural, not fitting: the information-bottleneck and blanket-cost terms in the objective are precision-independent by construction, while the controllability gain is the precision-weighted one. G's expression is unchanged; with τ_π = 0.1, κ = 30 this gives G = 2.47 and **3** fixed points.

**4.4 Reachability, and the demotion of the criterion.** Normalising π_max = 1 and writing `A ≡ κg/γ`:

`G = A·s/(4τ_π)`, and branch separation `= A·s = 4τ_π·G`.

| τ_π | s = 0.183 (best self channel) | s = 0.0787 (in-boundary mean) | s = 0.0254 (best tool channel) |
|---|---|---|---|
| 0.05 | A ≥ 1.1 | A ≥ 2.5 | A ≥ 7.9 |
| 0.10 | A ≥ 2.2 | A ≥ 5.1 | A ≥ 15.7 |
| 0.20 | A ≥ 4.4 | A ≥ 10.2 | A ≥ 31.5 |

- **Result 1**: yes, legal parameters give G > 1; nothing has to be pushed to an absurd magnitude. The bottleneck is the ratio of `s` to `τ_π`; κ, γ, (g−c) individually are not bottlenecks since they appear only through `A`.
- **Result 2 (more important)**: `m^S` crossing 0.5 requires `|x| > ln2/2 = 0.347`, i.e. separation ≳ 0.7, i.e. `G ≳ 0.175/τ_π`, which is automatically > 1 for τ_π ≤ 0.175. **"G > 1" and "the boundary actually flips" are nearly the same sentence.** The specification called it the make-or-break criterion; that was an overestimate. It screens out nothing.
- **Result 3 (the real obstruction) — fine-tuning tolerance = s.** The two branches sit at `x*_hi = A(1 − c/g)` and `x*_lo = A(1 − s − c/g)`, so `c/g` must lie in `[1−s, 1]`: **cost must cancel benefit to relative precision s**. Using the repository's own coefficients (γ_c = 28.75 auto-calibrated, β_I = 0.30):

| group | g_i | measured c/g | required window [1−s, 1] | deviation, in window-widths |
|---|---|---|---|---|
| proprioception | 0.0195 | 0.535 | [0.771, 1] | **2.0** (cartesian) / 12.3 (polar) |
| keypoints (arm) | 0.0608 | 0.172 | [0.943, 1] | 14.5 / 4.7 |
| **keypoints (tool)** | 0.0698 | **0.150** | **[0.987, 1]** | **65 / 33** |
| action | 0.0469 | 0.222 | [0.990, 1] | 75 |
| tactile (arm) | 0.0074 | 1.401 | [0.998, 1] | 251 |
| tactile (tool) | 0.0021 | 5.041 | [0.991, 1] | 469 |
| keypoints (ball, world) | 0.0021 | 5.038 | — | 420 (correctly outside) |

**No channel lands inside the window**; the nearest misses by 2 window-widths, and the theory's flagship phenomenon (tool incorporation) misses by 33–469. **Nothing in the objective function pulls c/g toward 1.** ⟹ hysteresis does not fall out of the objective we proposed; it requires a ~2%-precision hand-set ratio that the objective does not supply.

### 5 · Simulation: D2 — emergent hysteresis, and what the controls did to it

```
PYTHONPATH=. python scripts/run_d2_emergent.py --n-seeds 30 --n-boot 1000 \
    --s-self 0.183 --s-ball 0.0254                      # 702 s
PYTHONPATH=. python scripts/run_d2_emergent.py --n-seeds 30 --n-boot 1000 \
    --s-self 0.183 --s-ball 0.0254 --only E_field_gated # 164 s
```

Dynamics with the hand-installed cubic term fully removed (`a = 0`):

    τ_x ẋ = −γx + γ·A·s·(σ(x/τ_π) − ½) + γ·h ,   A = κg/γ,  s = Δπ/π_max

Parameters taken directly from D1 measurements: `s_self = 0.183`, `s_ball = 0.0254`, `τ_π = 0.1`, target `G = 3` ⟹ `A_self = 6.56` (inside the legal region), noise σ = 0.01, τ_x = 1, `h` triangle-swept −1 → +1 → −1.

Four arms: **A** gate on, a = 0 (the claim, G = 3.00); **B** π frozen constant, nothing else changed (negative control, G = 0); **C** the ball with the identical slow variable, identical gate and identical A but its own measured s (G = 0.42); **D** the ball with A raised to 47.2 so that G matches arm A (G = 3.00).

**5.1 Sweep-rate control — the main result.** Loop area `A(r)`, mean over 30 seeds, `r = τ_x/T_sweep` across four decades:

| r | 1e-1 | 3.3e-2 | 1e-2 | 3.3e-3 | 1e-3 | 3.3e-4 | 1e-4 |
|---|---|---|---|---|---|---|---|
| **A** gate on | 0.9571 | 0.6561 | 0.3950 | 0.2974 | 0.2520 | 0.2353 | **0.2268** |
| **B** gate frozen | 0.3831 | 0.1651 | 0.0531 | 0.0181 | 0.0054 | 0.0018 | **0.0006** |
| **C** ball, measured s | 0.4512 | 0.1953 | 0.0624 | 0.0211 | 0.0064 | 0.0021 | **0.0007** |
| **D** ball, matched G | 0.9571 | 0.6561 | 0.3950 | 0.2974 | 0.2520 | 0.2353 | **0.2268** |

Zero-rate extrapolation `A(r) = A₀ + c·r^β` (β profile grid, 30-seed bootstrap):

| arm | A₀ (β free) | β | A₀ (β = 1) | multiple of the 0.008 resolution floor | verdict |
|---|---|---|---|---|---|
| **A** | **+0.1932** | 0.54 | **+0.2771** | **24 – 35×** | true bistability |
| B | −0.0044 | 0.79 | +0.0081 | ≤1.0× | relaxation lag only |
| C | −0.0052 | 0.79 | +0.0097 | ≤1.2× | relaxation lag only |
| **D** | **+0.1932** | 0.54 | **+0.2771** | **24 – 35×** | true bistability |

Arm B's two `A₀` values are **digit-for-digit identical** to the D0-pos linear arm, because `gate_const=True` mathematically degenerates to it (asserted by regression test) — which also re-confirms the 0.008 resolution floor in this round. Thresholds at the slowest rate: arm A `h_up = +0.2674`, `h_dn = −0.2099` ⟹ Δ = +0.477 (a real loop); arm B `h_up = +0.3359`, `h_dn = +0.3583` ⟹ Δ = −0.022 (the two cross; there is no loop).

**5.2 Direct bistability test** (stronger than loop area): `h` fixed at 0, 30 seeds per branch, `T_hold = 1000 τ_x`:

| arm | lower-branch stay rate | upper | branch separation |
|---|---|---|---|
| **A** | **1.00** | **1.00** | **1.193** |
| B | 0.47 | 0.43 | 0.0012 |
| C | 0.43 | 0.40 | 0.0021 |
| **D** | **1.00** | **1.00** | **1.193** |

B/C's 0.4x is not "retained half the time"; both branches have collapsed to the same point and `sign(x_end)` is decided by noise (the separation of 0.001–0.002 is the substantive number). **[measured]**

**5.3 ⭐ The specificity control — half of the narrative removed.**
- **Arm C (the honest half)**: same slow variable, same gate, same drive/leak ratio, only the precision swing replaced by the ball's *measured* value ⟹ G falls to 0.42, `A₀` returns to the resolution floor, coexistence 0.43/0.40 fails. **No hysteresis.** ✅
- **Arm D (the fatal half)**: raise only the ball's A from 6.56 to 47.2 so that G = 3 ⟹ **every hysteresis number is digit-for-digit identical to arm A** (A₀ = +0.1932, separation 1.193, τ ratio 0.806).

This is not coincidence but analytically predictable: after normalisation the ODE depends **only on (G, τ_π)**, with drive amplitude `A·s = 4τ_π G`. **s decides how large A must be, not whether hysteresis occurs.**

> ⟹ **Hysteresis is a generic property of a gated slow variable; it is not a signature of selfhood.** On this rig, "the hysteresis of a self-boundary" and "the hysteresis of any similarly gated slow variable" are dynamically indistinguishable; the only distinction is a 7× magnitude difference in a quantity that a free parameter absorbs. This does **not** falsify H-B (arm A really does give rate-independent hysteresis at a = 0), but it cancels the inference "hysteresis ⟹ this is a self-boundary". Restoring specificity requires pinning A from data too — which lands straight back on §4.4 Result 3.

**5.4 The τ_off/τ_on asymmetry prediction — falsified, twice.** Holding `h = ±1.5·|h_up|` outside threshold and stepping from the opposite branch, measuring the time to complete (1 − 1/e). Both observables are reported because the 1-D reduction `m^S(x) = e^x/(e^x + e^{−|x|} + e^{−x})` is **itself asymmetric** under `x → −x` (m = 1/3 rather than 1/2 at x = 0), so it manufactures τ_off ≠ τ_on even from perfectly symmetric dynamics:

| arm | τ_on (m^S) | τ_off (m^S) | ratio (m^S) | τ_on (x) | τ_off (x) | **ratio (x)** |
|---|---|---|---|---|---|---|
| **A** gate on | 4.24±0.11 | 3.41±0.09 | 0.806 | 4.00±0.09 | 4.03±0.10 | **1.008** |
| B gate frozen | 1.50±0.03 | 0.81±0.02 | 0.537 | 1.06±0.05 | 1.04±0.05 | 0.981 |
| C ball | 1.81±0.04 | 1.00±0.00 | 0.554 | 1.29±0.03 | 1.28±0.04 | 0.992 |

The prediction was `τ_off > τ_on` (ratio > 1), returning to 1 when π is made constant. Measured: on the slow variable the ratio is **1.008** — no asymmetry at all; on `m^S` it is 0.806 (**below** 1, i.e. release *faster* than adoption), and constant-π gives 0.537, i.e. *further* from 1, so the predicted direction of that control is also wrong. Root cause, computable: the drift `F(x) = −γx + γAs(σ(x/τ_π) − ½) + γh` is strictly odd under `(x,h) → (−x,−h)`, so on/off are symmetric by construction. **The precision gate does not by itself produce a time-constant asymmetry.**

**Arm E — gate multiplying the whole drive** (the mechanism the specification actually wanted): `τẋ = −γx + γA[π(x)(1 + w·h) − π(0)]`, w = 0.4, otherwise as arm A. Cost remains ungated, else §4.3 forbids tristability.

| quantity | E | vs A |
|---|---|---|
| A(r), r = 1e-1 → 1e-4 | 1.0049 → **0.0995** | 0.9571 → 0.2268 |
| A₀ (β free = 0.75) | **+0.0916** [CI 0.0915, 0.0918] | +0.1932 |
| A₀ (β = 1) | **+0.1289** | +0.2771 |
| multiple of resolution floor | **11 – 16×** | 24 – 35× |
| coexistence / separation | 1.00 / 1.00, 1.193 | 1.00 / 1.00, 1.193 |
| thresholds (slowest rate) | `h_up = +0.1245`, `h_dn = −0.0819` | +0.2674 / −0.2099 |
| **τ_on / τ_off (x)** | 3.91 / 3.10 ⟹ **0.794** | 4.00 / 4.03 ⟹ 1.008 |

The asymmetry finally appears (0.794 ≠ 1.008) **and points the wrong way**: release is *faster* than adoption, and the threshold to leave (−0.0819) is *lower* in magnitude than the threshold to join (+0.1245). Computable reason: `G(h) = G₀(1 + w·h)`; for h > 0 the loop gain is high, the system is near its fold, critical slowing ⟹ slow adoption; for h < 0 the gain is low, the system is more linear ⟹ fast release. The original reasoning ("already inside self ⟹ high precision ⟹ contrary evidence must be larger to expel it") silently assumed **precision amplifies only supporting evidence**, which is false in any implementation where π multiplies the drive. To obtain "easy in, hard out" one must additionally assume an asymmetric evidence weighting — which is another hand-installed component.

**5.5 Not closed this round.** **[open]** The short-training encoder was not run (D1 used a ridge-regression proxy for ε, so Δπ still carries feature-class dependence — the largest open item); D2 ran on the 1-D reduced ODE, not the 34-channel rig; the grip-stiffness force-displacement calibration was never done, so the specification's primary parameter axis was never swept (D2 swept an abstract field); separatrix / minimum escape perturbation asymmetry untested; Wilcoxon paired test and retest σ₀ not done; D3–D5, the pyDMBD comparison baseline, and baselines a1/a2/b/c/d not run. 25 pytest tests pass.

### 6 · Human side: two campaigns, both unfavourable

**6.1 Why the decisive experiment does not exist.** Not because nobody thought of it: every parameterised rubber-hand study uses randomised or pseudo-randomised order, because the default hygiene of psychophysics treats sequence effects as **contamination rather than signal**. The paradigm was designed to erase the quantity we need. **[inference from method sections]**

**6.2 An existing order-dependence measurement, with the sign against us.** Zhang, Ma & Hommel 2015 (*Frontiers in Psychology* 6:1659, N=34): the same mid-distance condition preceded by near versus by far — **far→mid gives significantly higher ownership** (M = 3.768 vs 3.056, F(1,33) = 39.82, η²p = 0.547). Hysteresis predicts the opposite (near→mid higher). Under the sign convention of Liaci & Kornmeier 2018 (positive = hysteresis/priming, negative = adaptation) this is **negative, i.e. the adaptation side**. Not a clean refutation (7-point questionnaire; the parameter is distance not synchrony; only two steps) but it is the published data nearest to the bit we want, and it is not on our side. **[cited]**

**6.3 A larger replication we dug out of a candidate list, run and reported.** OSF `bsfwu` (Tsuji & Imaizumi, rubber-hand order effects, in the Lush 2020 line), **N = 185** with a `CondOrder` column (Syn1st / Asyn1st) — the synchrony version of the same path manipulation, five times the sample. **[measured, by us, on their public data]**
- Same Async condition: Syn1st group M = −0.455 versus Asyn1st group M = +0.436, difference **−0.891**, 95% CI [−1.232, −0.550], t(183) = −5.16, **p = 6.7e-7**, Hedges d = −0.756; Order × Condition F(1,183) = 19.17, p = 2.0e-5, η²p = 0.095. Experiencing the strong condition first *lowers* subsequent ratings of the weak condition = adaptation/contrast, same direction as 6.2.
- **Three down-weightings we found ourselves, by reading their questionnaire text**: (a) the dependent variable is not experienced ownership but **expectation** — participants watched a 32 s video and answered what they would *expect* to feel, having never undergone the procedure — so this is an order effect on beliefs about ownership, almost certainly containing judgemental anchoring; (b) control items show a same-direction significant effect (−0.313, p = 0.0435), so demand characteristics are real — **but not everything**: Order × Scale F(1,183) = 22.42, p = 4.4e-6, η²p = 0.109, with the effect on illusion items ~**2.8×** that on control items, so a genuine component exists but is contaminated by same-direction bias and cannot be cleanly separated in this dataset; (c) N is actually 185, not 184.

**6.4 A synchrony-side pipeline dry run — not embodiment evidence, but one technical fact that decides success or failure.** **[measured]**
- **The permutation null distribution is not centred at 0; it is centred at +0.191.** Mechanism identified (a `soa²` term plus block-level response-rate heterogeneity; 99.2% of lag-1 pairs fall within a block, and between-block response-rate differences survive the shuffle). ⟹ **testing against 0 reads the sign backwards**: a t-test says "+0.048, p = 0.47, no effect", while against the correct null the same data is significantly *negative*. Two independent null models (within-block reshuffle, cyclic shift of the history sequence) give the same-sign null centre (+0.191 / +0.158). **Discipline: on any ownership dataset, first run the null-bias diagnostic to locate the null centre, then talk about significance.**
- Real numbers split but explained: dataset `hev9z` (simultaneity judgement, 26k trials) shows the point of subjective simultaneity dragged **+16.1 ms** [12.3, 19.9] by the previous trial = adaptation side; `4ukzx` shows choice repetition **+0.447** = priming side. The cause is not instability but that `4ukzx` is a **TOJ-type monotone task** (β_soa = +7.6, β_soa² = −0.16), a different family from the peaked SJ curve.
- Both datasets: lag-1/lag-2 significant, **lag-3 at zero** ⟹ a 1–2 trial tail, **no multi-trial latch** (weak evidence, not embodiment).
- **Hard design constraint for any future self-built experiment — the most transferable item of the round**: *if the sign of the manipulated parameter maps directly onto the semantics of the binary response (as "who came first" does in TOJ), hysteresis and adaptation are mathematically indistinguishable.* ⟹ a trial-level ownership DV **must stay "yes/no"** and must never be phrased as "which hand feels more like mine". Also: if the experiment is a monotone sweep, a freely-reshuffling permutation null is **illegitimate** and must be replaced by within-sweep-direction order-preserving permutation.

**6.5 Data hunting: what does not exist, and one mistake repeated three times.** **[measured]**
- Trial-level ownership data: OSF (16 keyword sets) + Zenodo (10 sets) + OpenNeuro (full census of 1831 datasets) — **zero hits**.
- Three advertised "available" datasets opened by hand: eLife 11:e77221 (Chancel/Ehrsson/Ma 2022) fig1 source data is a **participant × condition count matrix** (S1, N0_−500 = 0 "yes" out of 12 trials; 17 rows × 22 columns), fig2/fig3 are model parameter estimates; OSF `spkvu` (Lanfranco 2024), enumerated recursively via API, contains **exactly three files** (`bias.csv` 2578 B, `dprime.csv` 2432 B, `readme.rtf`), all participant × condition aggregates. **No trial index, no order column in any of them** ⟹ the question is structurally uncomputable there. (Verification: `python3 osf_list.py spkvu 3`; `openpyxl.load_workbook` printing every sheet; 2026-07-28.)
- **Do not trust the task name; open the columns.** `ds001785` has a `stimamp` column that is strictly monotone up 0.10 → 1.94 and down 2.50 → 2.30 — the first genuine up/down sweep found in four rounds, and a name-level read would have declared victory; the response column is `n/a` for all 93 rows. Similarly `ds003922`'s responses are not in the BIDS events at all but under `sourcedata/`.
- **A correction to our own search agent's over-conclusion**: it concluded that trial-level structure does not exist *at the paradigm level* ("the classic DV is an end-of-block questionnaire"). That is **wrong for the Ehrsson line** — the eLife 77221 `RHIdetect` table *is* a trial-level binary ownership judgement, 12 trials per condition (the counts 0–12 are the evidence). The paradigm exists and is mature; the raw logs are simply never uploaded. ⟹ the correct next step is not "build our own paradigm" but **request the logs from the authors** — currently the highest value-per-effort move available, and one that requires a named human request.
- New target satisfying all four criteria: OSF `4dzrg` — visuotactile TOJ × observed human hand, 40 participants × 840 trials ≈ 33,600, columns `subNum blk cond trialNum vis_tac_first SOA resp corr RT` (extracted by range-reading the zip tail; the 384 MB archive was not downloaded). OpenNeuro `ds004561` (Veillette/Lopes/Nusbaum, CC0, EEG, 23 participants) is the only public **bodily-self** dataset with trial-level binary judgement, parameter and order all present (`onset duration trial_type trial intensity latency rt pressed_first agency`, 250 trials/participant) — **but it measures agency, not ownership**.
- Not tested empirically: NEMAR's own interface (zero hits is an inference, not a measurement), Dryad, figshare, GitHub. Not searched: numb-limb detachment thresholds; **full-body / avatar illusions**, which are more virtualised and may hide existing sweep data — the highest value-per-effort direction for a next round.

**6.6 Methodological templates worth copying, and one more result against us.** **[cited]**
- T1 — Martin, Kösem & van Wassenhove 2015 (*PLoS ONE* 10(3):e0119365), hysteresis in audiovisual synchrony: **the same blade has already been applied to the synchrony parameter**; only the modality (audiovisual → visuotactile) and the response ("is this my hand?") need changing. It did not vary sweep rate and did not establish rate independence.
- T2 — Liaci & Kornmeier 2018: the operational definition `hd = inflection(ascending) − inflection(descending)`, plus a third randomised-sequence baseline arm.
- T3 — stereo vision / binocular rivalry: the only literature with **multiple sweep rates** built in, i.e. the one that can execute our zero-sweep-rate extrapolation criterion.
- **Against us**: Schwiedrzik et al. 2014 (*Cerebral Cortex*) show hysteresis and adaptation are **independent, additive, and anatomically separable** components ⟹ **measuring zero net hysteresis does not mean there is no latch** (the two components can cancel). This must go into any pre-registration, or we can neither falsify ourselves with a null result nor use it as an alibi.
- Cost estimate (our own, not from any paper) for a VR-based self-built experiment: equipment plus participants ¥5k–8k, 3–5 developer-days, N = 24, 2–3 weeks of collection. **The real barrier is participant recruitment and ethics affiliation, not equipment.** VR is not the cheap option, it is the *only* option that meets the criteria: in a physical rubber-hand setup the delay is produced by the experimenter's hand, so step size cannot be made fine and sweep rate cannot be controlled, making multi-rate extrapolation near-impossible; in VR the delay is pure software. Visuomotor correlation alone induces the illusion, so no haptic hardware is needed.
- **Current human-side balance**: two independent manipulation dimensions (spatial distance / temporal synchrony), two different samples (N = 34 / N = 185), two kinds of measurement (experienced / expected) — **all on the adaptation side, none in the hysteresis direction**. That convergence is worth more than any single result. But both are block-level questionnaires and in principle cannot separate "hysteresis" from "single-shot contrast anchoring", so the genuinely discriminative data (trial-level + varied sweep rate + experienced measure) is **still missing**. **This line is neither supported nor genuinely falsified on the human side; the two usable data points both point the wrong way.**
- Decision update: **do not fund a self-built VR study yet** (the prior has worsened, so the expected value of a several-thousand-yuan experiment has dropped). Priority order: (1) request trial-level logs from the Ehrsson line — the only existing source of discriminative data, requiring a named request; (2) continue the simulation side, which does not depend on the biological premise.

### 7 · Ledger: the four falsifiers and where each stands

| # | Falsifier | Status |
|---|---|---|
| 1 | **Asymmetric threshold for tool incorporation** (slow in, slower out). Tightened mid-flight: a non-zero loop is not enough; loop area extrapolated to **zero sweep rate** must stay > 0, else a self-generated rate-dependent loop is mistaken for success. | **Partly passed, partly falsified.** Rate-independent hysteresis at a = 0: A₀ = +0.19…+0.28, 24–35× the resolution floor, coexistence 1.00/1.00 ⟹ **passed**. The asymmetry direction: **falsified twice** (§5.4). Self-specificity: **falsified** (§5.3). |
| 2 | **Damage test**: disable an actuator mid-run; μ should re-solve to a different closed partition within N episodes without policy retraining, and significantly faster than a fine-tuned VLA baseline. | **Not run.** |
| 3 | **Sensory-substitution transfer**: train μ with vision, swap to a tactile array encoding; if behaviour does not converge to the visually-reachable set, μ is modality-bound and the theory over-claims. | **Not run.** |
| 4 | **Bitter lesson**: if a plain VLA scaled 10× matches on tool use and damage recovery, μ was never the bottleneck. | **Not triggered — but because of an evidence vacuum, not because we won** (§2). Burden of proof remains on us. |

**Additional falsifiers added during the audit**, both of which fired:

- **D0** (added because our own attack on the FEP literature applies to us): first show that a non-trivial blanket-satisfying partition exists on the simulated arm. **Passed, but nearly information-free** (§3B).
- **D0′** (human side): a self-built up/down synchrony sweep. **Deferred** — the prior worsened enough (§6) that funding it is no longer justified.

### 8 · Current status of the claim

Original wedge: *μ has hysteresis, driven by second-order self-maintenance, with incorporation slow and release slower.*

| component | status |
|---|---|
| hysteresis emerges without a hand-installed non-linearity | ✅ **survives** |
| the hysteresis is specific to the self-boundary | ❌ generic property of gated slow variables |
| release is slower than incorporation | ❌ reversed, in both implementations |
| it falls out of the proposed objective without fine-tuning | ❌ requires a ~2% hand-set ratio |

Three of four pillars down, **all of them felled by our own instruments** — which is what the process is for.

**The reformulated question**, which is the actual output of this line: hysteresis is cheap; any gated slow variable has it. **What makes a boundary's hysteresis be *about that boundary*?** Restoring specificity requires pinning the free amplitude `A` from data (e.g. locking it to what the objective itself yields), which is the same problem as §4.4 Result 3, and neither is solved.

Two earlier threats also remain unanswered: whether "closure violation" is genuinely distinct from ELBO (§2), and the concession that raw pixels cannot serve as channels — μ is a partition over channels, so referents must have stable identity, which is this line's largest acknowledged cheat and is explicitly accounted for rather than hidden.

**Not ratified. Not a result. Published because the negative half is the part with evidentiary value.**

### 9 · References

- Aguilera, Millidge, Tschantz & Buckley (2022). How particular is the physics of the free energy principle? *Physics of Life Reviews* 40:24–50.
- Biehl, Pollock & Kanai (2021). A technical critique of some parts of the free energy principle. *Entropy* 23(3):293.
- Chancel, Ehrsson & Ma (2022). Uncertainty-based inference of a common cause for body ownership. *eLife* 11:e77221.
- Crutchfield & Young (1989); Shalizi & Crutchfield (2001) — causal states / computational mechanics.
- Cully, Clune, Tarapore & Mouret (2015). Robots that can adapt like animals. *Nature* 521:503–507.
- Friston, Da Costa & Parr (2021). Some interesting observations on the free energy principle. *Entropy* 23(8):1076.
- Holmes (2012). Does tool use extend peripersonal space? *Experimental Brain Research* 218:273–282.
- Klyubin, Polani & Nehaniv (2005) — empowerment.
- Liaci & Kornmeier (2018) — hysteresis and adaptation in perceptual sequences.
- Martin, Kösem & van Wassenhove (2015). Hysteresis in audiovisual synchrony perception. *PLoS ONE* 10(3):e0119365.
- Maturana & Varela (1980) — autopoiesis.
- Schwiedrzik, Ruff, Lazar, Leitner, Singer & Melloni (2014). Untangling perceptual memory: hysteresis and adaptation map into separate cortical networks. *Cerebral Cortex* 24(5):1152–1164.
- Tononi & Koch (2015) — consciousness and the boundary of a complex.
- Zhang, Ma & Hommel (2015). The metacontrol hypothesis / distance and the rubber hand illusion. *Frontiers in Psychology* 6:1659.
- *Dynamic Markov Blanket Detection for Macroscopic Physics Discovery*, arXiv:2502.21217; code at `github.com/bayesianempirimancer/pyDMBD`.
- Epoch AI (2026). *Where Autonomy Works: Evaluating Robot Capabilities in 2026*. https://epoch.ai/blog/where-autonomy-works-evaluating-robot-capabilities-in-2026

### 10 · Related notes on this site

- [State is a closure condition, not a given set](https://machengshen.github.io/theory/state-as-closure.md) — the closure ontology this proposal's training signal is built on.
- [Two-body karma: three modes of relational inertia](https://machengshen.github.io/theory/two-body-karma.md) — the same bistable-latch language applied to coupled minds; the caveats about structural rhyme apply there too.
- [The stage log for this line](https://machengshen.github.io/theory/learning-the-self-boundary-log.md) — what each stage overturned or established, in order.

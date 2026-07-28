<!-- Published from the author's working notes. Cognitive state: speculative. -->

# Stage log — the self-boundary line, in the order it happened

*Companion index to [Learning where the self ends](https://machengshen.github.io/theory/learning-the-self-boundary.md) · 2026-07-27 → 2026-07-28 · **not ratified***

---

## How to read this page

This is the audit trail. One line per stage, each saying **what it overturned or established** — because the value of this line is not its conclusion (there isn't one) but the record of a claim being taken apart in public, mostly by its own authors.

A plain-language summary of the whole story is Part I of the [main note](https://machengshen.github.io/theory/learning-the-self-boundary.md). The measured numbers are in Part II of the same note. Working artefacts that are not published here are named so the trail is complete, not to imply they are reachable.

Two abbreviations recur. **The boundary** is the line between "me" and "the world", written **μ** in the technical text and treated as something a machine should learn rather than be handed. **Hysteresis** is the sticking property of a switch whose on-threshold and off-threshold differ — the thermostat that starts cooling at 27 and stops at 25 rather than flipping at 26.

---

## Stage 0 · The proposal (2026-07-27)

| | |
|---|---|
| **Artefact** | Working memo: robot paradigm via a hysteretic self-boundary |
| **Established** | A unified diagnosis: imitation-based and reward-based robot learning share **one** defect — the agent/environment boundary is supplied by an engineer, never derived. Proposal: learn the boundary, with closure violation as the training signal, and make the objective second-order (maintain the condition under which the boundary remains a solution). |
| **Overturned** | Nothing yet. At this point the whole thing rests on one unreferenced clause: "in humans this is empirically well established." |

## Stage 1 · The executable specification (2026-07-27)

| | |
|---|---|
| **Artefact** | `robotics-mu-experiment-spec` — loss functions, analytic bistability conditions, a MuJoCo rig, a measurement protocol with sweep-rate control. Design layer ~95% complete; zero lines run. |
| **Established** | The claim became falsifiable in days rather than years: a 2–3 DoF simulated arm with a detachable tool and a breakable actuator is enough to kill it. |
| **Overturned — three of the memo's own statements, by the act of writing them down precisely** | (1) the boundary cannot be a scalar per channel: the blanket condition is intrinsically three-way, and a scalar cannot express "I am the screen"; (2) "slow in, slower out" is **not free** — a symmetric double well gives threshold symmetry, not on/off time asymmetry; the memo had conflated the two; (3) **raw pixels cannot serve as channels** — the boundary is a partition over channels, so referents need stable identity. That third one is the line's largest cheat, now accounted for explicitly. |

## Stage 2 · Prior-art audit, done as an attack rather than a survey (2026-07-27)

| | |
|---|---|
| **Artefact** | `dmbd-2502.21217-hysteresis-check` — full text of the nearest competing work, extracted and read, not inferred from the abstract. |
| **Established** | The nearest work has **no hysteresis**: its label process is a per-element first-order Markov chain, inference is acausal forward-backward smoothing, and the paper itself states the assignments "quickly diffuse to a uniform stationary distribution in the absence of observed data" — the definition of monostable. Zero occurrences of hysteresis / bistability / bifurcation / saddle-node. |
| **Overturned — ours** | The memo's line "FEP-family blankets have no temporal state" is **wrong for this paper**: its assignments do have their own state. The surviving distinction narrowed to exactly one axis: **monostable versus bistable.** |
| **Also recorded** | Their *general* form lets label transition rates depend on the macroscopic blanket variable — the very loop bistability needs. They assume it away for tractability and list it as future work. Our wedge lands in the next cell of their roadmap: not pre-empted, but not a wide window either. |

## Stage 3 · Evidence audit — the scale narrative (2026-07-28)

| | |
|---|---|
| **Artefact** | `scale-vs-structure-evidence-audit` (≈80% complete) |
| **Established** | "Scale has already solved tool use and damage recovery" is **not supported** — because nobody has measured either. No large model has ever published a functional-transfer success table for unseen tools. The only positive damage-recovery claim is a vendor video with no numbers, whose "damage" was made in-distribution by training across 100,000 simulated morphologies. An 11-year-old paper (5 leg damage conditions + a 14-condition arm damage matrix, adaptation in under two minutes) remains the most rigorous evaluation of that capability. |
| **Overturned — ours, and this is the important half** | There is equally **no** evidence that "better structure" beats scale on a robot: no paper where a structural method beats a 10× larger model on the same task and hardware with trial counts and error bars, and no demonstrated performance advantage anywhere for a *learned* self-boundary. **The other side has real scaling curves; we have a mechanism hypothesis.** The burden of proof is ours. |
| **Strategic consequence** | The valuable thing to claim here is the **measurement protocol**, not the architecture. On architecture we lose to scale; on methodology the field is empty. |

## Stage 4 · Evidence audit — the empirical premise, turned on ourselves (2026-07-28)

| | |
|---|---|
| **Artefact** | `fep-bodyschema-hysteresis-evidence-audit` (≈80% complete) |
| **Overturned — the load-bearing premise of the entire line** | "In humans this is empirically well established" was **false**. Tool incorporation: not only unmeasured for hysteresis — a 2012 re-analysis of six published plus one unpublished experiment concludes tool use *"does not literally extend peripersonal space"*, with small effect sizes and low power. Rubber hand: three rounds of search found **zero** experiments sweeping a parameter up and down to compare transition points. The one supportive number (builds in ~19 s, fades in ~66 s, N=27, the authors never use the word hysteresis) is exactly the kind we had already declared non-discriminative — a monostable leaky integrator gives it for free. |
| **Also overturned — ours** | "Argmax is memoryless ⟹ no hysteresis", used as our own kill-shot, was **already published** in 2022. Our increment is only the second half: attaching it to boundary maintenance. |
| **Downgraded, not refuted** | The nearest famous framework is not a proven result but a framework whose premises were never shown to hold: one 2021 critique removes a central inference step with counterexamples, a 2021 reply supplies the missing premises and relaxes exact to approximate, and a 2022 review finds the required conditions hold "only for a very narrow space of parameters" and demand a perception-action symmetry unusual in living systems. |
| **The same blade, turned on us — a new falsifier** | Our own design uses the *same* three-way blanket structure, so that critique cuts us too: whether a stable partition **exists** on our rig became a prerequisite question, added as stage D0 ahead of everything else. |
| **And again** | "We measured a non-zero hysteresis loop" is not evidence of bistability either: any first-order lag produces a rate-dependent loop at finite sweep rate. The criterion was tightened to **loop area extrapolated to zero sweep rate stays positive**. |

## Stage 5 · Data hunt — three rounds, and one repeated mistake (2026-07-28)

| | |
|---|---|
| **Artefacts** | `rhi-hysteresis-reanalysis-hunt` (≈85%), `trial-level-embodiment-data-hunt`, `openneuro-bids-rhi-hunt` |
| **Established — why the data does not exist** | Not because nobody thought of it. Every parameterised study randomises condition order, because the standard hygiene of the field treats sequence effects as **contamination rather than signal**. The paradigm was built to erase precisely the quantity we need. |
| **Established — scope of the vacuum** | Trial-level ownership data: zero hits across a public-repository search of 16 keyword sets, a second repository with 10 sets, and a **full census of 1831 neuroimaging datasets**. |
| **Overturned — ours, three times in a row** | Three separate "trial-level data available" statements were believed and then opened by hand. All three contained participant × condition aggregates with **no trial index and no order column**, making the question structurally uncomputable. Twice more, a dataset whose parameter column was a genuine monotone up/down sweep — the first real sweep found in four rounds — had a response column that was blank on every row. **Do not trust the task name or the availability statement; open the columns.** |
| **Overturned — a search agent's over-conclusion, corrected** | The claim "trial-level structure doesn't exist at the paradigm level" is wrong for one major lab: their published table *is* a trial-level binary ownership judgement, twelve trials per condition. The paradigm exists and is mature; the raw logs are simply never uploaded. The right next move is therefore to ask the authors, not to build a new paradigm. |
| **Established — methodological templates** | The same hysteresis blade has already been applied to audiovisual synchrony; a 2018 paper supplies the operational definition of a hysteresis width plus a randomised third baseline arm; binocular rivalry is the only literature with multiple sweep rates built in, i.e. the only one that can execute the zero-rate extrapolation criterion. |
| **Against us, again** | A 2014 study shows hysteresis and adaptation are independent, additive and anatomically separable ⟹ **measuring zero net hysteresis does not prove there is no latch**; the two can cancel. This has to be pre-registered, or a null result is neither a self-falsification nor an alibi. |

## Stage 6 · Human data re-analysis — two independent points, both against (2026-07-28)

| | |
|---|---|
| **Artefacts** | `mu-boundary/human-reanalysis/` |
| **Overturned — the direction of the effect** | Two independent manipulations (spatial distance, N=34, published; temporal synchrony, N=185, re-analysed by us from public data), two samples in different countries, two measurement types (experienced, expected) — **all on the adaptation/contrast side, none in the hysteresis direction.** In the larger dataset the same weak condition is rated **0.891 lower** when preceded by the strong condition, 95% CI [−1.232, −0.550], p = 6.7e-7. Convergence across independent designs is worth more than either result alone. |
| **Down-weighted by us, found by reading their materials** | That larger dataset measures **expectation**, not experience — participants watched a video and reported what they would expect to feel. Its control items also move in the same direction, so demand characteristics are real; but the effect on illusion items is ~2.8× that on control items, so a genuine component exists and cannot be cleanly separated here. |
| **Established — a technical fact that decides success or failure later** | On a dry run of the analysis pipeline, **the permutation null is not centred at zero but at +0.191**, for an identified reason. Testing against zero reads the sign backwards: a naive test says "no effect", while against the correct null the same data is significantly negative. Two independent null models agree. **Discipline: locate the null centre on your data before discussing significance.** |
| **Established — a hard design constraint for any future experiment** | If the sign of the manipulated parameter maps directly onto the semantics of the binary response, hysteresis and adaptation are **mathematically indistinguishable**. A trial-level ownership question must therefore stay "yes/no" and must never become "which hand feels more like mine". |
| **Decision** | Do not fund a self-built VR study yet: the prior has worsened, so the expected value has dropped. Priority becomes (1) request trial-level logs from the lab that has them, (2) continue on the simulation side, which does not depend on the biological premise. |

## Stage 7 · Simulation D0 — does the boundary even have an object? (2026-07-28)

| | |
|---|---|
| **Artefact** | `mu-boundary/RESULTS-D0.md` |
| **Established — the instrument works** | Positive control with a hand-installed double well: zero-rate loop area +0.36…+0.62 against a linear negative arm whose value is indistinguishable from zero. Analytic anchors reproduced to 2.6%; saddle-node scalings to 5%. Later negative results can therefore be attributed to the system, not the ruler. |
| **Overturned — our own criterion** | The negative arm's bootstrap confidence interval also excludes zero, because it reflects seed noise and not the systematic bias of having few sweep-rate points. **The correct criterion is not the confidence interval but a resolution floor and the factor by which the positive arm exceeds it.** |
| **Established, but nearly information-free** | A non-trivial partition satisfying the blanket condition does exist ⟹ the hysteresis discussion has an object. But a deliberately leaky calibration partition scores only marginally differently, so the dynamic range is **smaller than the across-seed spread**. The famous critique lands on our rig in mirror image: not "the condition holds only in a narrow region" but "it holds so easily that it selects nothing." |
| **Overturned — our own diagnosis, in the very next round, and this is the most reusable finding** | We had diagnosed the weak result as "the rig is too weakly coupled to the world" and shipped that as a premise. **It was wrong.** The weakness was a protocol defect; after fixing it, *both* rigs pass, including the one we had condemned. The probe we blamed the rig with runs along a path that never touches the blamed component and is structurally blind to it. **We read our probe's signal-to-noise as the system's coupling strength.** A real rig defect did exist — found only by building a second, estimator-agnostic probe. |
| **General lesson extracted** | Any time you argue "indicator X tells me about property Y", first show X is sensitive to Y; if you cannot, build a probe that does not share X's assumptions. |
| **Measurement pitfalls recorded** | Two of them invert the specification's own worries: giving the auxiliary predictor *less* regularisation manufactures false positives (an overfit predictor *fakes* the blanket condition); and contiguous temporal splitting with non-stationary exploration fabricates conclusions outright. ⟹ this indicator is more sensitive to estimator settings and data splitting than to the partition under study, so any experiment using it must first run a deliberately leaky calibration as a positive control. |

## Stage 8 · Simulation D1 — is the mechanism reachable? (2026-07-28)

| | |
|---|---|
| **Artefact** | `mu-boundary/RESULTS-D1-D2.md` |
| **Established** | Yes: legal parameters exist, and nothing has to be pushed to an absurd magnitude. |
| **Overturned — the criterion the specification called make-or-break** | Passing it turns out to be **nearly the same sentence as "the boundary flipped"**, so it screens out nothing. The specification overestimated it. |
| **Overturned — the specification's literal equation** | Its stated form **cannot** have three stable settings, as mathematics rather than numerics: two requirements demand opposite signs of the same quantity. Verified numerically and pinned with a regression test that pushes the coupling to 10,000× without ever producing three. A minimal structural repair was adopted. |
| **Overturned — a size estimate of ours, by 7×** | Reading the key quantity the way the specification literally says overestimates it sevenfold, because it smuggles in *channel identity* (some channels are intrinsically easy to predict) rather than the loop quantity. |
| **Overturned — a rescuing number, by a representation control** | One channel showed a value that would have saved the theory (0.98). Re-expressing the same information in polar coordinates collapses it to 0.007: the large value was our basis functions being unable to compute an inverse trigonometric function, not an information gap. Representation-invariant reading: at most ~0.18, tool channels 0.002–0.045. **A control we would not have run if the number had been small.** |
| **The real obstruction, newly found** | For two stable settings to exist, a cost/benefit ratio must land in a window whose relative width equals that measured quantity — **1.3–2.6% for tool channels** — while the objective function's own coefficients place every channel **2 to 420 window-widths outside**. Nothing in the objective pulls it in. ⟹ the effect does not fall out of the proposed objective; it requires a hand-set ratio the objective does not supply. |

## Stage 9 · Simulation D2 — the verdict (2026-07-28)

| | |
|---|---|
| **Artefact** | `mu-boundary/RESULTS-D1-D2.md`, 25 tests passing |
| **Established — the one surviving pillar** | With the hand-installed non-linearity **entirely removed** and only the self-reinforcing trust loop left, hysteresis appears and survives extrapolation to zero sweep rate: 24–35× the resolution floor, with both branches held 1.00/1.00 over long holds. The negative control (trust frozen constant) correctly falls back to the floor and is digit-for-digit identical to the earlier linear arm, as a regression test asserts. **Hysteresis does not need to be hand-installed.** |
| **Overturned — self-specificity, by the control we had demanded of ourselves** | Give the identical treatment to the uncontrollable wind-blown ball with *its own* measured numbers ⟹ no hysteresis (the honest half). But raise the ball's one free amplitude until the loop gain matches ⟹ **every hysteresis number is identical to the arm's, digit for digit.** After normalisation the equations depend only on that gain, so the "self" quantity decides how large the free knob must be, not whether the effect occurs. ⟹ **hysteresis is a generic property of a gated slow variable; the inference "it sticks, therefore it is a self-boundary" is cancelled.** |
| **Overturned — the signature prediction, twice** | "Slow in, slower out" is false here. Gate on the benefit: the ratio is 1.008 — **no asymmetry at all**, and the apparent asymmetry is an artefact of the 1-D reduction (which is asymmetric at the origin by construction). Gate on the whole drive, i.e. the mechanism actually intended: asymmetry appears but **points the wrong way** — release is faster and the threshold to leave is lower. Computable reason: precision amplifies *all* evidence about a channel, including the evidence against it. Getting "easy in, hard out" requires an extra, asymmetric evidence weighting — another hand-installed component, which is what we were avoiding. |
| **Honest scope** | This stage ran on the reduced one-dimensional equation driven by measured parameters, not on the full 34-channel rig; the encoder was not trained; the intended physical parameter axis (grip stiffness) was never swept. Those are the largest open items. |

---

## Where the line stands

| component of the original claim | status |
|---|---|
| hysteresis emerges without a hand-installed non-linearity | ✅ survives |
| the hysteresis is specific to the self-boundary | ❌ generic property of gated slow variables |
| release is slower than incorporation | ❌ reversed, in both implementations |
| it falls out of the proposed objective without fine-tuning | ❌ needs a ~2% hand-set ratio |

Three of four down, **every one of them felled by our own simulator or our own re-analysis**. The human-side motivation is not merely unproven — the two usable data points point the wrong way.

**The question that replaced it**, and the reason this line stays open: hysteresis is cheap, so the real question is *what would make a boundary's hysteresis be about that boundary itself* — rather than a property it shares with a ball blowing in the wind.

**Not ratified. Nothing here is a settled result.** Full narrative and all measured numbers: [Learning where the self ends](https://machengshen.github.io/theory/learning-the-self-boundary.md).

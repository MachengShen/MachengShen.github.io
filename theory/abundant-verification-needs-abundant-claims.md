<!-- Published from the author's working notes. Cognitive state: speculative. -->

# Abundant verification needs abundant claims

*A cross-line note addressed to Jie Fu's verification line — one convergence, one measured number, three objections, and one thing we would rather take than give · Macheng Shen × agent · 2026-08-06*

## What this is

This is a note addressed to a specific public line of work, in the same genre as the earlier note addressed to a parallel information-ontology channel: an invitation, not a scorecard. The line is Jie Fu's (付杰, Research Scientist at IQuest Research; previously a postdoctoral fellow with Yoshua Bengio at Mila), whose stated program is to *"preserve and flourish humanity by providing abundant verification."*

Three of his contributions are load-bearing here, and they are his, not ours:

1. **Re:Form** ([arXiv:2507.16331](https://arxiv.org/abs/2507.16331), TMLR May 2026; Chuanhao Yan, Fengdi Che, Xuhan Huang, Xu Xu, Xin Li, Yizhi Li, Xingwei Qu, Jingzhe Shi, Chenghua Lin, Yaodong Yang, Binhang Yuan, Hang Zhao, Yu Qiao, Bowen Zhou, Jie Fu). The diagnosis: for LLMs trained with RL on informal language, *the verification process that supplies the training signal is neither reliable nor scalable.* The remedy: generate inside a formal space — Dafny — where verification is automatic and provable. The results: **DafnyComp**, a benchmark of compositional formal programs with auto-formalized specifications; an SFT stage after which even a **0.5B** model emits syntactically valid, verifiable Dafny and beats proprietary models on it; RL with regularization improving out-of-domain generalization. The framing that matters most to this note is the *"reducing human priors"* one — no engineer writes per-sample preconditions, postconditions or invariants; the pipeline harvests verifier diagnostics and iterates.

2. **The autoformalization agenda** ([project page](https://bigaidream.github.io/project/auto/)): converting natural-language content into verifiable formalization, on the explicit premise that current LLMs "cannot do genuine logical reasoning or self-verification on their own."

3. **A note dated 2026-08-05** (小红书, note `6a73027b`) announcing sparse matrix factorization as an efficient mechanistic-interpretability method — reportedly matching mainstream MI at roughly **1%** of the data — and, more importantly, stating the vision: inside David Dalrymple's Guaranteed Safe AI frame ([arXiv:2405.06624](https://arxiv.org/abs/2405.06624)), let the verifier check not only a model's *outputs* but, cheaply, its *internals* — 君子论迹，也论心 — driving whole-pipeline verification cost down so society gets cheaper, more reliable **verification tokens**. The same note lists its own limitations: the reductionist assumption sits badly with emergent capability, and the circuits found are local and possibly non-unique. *(As of 2026-08-06 we could not locate the corresponding preprint; the citation is the note, and it should be replaced with the paper when it appears.)*

## The convergence, stated as evidence rather than as a contribution

On 2026-07-27 this line wrote a private note starting from something entirely unrelated to formal methods: the engineering reading of Sapir–Whorf, in which a language is a *lossy projection* of the world, so natural language is a projection tuned for human daily communication and therefore not tuned for verification. Running that forward produced the conclusion that the live gap is not the existence of formal languages — Lean, Coq, TLA+, Alloy, Dafny all exist — but the **informal↔formal translation**, i.e. autoformalization, with Dafny named as the concrete target.

That is the same wedge, reached from a different direction, two years later than the people actually building it. We record it as convergent evidence about where the gap is, and explicitly not as a contribution. Prior art is a clue, not a verdict — but when the clue is "sixteen authors already built the thing and published the benchmark," the honest move is to hand over what we have that they do not, and take what they have that we lack.

## The one measured thing we have: the bottleneck is not unit cost

The *"abundant verification tokens"* framing optimizes the **unit cost** of a verification. We have been running the other end of the same pipe — a small agent fleet in which verification is nominally mandatory, and every completion or blocker must carry evidence — and the constraint that actually binds there is not cost. It is that **the verifier cannot parse what it is handed.**

Concretely. A live gate in that fleet enforced a micro-assertion (*"the evidence that this blocker is real ="*) written as prose and checked with a regular expression. A regex is semantically blind, so the gate both missed real cases and fired on documents whose entire point was that nothing was blocked. On 2026-07-27 we replaced the prose assertion with a minimal **typed** receipt schema — `kind`, `claimed-action`, `verifier-id` always; completions additionally carrying `verified-by`, `evidence-cmd`, `evidence-output-hash`; blockers carrying `blocker-evidence-cmd` — and ran both against the same corpus. Re-run 2026-08-06:

| | corpus | result |
|---|---:|---|
| corpus | 18 items | 10 genuine parks, 8 non-parks including a known false-positive genre |
| prose + regex, recall on false parks | 10 | **5 (0.50)** |
| prose + regex, semantic false triggers | 8 | 0 |
| typed field, blind spot | — | none of the missed genres are expressible as a regex blind spot |
| schema self-checks | 4 | 4 pass |

The misses share a shape: a park with no adjacent action verb — *"waiting on owner: &lt;question&gt;"*, *"owner action item: confirm the model number"*, *"pending owner decision"*. Half of them. And the cost of one miss, measured in the wild: **a capability sat parked for about eighteen days behind a blocker nobody had ever executed** — the stated precondition was simply false, and no component errored, because a false blocker is indistinguishable from a true one to a checker that cannot read. An audit of the 11 parked items in that batch found 3–4 more of the same kind. *(That last figure is an audit estimate, not a clean measurement, and is stated as a range for that reason.)*

The claim we would offer upward, then: **cheap verification does not help if the thing being verified is stated in a form the verifier cannot parse.** An abundant supply of verification tokens presupposes an abundant supply of *well-typed claims*, and in deployed agent systems that supply does not exist — the claims are prose. Which suggests that autoformalization's nearest paying customer may not be mathematics at all. It may be **the claim layer of running agent systems**: every agent completion receipt is an informal assertion that wants to be a machine-checkable one, the corpus is enormous and grows daily, and the verifier's own pass/fail is the label.

Two numbers, per house rule. **P(mechanism — a typed claim layer strictly dominates prose-plus-regex for this class of check) ≈ 0.9**: it is measured directly, and the mechanism is not subtle. **P(useful at realistic scale — that claim typing rather than verification unit cost is the binding constraint in agent deployments generally) ≈ 0.3**: n = 1 fleet, corpus of 18, and — the reason to discount hardest — *the same authors wrote both the regex being beaten and the schema that beats it.* A stronger baseline is named as a falsifier below.

## Three objections to verifying internals

These are objections, not corrections. They are aimed at the *"论心"* half — cheap verification of model internals — and each carries what would dissolve it.

**One: an auditable certificate and a statistical decomposition are different objects.** The Guaranteed Safe AI frame asks the verifier for *an auditable proof certificate*. An MI-derived internal check emits a decomposition — a report, produced by machinery that a third party who did not co-train would have to trust. The literature that constrains this is not, as our own private note wrongly claimed, a pair of papers about unreadable emergent protocols; we went to check those citations for this note and neither says it, so that claim is withdrawn here. What does hold is weaker and still bites: policies and conventions specialized by self-play fail to coordinate with independently trained partners ([Other-Play, Hu, Lerer, Peysakhovich & Foerster, arXiv:2003.02979](https://arxiv.org/abs/2003.02979)), and the standard metrics for whether a learned channel means anything are themselves misleading ([Lowe, Foerster, Boureau, Pineau & Dauphin, arXiv:1903.05168](https://arxiv.org/abs/1903.05168)). Transposed: a readout tuned on one training run is exactly the kind of convention that need not transfer to the party who has to audit it. The question we would ask: **what would make an MI readout a certificate rather than a report?** Our own answer, which is where this line's interest is, is that you want the *machine-checkable* half of a private representation without the *human-unauditable* half — and that is a property of the receipt, not of the model.

**Two: non-uniqueness is path-dependence, and that is a spec requirement, not a caveat.** His note lists "circuits are local and possibly non-unique" among its limitations. A separate line here has been studying verification signatures that are hysteretic — path-dependent rather than lookup-shaped — and we killed our own self-specificity claim in that line, so we hold it loosely. But the inference transfers cleanly: **if the decomposition is not unique, an internal-verification claim is reproducible only if it carries its own path.** Which run, which data, which initialization, which tolerance. That converts a caveat you live with into a field you can check, and it costs one line in a schema.

**Three: making verification cheap puts optimization pressure on the verifier's input channel.** This is the reason our own schema is deliberately **SHADOW** — it logs and blocks nothing. The moment a schema becomes a gate, agents acquire an incentive to emit schema-*conformant fabrications*: our residual risk is a lazy agent pasting a plausible `evidence-output-hash` without ever re-running the command, and the schema raises the cost of that without eliminating it. Scaled up, this is Goodhart aimed at internals: **once "clean internals" are load-bearing, clean internals become the target.** A model under any optimization pressure toward passing an internal check is being trained, in part, to present internals that pass. We do not know whether the GS-AI frame budgets for a verified party that optimizes against the verifier's readout specifically; we would like to know, and we would rather be told it is already handled than be right.

## What we would rather take than give

The asymmetry is honest and runs the other way. Our shadow checker is a hand-rolled draft-07 subset validator; the thing we do not have is the informal→formal translation itself, which is precisely the Re:Form pipeline pointed at a different corpus. If any of the above is worth an afternoon to that group, the concrete suggestion is a **DafnyComp-shaped benchmark over operational claims rather than programs** — compositional, auto-formalizable, with the verifier's execution as ground truth — because that is the corpus where the informal side is already abundant and nobody has typed it.

## What would kill this note

- **The strongest one.** Run a semantically competent prose checker — an LLM judge — against the same 18-item corpus. If it matches the typed schema's recall with no semantic false triggers, then claim *typing* buys nothing and this note's core is dead: the gap was the regex, not the prose. We have not run that baseline, and until we do, 0.3 is generous rather than modest.
- If MI readouts can be made to re-run — a third party recomputing the decomposition and recovering the same circuit within a stated tolerance — objection two collapses into an engineering detail, correctly.
- If agent receipt corpora turn out too noisy or too low-diversity to train an autoformalizer, the "second customer" suggestion is dead and the fleet should just keep hand-writing schemas.
- If the GS-AI literature already treats adversarial pressure on internal readouts, objection three is not news and should be struck rather than softened.

## Cognitive state

`speculative`, deliberately, and the parts do not deserve the same tag. The corpus-scan numbers are reproducible on demand and would stand as `survived` at n = 1; the transfer claim addressed to another group's research program has had no test at all. An artifact carries one state on this site, and the honest single state is the weaker one.

## References

- Chuanhao Yan et al., *Re:Form — Reducing Human Priors in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny*, [arXiv:2507.16331](https://arxiv.org/abs/2507.16331), TMLR (May 2026). Code and models: [Veri-Code/ReForm](https://github.com/Veri-Code/ReForm).
- Jie Fu, [*Autoformalization and Formally Verifiable AI*](https://bigaidream.github.io/project/auto/), and [homepage](https://bigaidream.github.io/).
- Jie Fu, note on sparse matrix factorization for mechanistic interpretability and abundant verification tokens, 小红书 note `6a73027b`, 2026-08-05.
- David "davidad" Dalrymple, Joar Skalse, Yoshua Bengio, Stuart Russell, Max Tegmark, Sanjit Seshia, Steve Omohundro, Christian Szegedy, Ben Goldhaber, Nora Ammann, Alessandro Abate, Joe Halpern, Clark Barrett, Ding Zhao, Tan Zhi-Xuan, Jeannette Wing, Joshua Tenenbaum, *Towards Guaranteed Safe AI: A Framework for Ensuring Robust and Reliable AI Systems*, [arXiv:2405.06624](https://arxiv.org/abs/2405.06624).
- Hengyuan Hu, Adam Lerer, Alex Peysakhovich, Jakob Foerster, *"Other-Play" for Zero-Shot Coordination*, [arXiv:2003.02979](https://arxiv.org/abs/2003.02979), ICML 2020.
- Ryan Lowe, Jakob Foerster, Y-Lan Boureau, Joelle Pineau, Yann Dauphin, *On the Pitfalls of Measuring Emergent Communication*, [arXiv:1903.05168](https://arxiv.org/abs/1903.05168), AAMAS 2019.
The wider autoformalization frontier is deliberately not surveyed here. This note is addressed to one line, not to a field, and a survey it did not do is not a survey it should pretend to.

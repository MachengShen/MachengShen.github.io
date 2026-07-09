<!-- Published from the author's working notes. Cognitive state: mixed; each claim is tagged inline. -->

# Coordination Structures as Resource-Scheduling Architectures

*A descriptive theory. Draft, 2026-07-09.*

Every substantive claim below carries a tag: `[consensus]` for established
textbook results, `[empirical]` for claims with cited supporting data,
`[speculative]` for my own untested extensions, and `[retired]` for a stronger
claim that is available and attractive in this space and is rejected here, with
the reason given. The essay states mechanisms and their measurable
proxies. It does not rank the mechanisms, name culprits, or recommend anything.
Where it uses the vocabulary of learning systems, it marks explicitly where the
correspondence is a mathematical derivation and where it is only a structural
rhyme.

## 1. The object of study

Treat a polity, a firm, a market, and a self-governed commons as four instances
of one object: an *architecture for scheduling scarce resources under
distributed, private information*. The scheduling problem is fixed. Many agents
each hold local information (about their own costs, needs, capacities,
preferences) that no one else has and that is expensive or impossible to
transmit in full. Some allocation of resources must nonetheless be chosen. The
architectures differ in how they gather the dispersed information, who decides,
and how the consequences of decisions feed back to the units that made them.

This framing is deliberately flat. It does not treat "the state" as a moral
agent, "the market" as a natural fact, or "the firm" as a mere legal shell. Each
is a mechanism with an information flow and an incentive structure, and each can
be described in the same terms as the others. The interesting questions are
comparative and empirical: given the information structure of a domain, which
architecture schedules it at lower cost, and what happens to that answer when
the cost of communication and computation changes.

## 2. Two algorithms, and the result that they are special cases

Capitalism and socialism, stripped to their scheduling content, are two
algorithms over the same problem. In one, allocation is set by decentralized
exchange at prices that no single party controls. In the other, allocation is
set by a central plan that assigns quantities directly. The twentieth-century
argument over which is correct — the *socialist calculation debate*, opened by
Ludwig von Mises in 1920 and carried by Oskar Lange, Abba Lerner, and Friedrich
Hayek into the 1940s — is, read descriptively, an argument about which algorithm
can extract and use dispersed information at acceptable cost `[consensus]`.
([Socialist calculation debate, overview](https://en.wikipedia.org/wiki/Socialist_calculation_debate);
[Persky, "Retrospectives: Lange and von Mises, Large-Scale Enterprises, and the Economic Case for Socialism," *J. Econ. Perspectives* 5(4):229, 1991](https://doi.org/10.1257/jep.5.4.229))

The theory of mechanism design later placed both algorithms inside one formal
space. A *mechanism* is a rule mapping the agents' reported information to an
outcome; the design question is which rules induce agents to report truthfully
(incentive compatibility) and transmit the least information necessary
(informational efficiency). Leonid Hurwicz, Eric Maskin, and Roger Myerson
received the 2007 Nobel Memorial Prize for this framework, which treats market
and plan as points in a common design space rather than as rival ideologies
`[consensus]`.
([Nobel scientific background, 2007](https://www.nobelprize.org/prizes/economic-sciences/2007/);
[Myerson, "Perspectives on Mechanism Design"](https://www.nobelprize.org/uploads/2018/06/myerson-slides.pdf))
Hurwicz's own results are the load-bearing part: he showed that the requirement
to elicit private information truthfully constrains *any* mechanism, and proved
negative results bounding what decentralized information-revelation can achieve
`[consensus]`.

Once both are special cases, "which is right" is the wrong question and "what is
the optimal mixture, as a function of the domain's information structure" is the
right one. The mixture is not a compromise between ideologies; it is a point
chosen by the information geometry of the problem. Domains whose relevant
information is cheap to standardize and transmit admit more centralized
scheduling at lower cost; domains whose relevant information is tacit, local, or
strategically withheld resist it. This is a claim about information, not about
virtue.

## 3. The information constraint, stated twice

The binding constraint on any central scheduler was stated, in two independent
vocabularies, by Hayek and by James Scott.

Hayek's *The Use of Knowledge in Society* (1945) argues that the knowledge
relevant to allocation exists only as dispersed, local, often unarticulated
fragments, and that market prices act as a compression of that knowledge — a
low-dimensional signal that lets an agent act correctly on information it never
directly receives `[consensus]`.
([Hayek 1945, *American Economic Review* 35(4):519–530](https://en.wikipedia.org/wiki/The_Use_of_Knowledge_in_Society);
[full text, Liberty Fund](https://oll.libertyfund.org/titles/hayek-the-use-of-knowledge-in-society-1945))
The load-bearing point is subtle and frequently misread: Hayek's objection is
not that a planner has too little compute. It is that the relevant information is
*never transmitted at all* — it is local, tacit, and in some cases only comes
into existence through the act of exchange.

Scott's *Seeing Like a State* (1998) states the same constraint from the
scheduler's side. To schedule centrally, an authority must first make its domain
*legible*: it must impose standardized categories, measures, and records that
render local reality countable. Scott's empirical claim, drawn from cases in
forestry, cadastral mapping, and agriculture, is that the act of imposing
legibility discards the local, contextual knowledge — he uses the term *mētis* —
that made the original arrangement function `[empirical]`.
([Scott 1998, Yale University Press; overview](https://en.wikipedia.org/wiki/Seeing_Like_a_State))
Here I will avoid the word "destroys," which smuggles a verdict: the descriptive
claim is that the standardized representation is *lossy* with respect to the
information that governs local outcomes, and that decisions made on the
compressed representation can diverge measurably from decisions made with the
full local information. Whether that loss is worth its coordination gains is
exactly the empirical mixture question, not a foregone conclusion.

The Soviet *material-balance* method is the cleanest historical instance of the
constraint operating at scale. Gosplan allocated by tabulating physical supplies
and requirements for thousands of commodities and iterating toward consistency,
in physical units rather than prices. By 1973 balances were computed for on the
order of 1,900 of the most important items, a small fraction of the millions of
distinct goods in the economy, and the recorded difficulty was precisely the
*aggregation*: the categories legible to the center were coarser than the
distinctions that governed whether an allocation actually worked `[empirical]`.
([Material balance planning](https://en.wikipedia.org/wiki/Material_balance_planning))
I state this as a mechanism, not a morality tale: coarse legible categories
produce allocation error at a rate that rises with the mismatch between category
granularity and the granularity of the underlying information.

## 4. Does cheap computation move the optimal point?

This is the one genuinely open question in the essay, and I want to state it
without resolving it, because the honest answer is that it is not obvious.

The intuition that modern computation and rich telemetry shift the
centralize/decentralize optimum *toward* the center is real and has real force:
a scheduler that can ingest and process orders of magnitude more data than
Gosplan could is a different scheduler `[speculative]`. Contemporary logistics
networks, ride dispatch, and cloud resource allocation are large centralized
schedulers that outperform the market alternatives *within their domains*, and
they do so because the relevant information — locations, capacities, latencies —
is now cheaply instrumented and transmitted.

But the Hayek/Scott objection was never primarily about compute. It was about
information that is *never transmitted*: tacit, preference-dependent, or
strategically suppressed. More compute at the center does nothing for
information that never enters the channel. Worse, incentive compatibility
(Section 2) says that agents' willingness to reveal private information depends
on the mechanism's rules, not on the center's processing power — a scheduler
that can process everything still faces agents deciding what to report
`[consensus]`. So cheap computation plausibly moves the optimum toward the
center in the sub-domains where the binding constraint was *transmission and
processing* of in-principle-observable data, and leaves it roughly where it was
in the sub-domains where the binding constraint was *information that is tacit,
never articulated, or strategically withheld.* The net direction of the shift is
therefore domain-specific and, at the level of a whole economy, genuinely
undetermined by the theory. Anyone claiming the general answer is obvious in
either direction is overclaiming.

`[retired]` A stronger version of this claim is available and tempting: that once
telemetry is dense enough, the socialist-calculation problem dissolves and
central scheduling strictly dominates. It is rejected here. It conflates the two
constraints above —
treating the entire Hayek/Scott argument as a claim about insufficient compute,
which it demonstrably is not — and it ignores that incentive compatibility is
invariant to the center's processing power. The dense-telemetry claim is true
only on the transmission-limited sub-domains and is simply misapplied on the
rest.

## 5. Boundaries and scale: the transaction-cost machinery

Why do large coordinating structures exist at all, if decentralized exchange is
so informationally efficient? Ronald Coase answered in 1937: because using the
market is not free. There are costs to discovering prices, negotiating, and
enforcing each transaction, and when those costs exceed the cost of organizing
the same activity by internal direction, agents form a firm. The boundary of the
firm sits where the marginal cost of internal coordination equals the marginal
cost of a market transaction `[consensus]`.
([Coase 1937, *Economica* 4(16):386–405](https://en.wikipedia.org/wiki/The_Nature_of_the_Firm))
Oliver Williamson operationalized this into transaction-cost economics: the
make-versus-buy boundary is set by bounded rationality, uncertainty, and above
all *asset specificity* — the degree to which an investment is worth less
outside a particular relationship, which exposes the parties to holdup that
contracts cannot fully resolve `[consensus]`.
([Williamson, Nobel lecture, "Transaction Cost Economics: The Natural Progression"](https://web.pdx.edu/~nwallace/EHP/TCEProgression.pdf))

The descriptive extension to states and other large structures is
straightforward and does not require any moral coloring: a large coordinating
structure lowers coordination cost *inside* its boundary — a common currency,
common rules, common records, common enforcement — and it raises coordination
cost *across* its boundary, because a counterpart outside must bridge different
currencies, rules, and records `[speculative]`. The structure is, in dynamical
terms, an attractor: within its basin, transactions flow cheaply and tend to
route through it; at its edge, they meet a barrier. This is a description of a
cost gradient. It is not a claim that internal cheapness is good or that the
boundary barrier is bad; both are simply consequences of the same architecture,
and their net effect on any given transaction depends on where that transaction
sits relative to the boundary.

## 6. Credit routing: a lens, marked as a lens

Here I introduce a framing from the study of learning systems, and I mark its
epistemic status carefully, because the essay's credibility depends on not
letting an elegant formalism import unearned truth.

In a learning system, improvement requires that a signal about the quality of an
outcome propagate backward to every internal structure that contributed to it.
Marvin Minsky named this the *credit-assignment problem* in 1961: when a complex
system succeeds or fails, how is credit or blame distributed among the many
internal decisions that produced the result `[consensus]`.
([Minsky, "Steps Toward Artificial Intelligence," 1961](http://incompleteideas.net/papers/Minsky60steps.pdf))
Backpropagation is one exact solution for a differentiable network: it computes,
for every internal parameter, its contribution to the output error and adjusts
it accordingly `[consensus]`. (Rumelhart, Hinton & Williams, "Learning
representations by back-propagating errors," *Nature* 323:533–536, 1986.)

The *lens*: an institution is a structure through which outcomes are produced,
and one can ask, as an empirical question, whether the signal generated by an
outcome — the reward, the loss, the correction — reaches the units that actually
generated that outcome, and how long it takes to get there. Call these
properties the *fidelity* and *latency* of credit routing. An institution in
which a failure's cost falls on the units that caused it, quickly, is doing
something structurally analogous to a low-latency backward pass. An institution
in which the cost falls elsewhere, or arrives after the causal units have
dispersed, is doing something structurally analogous to a broken or
high-latency one.

I state whether credit reaches the generating units as a *measurement*, not an
accusation. The proxy is concrete: after a documented failure in an institution,
measure the time until the units causally responsible experience a corrective
consequence, and the fraction of the corrective signal that lands on them versus
elsewhere. These are, in principle, observable quantities.

## 7. The boundary between rhyme and derivation

This is the section the rest of the essay is accountable to.

The transaction-cost account of boundaries (Sections 5) is a *derivation*: it is
a genuine economic model with comparative-static predictions, and its terms
(coordination cost, asset specificity) are defined and, in favorable cases,
measurable. The information constraint (Section 3) is a *derivation* in the sense
that Hayek's price-compression argument and Hurwicz's incentive-compatibility
results are formal claims with proofs and stated assumptions. Mechanism design's
special-case result (Section 2) is a theorem.

The credit-routing framing (Section 6) is a *rhyme*, and I will not pretend
otherwise. Backpropagation is a statement about a differentiable function: there
is a well-defined loss, a well-defined gradient, and a guarantee that the
backward pass computes exactly the contribution of each parameter. An
institution has none of these. There is no scalar loss function; there is no
gradient; there is no guarantee that "the units that caused an outcome" is even
well-defined, because causation in a social structure is distributed,
contested, and often unrecoverable. "Fidelity" and "latency" of credit routing
are *metaphors operationalized as proxies* — useful because they tell you what
to measure, dangerous if you let them inherit the mathematical certainty of the
thing they are named after. The rhyme earns its place only by generating
falsifiable measurements (Section 8). It does not earn the right to be called a
model.

`[retired]` A tempting version of this framework would assign each institution a
single scalar "credit-transport fidelity" score, by analogy to a loss gradient,
and rank institutions by it. That move is rejected here. Credit in a social
structure is multi-dimensional (financial, reputational, legal, informational),
the backward pass is not differentiable, and collapsing it to one number was the
formalism smuggling in a structure the domain does not have. The scalar looked
rigorous and was not. What survives is the *pair* of separately measurable
proxies above, applied per-dimension, with no claim that they compose into a
gradient.

## 8. What would falsify this

Three concrete, checkable predictions. Each is stated so that a specific
observation would count against the theory.

**Falsifier 1 — the information-constraint prediction.** Partition economic
domains by whether the information that governs good allocation is *telemetered*
(cheaply instrumented and transmitted) or *tacit* (local, preference-dependent,
or strategically withheld). The theory predicts that centralized scheduling
gains ground, relative to decentralized market mechanisms, in the telemetered
domains as computation cheapens, and does *not* gain ground in the tacit
domains. Disconfirmation: if centralized scheduling comes to outperform
decentralized mechanisms even in domains where the governing information remains
tacit and un-telemetered, the Hayek/Scott information constraint is false or
inessential. Conversely, if decentralized markets keep winning even in fully
telemetered domains, then "cheap computation shifts the optimum toward the
center" is false. Either observation kills a load-bearing claim.

**Falsifier 2 — the credit-routing prediction.** Across institutions matched for
scale and domain, measure time-to-correction after documented failures (the
latency proxy of Section 6). The theory predicts that lower-latency,
higher-fidelity credit routing is associated with faster measured adaptation and
lower persistent repeated-error rates. Disconfirmation: if institutions with
demonstrably slow or misrouted credit adapt just as fast as those with fast,
well-targeted routing, then the credit-routing lens has no empirical purchase and
should be dropped entirely — it would be revealed as pure metaphor.

**Falsifier 3 — the boundary-shift prediction.** The transaction-cost account
(Section 5) implies that as communication and coordination costs fall, the
firm/market boundary moves in coordination-cost-sensitive sectors but *not* in
sectors where asset specificity, rather than communication cost, is the binding
constraint. Prediction: a measurable divergence between the two sector types in
how make-versus-buy boundaries shift as communication cost falls.
Disconfirmation: if falling communication cost produces no measurable boundary
shift in the coordination-cost-sensitive sectors, or shifts asset-specific and
non-asset-specific sectors identically, then transaction cost is not doing the
work the theory assigns it.

A fourth, already partially tested, is offered as a bonus because it cuts against
optimism about the newest structure: token-weighted governance should trend
toward concentration of decisive power over time, measurable as a falling
Nakamoto coefficient or rising Gini of effective voting weight. If token-weighted
systems reliably do *not* concentrate, the plutocracy mechanism of Section 9 is
false. Current evidence points toward concentration, and there is a formal
impossibility result in this direction `[empirical]`
([*Concave is the New Linear: The Impossibility of Anti-Plutocratic DAO
Governance*, arXiv:2605.18990](https://arxiv.org/pdf/2605.18990)), but the
prediction remains open for structures not yet observed.

## 9. Four structures, and a candidate fifth

The market/plan dichotomy is too small. There are at least four scheduling
structures already documented, and a fifth under construction.

*Market* schedules by decentralized exchange at prices. *Firm* schedules by
internal direction within a transaction-cost boundary. *State* schedules by
territorial authority over standardized categories. The fourth is the *commons*,
and its inclusion rests on Elinor Ostrom's empirical work. Ostrom documented
long-lived common-pool-resource institutions — irrigation systems, fisheries,
forests — that are governed neither by market price nor by central plan nor by
private firm, but by *polycentric* arrangements of the resource users
themselves, and she extracted eight design principles that the durable cases
share and the collapsed cases lack `[empirical]`.
([Ostrom, *Governing the Commons*, Cambridge University Press, 1990; design
principles overview](https://en.wikipedia.org/wiki/Elinor_Ostrom))
The commons is a distinct algorithm with documented conditions for stability, not
a degenerate market or a small state. That is an empirical finding, and it
enlarges the design space from two structures to four.

The candidate fifth is the *protocol*: rules enforced by a shared substrate
rather than by an owner. In a protocol, the scheduling rule is executed by an
infrastructure that no single participant controls, and compliance is a property
of the substrate rather than of an enforcing authority `[speculative]`. The
descriptive question is the mechanism-design one: under what conditions is such a
structure incentive-compatible — that is, when does following the rule remain
each participant's best response without an external enforcer?

Honesty about a structure requires stating where it demonstrably fails, and the
protocol has three documented failure modes. First, *governance capture under
token-weighted voting*: when decision weight is proportional to holdings, decisive
power concentrates, and small holders face a rational incentive to abstain or to
accept side payments because a bad decision costs them little `[empirical]`
([Buterin, "Moving beyond coin voting governance," 2021](https://vitalik.eth.limo/general/2021/08/16/voting3.html);
[impossibility result, arXiv:2605.18990](https://arxiv.org/pdf/2605.18990)).
Second, the *oracle problem*: a substrate that enforces rules deterministically
over its own internal state cannot, by construction, observe the external world;
importing external facts requires a trusted channel, which reintroduces the very
trusted party the structure was meant to remove `[consensus]`
([The blockchain oracle problem, Chainlink](https://chain.link/education-hub/oracle-problem)).
Third, *participation and complexity barriers* that hand effective control to the
technically fluent minority `[empirical]`
([D. Ferreira, "The Myths of Blockchain Governance," *Corporate Governance: An International Review*, 2025](https://onlinelibrary.wiley.com/doi/10.1111/corg.70008)).
A protocol is incentive-compatible only where these three are solved or absent;
where they are present, it degrades toward one of the older four structures.
Stating this is what makes the fifth structure a subject of theory rather than of
advocacy.

## 10. Stability of boundaries, stated as conditions

I will not predict the collapse or persistence of any coordinating structure.
The descriptive statement is about conditions.

A coordination structure's boundary is stable while, for the transactions that
cross it, the internal-coordination advantage it offers exceeds the boundary cost
it imposes (Section 5), and while its scheduling error on its domain stays below
the error of the available alternatives (Section 3). Four quantities are
currently changing those conditions, and I list them as observable trends
without asserting a direction of net effect: the falling cost of communication;
the emergence of agent-mediated coordination that lowers the cost of managing
many simultaneous relationships; increased mobility of capital across boundaries;
and the appearance of protocol-governed commons as a fifth option in the design
space. Each of these changes the terms in the boundary-stability inequality. The
theory does not say which way the inequality tips, because that depends on the
domain's information structure and on which of the protocol failure modes bind.
It says only what to measure to find out.

`[speculative]` My own extension, offered as hypothesis and not conclusion: as
communication cost falls and a credible fifth structure becomes available, the
*number of viable structures per domain* rises, and scheduling migrates toward
whichever structure minimizes the sum of information loss (Section 3) and
coordination cost (Section 5) for that specific domain — producing not a single
winning architecture but a heterogeneous patchwork in which market, firm, state,
commons, and protocol each schedule the domains they fit. This is a prediction of
*fragmentation of scheduling by domain*, and it is checkable: it fails if
scheduling instead consolidates onto a single dominant architecture across
heterogeneous domains.

## 11. What this essay does not claim

It does not claim any structure is better. "Better" is undefined without a
choice of objective, and choosing the objective is exactly the normative act the
essay abstains from. It does not claim the nation-state, or any structure, is
ending; it states the conditions under which a boundary is stable and lists what
is changing those conditions. It does not identify any present government, party,
or leader as a subject of praise or criticism; its historical examples are
factual and cited. And it treats its own most attractive move — the credit-
routing lens — as a rhyme that has to earn each measurement, never as a
derivation that inherits the certainty of backpropagation. Subtraction is the
governing discipline here: a paragraph that was beautiful but added no
falsifiable content has been cut, and the version of the framework that would
have looked rigorous while smuggling in a gradient the domain does not have is
rejected in writing above, with its reason attached.

---

### Sources

- F. A. Hayek, "The Use of Knowledge in Society," *American Economic Review* 35(4):519–530, 1945. https://en.wikipedia.org/wiki/The_Use_of_Knowledge_in_Society · full text: https://oll.libertyfund.org/titles/hayek-the-use-of-knowledge-in-society-1945
- J. C. Scott, *Seeing Like a State*, Yale University Press, 1998. https://en.wikipedia.org/wiki/Seeing_Like_a_State
- R. H. Coase, "The Nature of the Firm," *Economica* 4(16):386–405, 1937. https://en.wikipedia.org/wiki/The_Nature_of_the_Firm
- O. E. Williamson, "Transaction Cost Economics: The Natural Progression" (Nobel lecture, 2009). https://web.pdx.edu/~nwallace/EHP/TCEProgression.pdf
- E. Ostrom, *Governing the Commons*, Cambridge University Press, 1990. https://en.wikipedia.org/wiki/Elinor_Ostrom
- Socialist calculation debate (Mises 1920; Lange 1936–37; Hayek). https://en.wikipedia.org/wiki/Socialist_calculation_debate · J. Persky, "Retrospectives: Lange and von Mises, Large-Scale Enterprises, and the Economic Case for Socialism," *Journal of Economic Perspectives* 5(4):229–236, 1991. https://doi.org/10.1257/jep.5.4.229
- Mechanism design, Nobel Memorial Prize 2007 (Hurwicz, Maskin, Myerson). https://www.nobelprize.org/prizes/economic-sciences/2007/ · https://www.nobelprize.org/uploads/2018/06/myerson-slides.pdf
- Soviet material-balance planning. https://en.wikipedia.org/wiki/Material_balance_planning
- M. Minsky, "Steps Toward Artificial Intelligence," *Proc. IRE*, 1961. http://incompleteideas.net/papers/Minsky60steps.pdf
- D. Rumelhart, G. Hinton, R. Williams, "Learning representations by back-propagating errors," *Nature* 323:533–536, 1986.
- V. Buterin, "Moving beyond coin voting governance," 2021. https://vitalik.eth.limo/general/2021/08/16/voting3.html
- "Concave is the New Linear: The Impossibility of Anti-Plutocratic DAO Governance," arXiv:2605.18990. https://arxiv.org/pdf/2605.18990
- The blockchain oracle problem (Chainlink education hub). https://chain.link/education-hub/oracle-problem
- D. Ferreira, "The Myths of Blockchain Governance," *Corporate Governance: An International Review*, 2025. https://onlinelibrary.wiley.com/doi/10.1111/corg.70008

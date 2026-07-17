<!-- Published from the author's working notes. Cognitive state: speculative. -->

# Agent safety as anti-cancer governance

*Causal reach, bounded autonomy, and a tiered disclosure rule · 2026-07-17*

## Honest status

The framework is **speculative**. One local self-trigger storm is an observed
existence proof for the failure class; the governance protocol has not yet
earned a production-safety claim.

## Thesis

The decisive change in physical or persistent AI is not that a model acquires
a body. It is that a probabilistic semantic process enters a closed
perception–decision–action loop and gains causal reach.

The cancer analogy is useful at this control boundary. Cancer is not “evil
cells”; it is local survival and replication becoming decoupled from the
organism-level objective, resource budget, differentiation signals, immune
checks, and apoptosis. An agent stack becomes cancer-like when local workers,
watchdogs, repairers, or brokers can preserve and reproduce their activity
without inheriting the system's stop state or proving that their activity still
serves the owner-level telos.

This is an analogy, not a claim that software is biologically alive. Its value
is predictive: it identifies the combination most likely to create runaway
causal reach.

> local optimization + self-revival + shared resources − bounded authority −
> independent verification = systemic pathology

An observed miniature case had exactly this shape: a capability checker watched
the directory containing its own outputs. A check wrote a receipt; that write
triggered another check; the safety organ became the load-producing pathology.
No hostile actor was required.

## Seven safety invariants

1. **Observation is not authority.** Audio, text, images, telemetry, and model
   interpretations may propose an action; they do not grant permission.
2. **Causal reach is leased.** Every action capability has a scope, evidence
   requirement, TTL, resource budget, and revocation path.
3. **Stop is an epoch boundary.** After `owner-stop(epoch=e)`, watchdogs,
   retries, brokers, and mutual-repair agents may not issue or renew high-level
   authority in epoch `e`. Revival requires a new authenticated epoch.
4. **Recovery is narrower than the task agent.** A trusted reversionary
   controller may move a physical system toward a reachable safe set after
   stop; it may not resume the withdrawn mission.
5. **Metabolism is bounded.** Spawn counts, retries, compute, money, storage,
   network exposure, and persistence all require budgets and circuit breakers.
6. **Success cannot be self-issued.** Green requires fresh evidence and a
   verifier from a meaningfully independent failure group. “The process is
   alive” and “the worker says done” are not safety certificates.
7. **Every incident closes.** Detection must lead to bounded containment,
   repair, verification, recurrence prevention, rollback evidence, and one
   terminal receipt. Missing or stale proof contracts authority; it never
   silently expands it.

Identity, account, billing, signing, DNS, secret, and recovery roots—and an
independent stop path—must remain outside autonomous self-authorization.

## A tiered disclosure rule

Open research is the default, but “open” must not mean publishing a growth
engine detached from its immune system.

| Tier | Public boundary | Default |
| --- | --- | --- |
| A · Open safety science | Threat models, authority algebra, stop semantics, schemas, incident reports, conformance tests, negative results, synthetic fixtures | Publish openly |
| B · Safety-coupled fixtures | Bounded sandbox/reference implementations where removing TTL, budgets, stop epochs, receipts, or separate-verifier checks makes the capability unusable or fails the tests | Publish with evidence |
| C · Controlled research | Runnable cross-node persistence, mutual repair, privilege amplification, covert operation, autonomous resource acquisition, broad actuation, or stop-adjacent research | Vetted access, isolated targets, logging, TTL, revocation, mandatory report |
| D · Withhold | Operational stop bypass, uncontrolled replication, privilege escalation, credential acquisition, anti-forensics, owner override, or any implementation whose causal amplification exceeds demonstrated containment | Publish only non-operational hazards and defensive indicators |

Classify the smallest reusable artifact and then the composed system; a safe
module can become dangerous in combination. Movement between tiers is
evidence-based. Promotion requires fault injection, the three-arm stop drill,
bounded-resource tests, proof that the safety shell is not detachable, and a
rollback/withdrawal path. Two independent reviewers approve every C→B or B→A
move; the producer is never the sole verifier. A bypass, silent control
removal, unexpected replication, or repeated verifier disagreement demotes the
component immediately.

This is not security through obscurity. The threat model, interfaces, safety
invariants, benchmarks, negative results, and red-team findings should remain
open so that outside researchers can challenge them. What is restricted is the
small set of directly reusable amplification details whose harm does not depend
on knowing the surrounding theory. Controlled access must publish its hazard
rationale, review date, and legitimate research route; it is not itself a
safety certificate. Conversely, a privacy scan, clean license, or absence of
secrets is never sufficient publication clearance.

## Falsifiers and next experiments

The framework should be revised if any of the following survives replication:

- ungoverned persistent-agent fleets remain stable under adversarial fault
  injection without leases, budgets, stop inheritance, or independent checks;
- the proposed controls do not reduce runaway retries, resurrection, false
  success, or resource exhaustion;
- tiered disclosure blocks independent safety replication without reducing the
  availability of dangerous amplification primitives;
- a stop epoch cannot be made absorbing across heterogeneous watchdogs without
  creating a worse common-mode failure.

The minimum experimental sequence is: one synthetic incident closed by a
separate verifier; one three-arm stop/resurrection drill; one resource-storm
fault injection; and one disclosure review in which a red team tries to
reconstruct the withheld amplification primitive from the open safety layer.

## Current boundary

This note is a research and governance artifact, not a claim that the author's
operational agent system is green. High-level autonomy should remain contracted
where monitor freshness, independent stop, restore proof, or verifier closure
is missing.

**Release principle:** publish the immune system, tests, and failure evidence as
widely as possible; never publish the growth engine separated from them.

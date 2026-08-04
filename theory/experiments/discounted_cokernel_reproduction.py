#!/usr/bin/env python3
"""Reproduce the corrected discounted-cokernel result and 2x2 dissociation.

Requires only NumPy. The script writes discounted_cokernel_results.json beside
itself. It is intentionally a finite-graph smoke test, not an RL benchmark.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import permutations
from pathlib import Path

import numpy as np


TOL = 1e-10


def incidence(n_vertices, edges, gamma):
    """(D_gamma phi)_e = phi_tail - gamma*phi_head."""
    operator = np.zeros((len(edges), n_vertices), dtype=float)
    for row, (tail, head) in enumerate(edges):
        operator[row, tail] += 1.0
        operator[row, head] -= gamma
    return operator


def residual(n_vertices, edges, rewards, gamma, weights=None):
    rewards = np.asarray(rewards, dtype=float)
    weights = (
        np.ones(len(edges), dtype=float)
        if weights is None
        else np.asarray(weights, dtype=float)
    )
    operator = incidence(n_vertices, edges, gamma)
    sqrt_w = np.sqrt(weights)
    potential, _, rank, _ = np.linalg.lstsq(
        sqrt_w[:, None] * operator, sqrt_w * rewards, rcond=None
    )
    weight_matrix = np.diag(weights)
    projector = operator @ np.linalg.pinv(
        operator.T @ weight_matrix @ operator
    ) @ operator.T @ weight_matrix
    remainder = rewards - operator @ potential
    norm = float(np.sqrt(np.sum(weights * remainder**2)))
    scale = float(np.sqrt(np.sum(weights * rewards**2)))
    return {
        "rank": int(rank),
        "residual_norm": norm,
        "relative_residual": norm / max(scale, 1e-15),
        "normal_equation_defect": float(
            np.linalg.norm(operator.T @ (weights * remainder))
        ),
        "projector_idempotence_defect": float(
            np.linalg.norm(projector @ projector - projector)
        ),
        "weighted_self_adjoint_defect": float(
            np.linalg.norm(projector.T @ weight_matrix - weight_matrix @ projector)
        ),
        "residual": remainder,
    }


def aggregate(latent_rewards, alias):
    sums, counts = {}, {}
    for state, reward in enumerate(latent_rewards):
        edge = (alias[state], alias[(state + 1) % len(latent_rewards)])
        sums[edge] = sums.get(edge, 0.0) + float(reward)
        counts[edge] = counts.get(edge, 0) + 1
    edges = sorted(sums)
    rewards = np.array([sums[e] / counts[e] for e in edges])
    weights = np.array([counts[e] / len(latent_rewards) for e in edges])
    return edges, rewards, weights


def summarize(values):
    values = np.asarray(values, dtype=float)
    return {
        "n": int(values.size),
        "fraction_nonzero": float(np.mean(values > TOL)),
        "mean_residual_norm": float(np.mean(values)),
        "max_residual_norm": float(np.max(values)),
    }


def monte_carlo(n_trials=3000, gamma=0.9):
    all_norms, filtered_norms, by_edges = [], [], {}
    required = {(0, 1), (1, 2), (2, 0)}
    for trial in range(n_trials):
        rng = np.random.default_rng(1000 + trial)
        phi = rng.standard_normal(6)
        latent_rewards = np.array(
            [phi[s] - gamma * phi[(s + 1) % 6] for s in range(6)]
        )
        order = rng.permutation(6)
        alias = {
            int(order[0]): 0,
            int(order[1]): 0,
            int(order[2]): 1,
            int(order[3]): 1,
            int(order[4]): 2,
            int(order[5]): 2,
        }
        edges, rewards, weights = aggregate(latent_rewards, alias)
        norm = residual(3, edges, rewards, gamma, weights)["residual_norm"]
        all_norms.append(norm)
        by_edges.setdefault(len(edges), []).append(norm)
        if required.issubset(set(edges)):
            filtered_norms.append(norm)
    return {
        "all_trials": summarize(all_norms),
        "historical_filter": summarize(filtered_norms),
        "by_unique_edge_count": {
            str(k): summarize(v) for k, v in sorted(by_edges.items())
        },
    }


def rational_rank(matrix):
    work = [row[:] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [x / scale for x in work[rank]]
        for row in range(len(work)):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                x - factor * y for x, y in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def exact_alias_count():
    gamma = Fraction(9, 10)
    aliases = sorted(set(permutations((0, 0, 1, 1, 2, 2))))
    latent_operator = []
    for state in range(6):
        row = [Fraction(0) for _ in range(6)]
        row[state] += 1
        row[(state + 1) % 6] -= gamma
        latent_operator.append(row)

    required = {(0, 1), (1, 2), (2, 0)}
    conditioned = nonexact = 0
    by_edges = {}
    for alias in aliases:
        edge_to_latent = {}
        for state in range(6):
            edge = (alias[state], alias[(state + 1) % 6])
            edge_to_latent.setdefault(edge, []).append(state)
        edges = sorted(edge_to_latent)
        if not required.issubset(set(edges)):
            continue
        conditioned += 1
        obs_operator, aggregated_latent_operator = [], []
        for tail, head in edges:
            row = [Fraction(0) for _ in range(3)]
            row[tail] += 1
            row[head] -= gamma
            obs_operator.append(row)
            latent_row = [Fraction(0) for _ in range(6)]
            source_rows = edge_to_latent[(tail, head)]
            for source in source_rows:
                for column, value in enumerate(latent_operator[source]):
                    latent_row[column] += value / len(source_rows)
            aggregated_latent_operator.append(latent_row)
        augmented = [
            obs + latent
            for obs, latent in zip(obs_operator, aggregated_latent_operator)
        ]
        generic_nonexact = rational_rank(augmented) > rational_rank(obs_operator)
        nonexact += int(generic_nonexact)
        bucket = by_edges.setdefault(
            len(edges), {"aliases": 0, "generic_nonexact": 0}
        )
        bucket["aliases"] += 1
        bucket["generic_nonexact"] += int(generic_nonexact)
    return {
        "balanced_alias_maps": len(aliases),
        "conditioned_maps": conditioned,
        "generic_nonexact_maps": nonexact,
        "generic_nonexact_ratio": f"{nonexact}/{conditioned}",
        "fraction_generic_nonexact": nonexact / conditioned,
        "by_unique_edge_count": {
            str(k): v for k, v in sorted(by_edges.items())
        },
    }


def representation_cases(gamma=0.9):
    phi = np.array([0.0, 1.0, -1.0, 2.0, -2.0, 0.5])
    latent_edges = [(s, (s + 1) % 6) for s in range(6)]
    latent_rewards = np.array(
        [phi[s] - gamma * phi[(s + 1) % 6] for s in range(6)]
    )
    cases = {
        "full": residual(6, latent_edges, latent_rewards, gamma),
    }
    aliases = {
        "exact_alias": {0: 0, 1: 1, 2: 2, 3: 0, 4: 1, 5: 2},
        "overconstrained_alias": {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2},
    }
    for name, alias in aliases.items():
        edges, rewards, weights = aggregate(latent_rewards, alias)
        cases[name] = residual(3, edges, rewards, gamma, weights)
    return {
        name: {
            "residual_norm": value["residual_norm"],
            "relative_residual": value["relative_residual"],
        }
        for name, value in cases.items()
    }


def game_cases():
    payoff = np.array([[1.0, -1.0], [-1.0, 1.0]])
    nodes = [(0, 0), (0, 1), (1, 0), (1, 1)]
    index = {node: i for i, node in enumerate(nodes)}
    edges = [
        (index[(0, 0)], index[(1, 0)]),
        (index[(0, 1)], index[(1, 1)]),
        (index[(0, 0)], index[(0, 1)]),
        (index[(1, 0)], index[(1, 1)]),
    ]
    games = {
        "potential": (payoff, payoff),
        "harmonic": (payoff, -payoff),
    }
    out = {}
    for name, (p1, p2) in games.items():
        flow = np.array(
            [
                p1[1, 0] - p1[0, 0],
                p1[1, 1] - p1[0, 1],
                p2[0, 1] - p2[0, 0],
                p2[1, 1] - p2[1, 0],
            ]
        )
        fit = residual(len(nodes), edges, flow, gamma=1.0)
        out[name] = {
            "harmonic_norm": fit["residual_norm"],
            "harmonic_fraction": fit["relative_residual"],
        }
    return out


def main():
    gamma = 0.9
    cycle_edges = [(s, (s + 1) % 5) for s in range(5)]
    cycle_discounted = residual(
        5, cycle_edges, np.array([1.0, -0.3, 2.1, 0.7, -1.4]), gamma
    )
    cycle_undiscounted = residual(
        5, cycle_edges, np.ones(5), gamma=1.0
    )
    representations = representation_cases(gamma)
    games = game_cases()
    ensemble = monte_carlo()
    exact_structure = exact_alias_count()

    # Shaping-invariance and weighted-projector regression on an overdetermined
    # graph. These are definition tests, not statistical checks.
    branch_edges = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 0)]
    branch_rewards = np.array([0.4, -1.1, 0.2, 1.7, -0.8, 0.3])
    branch_weights = np.array([1, 2, 1, 2, 1, 2], dtype=float) / 9.0
    branch = residual(3, branch_edges, branch_rewards, gamma, branch_weights)
    shaping_potential = np.array([0.3, -0.6, 1.2])
    shaped = residual(
        3,
        branch_edges,
        branch_rewards + incidence(3, branch_edges, gamma) @ shaping_potential,
        gamma,
        branch_weights,
    )
    shaping_invariance_defect = float(
        np.linalg.norm(branch["residual"] - shaped["residual"])
    )

    assert cycle_discounted["residual_norm"] < TOL
    assert cycle_undiscounted["residual_norm"] > TOL
    assert representations["full"]["residual_norm"] < TOL
    assert representations["exact_alias"]["residual_norm"] < TOL
    assert representations["overconstrained_alias"]["residual_norm"] > TOL
    assert games["potential"]["harmonic_norm"] < TOL
    assert games["harmonic"]["harmonic_fraction"] > 1.0 - TOL
    assert branch["projector_idempotence_defect"] < TOL
    assert branch["weighted_self_adjoint_defect"] < TOL
    assert branch["normal_equation_defect"] < TOL
    assert shaping_invariance_defect < TOL
    assert exact_structure["balanced_alias_maps"] == 90
    assert exact_structure["conditioned_maps"] == 45
    assert exact_structure["generic_nonexact_maps"] == 42
    assert ensemble["historical_filter"]["n"] == 1484
    assert np.isclose(
        ensemble["historical_filter"]["fraction_nonzero"], 1381 / 1484
    )
    assert ensemble["all_trials"]["n"] == 3000
    assert np.isclose(ensemble["all_trials"]["fraction_nonzero"], 2809 / 3000)

    results = {
        "definition": {
            "operator": "(D_gamma phi)_e = phi_tail - gamma*phi_head",
            "obstruction": "W-orthogonal residual of r modulo im(D_gamma)",
            "tolerance": TOL,
        },
        "simple_cycles": {
            "gamma_0_9": {
                "rank": cycle_discounted["rank"],
                "residual_norm": cycle_discounted["residual_norm"],
            },
            "gamma_1": {
                "rank": cycle_undiscounted["rank"],
                "residual_norm": cycle_undiscounted["residual_norm"],
            },
        },
        "partial_observability": ensemble,
        "exact_alias_structure": exact_structure,
        "operator_regressions": {
            "projector_idempotence_defect": branch[
                "projector_idempotence_defect"
            ],
            "weighted_self_adjoint_defect": branch[
                "weighted_self_adjoint_defect"
            ],
            "normal_equation_defect": branch["normal_equation_defect"],
            "shaping_invariance_defect": shaping_invariance_defect,
        },
        "two_axis_dissociation": {
            "representation": representations,
            "strategic": games,
            "next_test": "perform both targeted repairs in one coupled learner and verify axis selectivity",
        },
    }
    path = Path(__file__).with_name("discounted_cokernel_results.json")
    path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()

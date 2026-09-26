# Agent-based simulation results: ownership rules vs concentration and mission drift

## Reproducibility

- Script: `simulate_company_architecture.py`
- Seeds: `3, 11, 17, 23, 29, 37, 43, 53` (8 runs per scenario)
- Output files:
  - `simulation_outputs/timeseries_by_seed.csv`
  - `simulation_outputs/final_period_by_seed.csv`
  - `simulation_outputs/summary_stats.csv`
  - `charts/gini_over_time.png`
  - `charts/mission_drift_over_time.png`

## Scenarios compared

1. `shareholder_only`
2. `pbc_benefit_duty`
3. `foundation_steward_locked_mission`
4. `cooperative`
5. `shareholder_plus_ai_windfall_rule`

## Metrics

- **Wealth concentration**: Gini coefficient, top-1% wealth share.
- **Mission drift**: mean absolute divergence between firm mission target and simulated period-by-period decision under competitive pressure.
- Summary table reports **mean, standard deviation, and min-max spread across 8 seeds** at the final period (mission drift averaged over the final 10 periods per seed).

## Results table

| scenario | final Gini (mean ± sd) | Gini range | top-1% share (mean ± sd) | top-1% range | mission drift last-10 periods (mean ± sd) | mission drift range |
|---|---:|---:|---:|---:|---:|---:|
| shareholder_only | 0.2335 ± 0.0060 | 0.2233-0.2406 | 0.0501 ± 0.0066 | 0.0404-0.0636 | 0.4111 ± 0.0198 | 0.3817-0.4319 |
| pbc_benefit_duty | 0.2228 ± 0.0059 | 0.2130-0.2303 | 0.0464 ± 0.0059 | 0.0377-0.0585 | 0.2720 ± 0.0146 | 0.2495-0.2891 |
| foundation_steward_locked_mission | 0.2133 ± 0.0060 | 0.2035-0.2211 | 0.0439 ± 0.0055 | 0.0358-0.0551 | 0.1084 ± 0.0060 | 0.1000-0.1155 |
| cooperative | 0.1923 ± 0.0066 | 0.1822-0.2015 | 0.0403 ± 0.0051 | 0.0329-0.0508 | 0.1532 ± 0.0055 | 0.1460-0.1616 |
| shareholder_plus_ai_windfall_rule | 0.2232 ± 0.0064 | 0.2127-0.2313 | 0.0476 ± 0.0063 | 0.0385-0.0605 | 0.4111 ± 0.0198 | 0.3817-0.4319 |

## Charts

![Gini over time by scenario](charts/gini_over_time.png)

![Mission drift over time by scenario](charts/mission_drift_over_time.png)

## What is by-construction vs emergent

### By construction from assumptions

- `shareholder_plus_ai_windfall_rule` has **the same mission drift** as `shareholder_only` because the windfall rule is implemented only as an ex-post redistribution of exceptional profits (it does not alter firm objective weights).
- `foundation_steward_locked_mission` and `cooperative` include mission floors / lock-in constraints, so lower mission drift relative to `shareholder_only` is directly encoded.
- Cooperative concentration is structurally damped because payouts are allocated via labor/patronage shares rather than capital ownership shares.

### Emergent within the toy model

- The relative ranking among concentration outcomes (cooperative < foundation/steward < PBC < shareholder) is generated through the interaction of payout rules, ownership-updating dynamics, and shocks across periods/seeds.
- The size of concentration reduction from the windfall rule (vs shareholder-only) depends on how often returns exceed the windfall threshold in stochastic runs.

## Interpretation limits

- This is a stylized simulation, not causal evidence about real firms.
- Results are sensitive to parameter choices (mission floors, ownership turnover, payout ratios, windfall threshold/tax).
- Use as a futures-thinking sandbox to stress-test governance logic, not as empirical forecasting.

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "outputs" / "cost_curve"


def annuity_factor(rate: float, years: int) -> float:
    if rate == 0:
        return 1 / years
    return rate / (1 - (1 + rate) ** (-years))


def levelized_metrics(option: dict, discount_rate: float, lng_price_usd_mmbtu: float, fx: float, heat_rate: float, gas_om_thb_mwh: float) -> dict:
    capex = float(option["capex_thb_per_kw"])
    om_frac = float(option["fixed_om_fraction_of_capex"])
    life = int(option["lifetime_years"])
    annual_energy = float(option["annual_energy_delta_kwh_per_kw"])
    peak_delta = float(option["evening_peak_delta_kw_per_kw"])

    annualized_capex = capex * annuity_factor(discount_rate, life)
    fixed_om = capex * om_frac
    variable_cost = 0.0

    if option.get("label", "").lower().startswith("new ccgt"):
        fuel_thb_per_mwh = lng_price_usd_mmbtu * heat_rate * fx
        variable_cost = (fuel_thb_per_mwh + gas_om_thb_mwh) * max(annual_energy, 0.0) / 1000.0

    annual_cost = annualized_capex + fixed_om + variable_cost

    if abs(annual_energy) < 1e-9:
        shifted = abs(peak_delta) * 4 * 330
        energy_denominator = shifted
        energy_metric_label = "thb_per_kwh_shifted"
    else:
        energy_denominator = abs(annual_energy)
        energy_metric_label = "thb_per_kwh_saved_or_supplied"

    thb_per_kwh = annual_cost / energy_denominator if energy_denominator > 0 else np.nan
    thb_per_kw_peak = annual_cost / abs(peak_delta) if abs(peak_delta) > 0 else np.nan

    return {
        "annualized_capex_thb_per_kw_year": annualized_capex,
        "fixed_om_thb_per_kw_year": fixed_om,
        "variable_cost_thb_per_kw_year": variable_cost,
        "annual_total_cost_thb_per_kw_year": annual_cost,
        "thb_per_kwh": thb_per_kwh,
        "thb_per_kw_evening_peak_year": thb_per_kw_peak,
        "energy_metric_label": energy_metric_label,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assumptions = yaml.safe_load((REPO_ROOT / "assumptions.yaml").read_text(encoding="utf-8"))

    options = assumptions["cost_curve_options"]
    r = assumptions["macroeconomic"]["real_discount_rate"]["value"]
    fx = assumptions["macroeconomic"]["fx_thb_per_usd"]["value"]
    heat_rate = assumptions["fuel_scenarios"]["ccgt_heat_rate_mmbtu_per_mwh"]["value"]
    gas_om = assumptions["fuel_scenarios"]["gas_variable_om_thb_per_mwh"]["value"]

    potentials_mw = {
        "aircon_retrofit_controls": 2500,
        "building_ems": 1500,
        "rooftop_solar_self_use": 4000,
        "bess_shift": 3000,
        "tou_demand_response": 2000,
        "distribution_loss_reduction": 1200,
        "new_ccgt_lng": 4000,
        "smr": 300,
        "imported_hydro": 2000,
    }

    rows = []
    for key, opt in options.items():
        for scenario_name, scenario in assumptions["fuel_scenarios"]["lng_usd_per_mmbtu"].items():
            metrics = levelized_metrics(opt, r, scenario["value"], fx, heat_rate, gas_om)
            rows.append(
                {
                    "option_key": key,
                    "option_label": opt["label"],
                    "scenario": scenario_name,
                    "lng_usd_mmbtu": scenario["value"],
                    "estimate": opt.get("estimate", True),
                    "source": opt.get("source", ""),
                    "potential_mw": potentials_mw.get(key, np.nan),
                    **metrics,
                }
            )
            if key != "new_ccgt_lng":
                break

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "cost_curve_metrics.csv", index=False)

    base = df[df["scenario"] == "base"].copy().sort_values("thb_per_kwh")
    base["cum_peak_mw"] = base["potential_mw"].cumsum()
    base["start_peak_mw"] = base["cum_peak_mw"] - base["potential_mw"]

    plt.figure(figsize=(12, 6))
    for _, row in base.iterrows():
        plt.bar(
            x=row["start_peak_mw"] + row["potential_mw"] / 2,
            height=row["thb_per_kwh"],
            width=row["potential_mw"],
            edgecolor="black",
            alpha=0.75,
            label=row["option_label"],
        )
    plt.xlabel("Cumulative evening-peak impact potential (MW, screening estimate)")
    plt.ylabel("Levelized cost (THB/kWh saved or supplied)")
    plt.title("Thailand screening supply/savings cost curve (base LNG scenario)")
    handles, labels = plt.gca().get_legend_handles_labels()
    uniq = dict(zip(labels, handles))
    plt.legend(uniq.values(), uniq.keys(), fontsize=8, bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(OUT / "supply_curve_base.png", dpi=180)
    plt.close()

    # LNG sensitivity for new CCGT
    ccgt = df[df["option_key"] == "new_ccgt_lng"].copy()
    plt.figure(figsize=(7, 4))
    plt.plot(ccgt["scenario"], ccgt["thb_per_kwh"], marker="o")
    plt.ylabel("LCOE (THB/kWh)")
    plt.xlabel("LNG price scenario")
    plt.title("New CCGT sensitivity to LNG price")
    plt.tight_layout()
    plt.savefig(OUT / "ccgt_lng_sensitivity.png", dpi=180)
    plt.close()

    print("Wrote cost-curve tables and charts.")


if __name__ == "__main__":
    main()
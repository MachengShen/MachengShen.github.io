from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA = REPO_ROOT / "data" / "processed"
OUT = REPO_ROOT / "outputs" / "hourly"


def build_data_centre_profile(df: pd.DataFrame, target_gw: float, load_factor: float, evening_coincidence: float) -> pd.Series:
    base_mw = target_gw * 1000 * load_factor
    h = df["timestamp"].dt.hour
    # Slight diurnal bump from cooling loads; mostly flat IT demand.
    shape = np.where((h >= 18) & (h <= 22), evening_coincidence, 1.0)
    return pd.Series(base_mw * shape, index=df.index)


def apply_option(df: pd.DataFrame, option_key: str, potential_mw: float) -> pd.Series:
    ts = df["timestamp"]
    h = ts.dt.hour
    demand = df["demand_with_dc_mw"].copy()

    if option_key == "aircon_retrofit_controls":
        profile = np.where((h >= 10) & (h <= 17), 0.03, 0.0) + np.where((h >= 18) & (h <= 22), 0.05, 0.0)
        return demand * (1 - profile)
    if option_key == "building_ems":
        profile = np.where((h >= 8) & (h <= 20), 0.02, 0.0)
        return demand * (1 - profile)
    if option_key == "rooftop_solar_self_use":
        solar_shape = np.maximum(0, np.sin((h - 6) / 12 * np.pi))
        solar_cf = 0.2
        solar_output = potential_mw * (solar_shape / solar_shape.max()) * solar_cf
        return demand - solar_output
    if option_key == "bess_shift":
        shifted = demand.copy()
        charge_hours = (h >= 10) & (h <= 15)
        discharge_hours = (h >= 18) & (h <= 22)
        shifted.loc[charge_hours] = shifted.loc[charge_hours] + 0.18 * potential_mw
        shifted.loc[discharge_hours] = shifted.loc[discharge_hours] - 0.22 * potential_mw
        return shifted
    if option_key == "tou_demand_response":
        shifted = demand.copy()
        evening = (h >= 18) & (h <= 22)
        night = (h >= 0) & (h <= 5)
        shifted.loc[evening] = shifted.loc[evening] - 0.20 * potential_mw
        shifted.loc[night] = shifted.loc[night] + 0.10 * potential_mw
        return shifted
    if option_key == "distribution_loss_reduction":
        return demand * (1 - 0.012)
    if option_key == "new_ccgt_lng":
        residual = demand.copy()
        evening = (h >= 18) & (h <= 22)
        residual.loc[evening] = residual.loc[evening] - potential_mw
        return residual
    if option_key == "smr":
        return demand - 0.90 * potential_mw
    if option_key == "imported_hydro":
        residual = demand.copy()
        evening = (h >= 17) & (h <= 23)
        residual.loc[evening] = residual.loc[evening] - 0.8 * potential_mw
        return residual

    return demand


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assumptions = yaml.safe_load((REPO_ROOT / "assumptions.yaml").read_text(encoding="utf-8"))
    hourly = pd.read_csv(DATA / "hourly_proxy_2024.csv", parse_dates=["timestamp"])
    hourly = hourly.dropna(subset=["timestamp"]).copy()
    hourly.rename(columns={"total_demand_mw": "baseline_demand_mw"}, inplace=True)

    dc_target = assumptions["hourly_model"]["data_centre_peak_2037_gw"]
    dc_lf = assumptions["hourly_model"]["data_centre_load_factor"]["value"]
    dc_peak_coincidence = assumptions["hourly_model"]["data_centre_evening_peak_coincidence"]["value"]

    hourly["data_centre_mw"] = build_data_centre_profile(hourly, dc_target, dc_lf, dc_peak_coincidence)
    hourly["demand_with_dc_mw"] = hourly["baseline_demand_mw"] + hourly["data_centre_mw"]

    evening_mask = hourly["timestamp"].dt.hour.between(18, 22)
    baseline_evening_peak = hourly.loc[evening_mask, "baseline_demand_mw"].max()
    dc_evening_peak = hourly.loc[evening_mask, "demand_with_dc_mw"].max()

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

    effects = []
    traces = {"baseline": hourly["baseline_demand_mw"], "with_dc": hourly["demand_with_dc_mw"]}
    for key, potential in potentials_mw.items():
        adjusted = apply_option(hourly, key, potential)
        adjusted_evening_peak = adjusted.loc[evening_mask].max()
        effects.append(
            {
                "option_key": key,
                "potential_mw": potential,
                "baseline_evening_peak_mw": baseline_evening_peak,
                "dc_evening_peak_mw": dc_evening_peak,
                "post_option_evening_peak_mw": adjusted_evening_peak,
                "peak_reduction_vs_dc_mw": dc_evening_peak - adjusted_evening_peak,
            }
        )
        traces[key] = adjusted

    effects_df = pd.DataFrame(effects).sort_values("peak_reduction_vs_dc_mw", ascending=False)
    effects_df.to_csv(OUT / "option_effects_evening_peak.csv", index=False)

    # Save representative hourly outputs for top 3 options.
    top_keys = effects_df.head(3)["option_key"].tolist()
    export = pd.DataFrame({"timestamp": hourly["timestamp"], "baseline_mw": traces["baseline"], "with_dc_mw": traces["with_dc"]})
    for key in top_keys:
        export[f"{key}_mw"] = traces[key]
    export.to_csv(OUT / "hourly_residual_load_top_options.csv", index=False)

    # Plot one representative peak week.
    peak_idx = hourly["demand_with_dc_mw"].idxmax()
    start = max(0, peak_idx - 24 * 3)
    end = min(len(hourly), peak_idx + 24 * 4)
    x = hourly["timestamp"].iloc[start:end]

    plt.figure(figsize=(13, 6))
    plt.plot(x, traces["baseline"].iloc[start:end], label="Baseline 2024 demand")
    plt.plot(x, traces["with_dc"].iloc[start:end], label="With data-centre growth (8.8 GW high case)")
    for key in top_keys:
        plt.plot(x, traces[key].iloc[start:end], label=f"With {key}")
    plt.ylabel("MW")
    plt.title("Representative peak-week residual load (screening model)")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "residual_load_peak_week.png", dpi=180)
    plt.close()

    summary = pd.DataFrame(
        [
            {"metric": "baseline_evening_peak_mw", "value": baseline_evening_peak},
            {"metric": "with_data_centre_evening_peak_mw", "value": dc_evening_peak},
            {"metric": "data_centre_increment_mw", "value": dc_evening_peak - baseline_evening_peak},
        ]
    )
    summary.to_csv(OUT / "hourly_model_summary.csv", index=False)
    print("Wrote hourly model outputs.")


if __name__ == "__main__":
    main()
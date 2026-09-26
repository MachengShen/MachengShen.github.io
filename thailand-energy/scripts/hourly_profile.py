"""Hourly evening-peak check for Thailand (EGAT system), 2023-2024.

Data: Bunnak, P. (2025) "Thai Power System: Hourly Power Generation, Demand,
and Cross-Border Flows", Zenodo record 17109911, CC-BY-4.0 (collected from
EGAT's public website). Files: data/system_2023.csv, data/system_2024.csv.

Outputs:
  data/hourly_mean_profile.csv   mean demand by hour (all year, April)
  data/peak_day_2024.csv         hourly demand on the 2024 peak day
  data/daily_peak_hour_counts.csv hour at which each day's peak occurred
  assets/evening_peak_2024.svg    chart used on the website

The "illustrative" line subtracts the independent reviewers' screening
estimates (AC efficiency ~2,150 MW over 18:00-23:59, storage ~660 MW over 18:00-22:59).
Those two numbers are unverified screening estimates, not measurements.
Run:  python scripts/hourly_profile.py   (needs pandas)
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D, A = ROOT / "data", ROOT / "assets"
AC_MW, BESS_MW = 2150, 660  # reviewer screening estimates (unverified)


def load(year):
    d = pd.read_csv(D / f"system_{year}.csv")
    d["total_demand_mw"] = d[[c for c in d.columns if c.endswith("_demand")]].sum(axis=1)
    d["ts"] = pd.to_datetime(d["datetime"], format="%d/%m/%Y %H:%M")
    d["hour"] = d["ts"].dt.round("h").dt.hour
    d = d[d["ts"].dt.year == year]
    return d


def main():
    prof, counts = [], []
    for y in (2023, 2024):
        d = load(y)
        prof.append(d.groupby("hour")["total_demand_mw"].mean().rename(f"mean_{y}"))
        prof.append(d[d.ts.dt.month == 4].groupby("hour")["total_demand_mw"].mean().rename(f"april_mean_{y}"))
        pk = d.loc[d.groupby(d.ts.dt.date)["total_demand_mw"].idxmax()]
        counts.append(pk["hour"].value_counts().sort_index().rename(f"days_{y}"))
        if y == 2024:
            peak_date = d.loc[d["total_demand_mw"].idxmax(), "ts"].date()
            day = d[d.ts.dt.date == peak_date].groupby("hour")["total_demand_mw"].mean()
    p = pd.concat(prof, axis=1).round(0)
    p.to_csv(D / "hourly_mean_profile.csv", index_label="hour")
    c = pd.concat(counts, axis=1).fillna(0).astype(int).sort_index()
    c.to_csv(D / "daily_peak_hour_counts.csv", index_label="hour_of_daily_peak")
    hrs = day.index.to_series()
    # AC saving assumed to apply 18:00-23:59 (AC keeps running late); storage discharges 18:00-22:59.
    illus = day - hrs.between(18, 23).astype(int) * AC_MW - hrs.between(18, 22).astype(int) * BESS_MW
    print("illustrative new peak", illus.max(), "at hour", illus.idxmax(), "reduction", round(day.max() - illus.max()))
    pdf = pd.DataFrame({"demand_mw": day.round(0), "illustrative_minus_reviewer_AC_and_storage_mw": illus.round(0)})
    pdf.to_csv(D / "peak_day_2024.csv", index_label="hour")
    share = c.loc[19:21].sum() / c.sum()
    print("peak day", peak_date, "max", day.max(), "share of days peaking 19-21h", share.round(3).to_dict())
    svg(day, illus, p["april_mean_2024"], p["mean_2024"], str(peak_date))
    zh = (A / "evening_peak_2024.svg").read_text(encoding="utf-8")
    for en, cn in [("solar hours", "光伏出力时段"), ("evening peak", "晚高峰"), (f"Peak day {peak_date}", f"峰值日 {peak_date}"),
                   ("April 2024 avg", "2024年4月平均"), ("2024 annual avg", "2024年全年平均"), ("Peak day, illustrative AC+storage cut", "峰值日：示意扣减空调+储能")]:
        zh = zh.replace(">" + en + "<", ">" + cn + "<")
    (A / "evening_peak_2024.zh.svg").write_text(zh, encoding="utf-8")


def svg(day, illus, apr, yr, peak_date):
    W, H, L, R, T, B = 760, 380, 60, 20, 30, 50
    ymin, ymax = 15000, 37000
    x = lambda h: L + (W - L - R) * h / 23
    y = lambda v: T + (H - T - B) * (1 - (v - ymin) / (ymax - ymin))
    def path(s):
        return " ".join(f"{'M' if i == 0 else 'L'}{x(h):.1f},{y(v):.1f}" for i, (h, v) in enumerate(s.items()))
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Thailand EGAT-system hourly demand 2024" font-family="system-ui,sans-serif" font-size="12">']
    o.append(f'<rect x="{x(6):.1f}" y="{T}" width="{x(18)-x(6):.1f}" height="{H-T-B}" fill="#fff6d6"/>')
    o.append(f'<text x="{x(12):.1f}" y="{T+14}" text-anchor="middle" fill="#9a7b00">solar hours</text>')
    o.append(f'<rect x="{x(18.5):.1f}" y="{T}" width="{x(22)-x(18.5):.1f}" height="{H-T-B}" fill="#fde2e2"/>')
    o.append(f'<text x="{x(20.25):.1f}" y="{T+14}" text-anchor="middle" fill="#a33">evening peak</text>')
    for v in range(15000, 37001, 5000):
        o.append(f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="#ddd"/><text x="{L-6}" y="{y(v)+4:.1f}" text-anchor="end">{v//1000} GW</text>')
    for h in range(0, 24, 3):
        o.append(f'<text x="{x(h):.1f}" y="{H-B+18}" text-anchor="middle">{h:02d}:00</text>')
    o.append(f'<path d="{path(yr)}" fill="none" stroke="#888" stroke-width="2"/>')
    o.append(f'<path d="{path(apr)}" fill="none" stroke="#1f6fb2" stroke-width="2"/>')
    o.append(f'<path d="{path(day)}" fill="none" stroke="#c0392b" stroke-width="3"/>')
    o.append(f'<path d="{path(illus)}" fill="none" stroke="#2e8b57" stroke-width="2" stroke-dasharray="6 4"/>')
    lg = [("#c0392b", f"Peak day {peak_date}"), ("#1f6fb2", "April 2024 avg"), ("#888", "2024 annual avg"), ("#2e8b57", "Peak day, illustrative AC+storage cut")]
    for xo, (col, t) in zip((10, 170, 290, 410), lg):
        o.append(f'<line x1="{xo}" x2="{xo + 18}" y1="{H-8}" y2="{H-8}" stroke="{col}" stroke-width="3"/><text x="{xo + 22}" y="{H-4}" font-size="10">{t}</text>')
    o.append("</svg>")
    (A / "evening_peak_2024.svg").write_text("\n".join(o), encoding="utf-8")


if __name__ == "__main__":
    main()

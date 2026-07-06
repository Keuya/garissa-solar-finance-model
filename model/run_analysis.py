"""Run scenarios + sensitivities and write outputs/ (CSV + charts).

Usage:  python -m model.run_analysis
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from .assumptions import BASE, SCENARIOS
from .engine import build_cashflows, metrics

OUT = os.path.join(os.path.dirname(__file__), "..", "outputs")


def scenario_table() -> pd.DataFrame:
    return pd.DataFrame({name: metrics(a) for name, a in SCENARIOS.items()})


def sensitivity_table() -> pd.DataFrame:
    """One-way sensitivities on equity IRR around the base case."""
    shocks = {
        "Tariff -10% / +10%": [BASE.scale(tariff_usd_kwh=BASE.tariff_usd_kwh * m) for m in (0.9, 1.1)],
        "Yield P90 / P10 (-7% / +7%)": [BASE.scale(p50_yield_mwh=BASE.p50_yield_mwh * m) for m in (0.93, 1.07)],
        "CAPEX +15% / -15%": [BASE.scale(capex_usd=BASE.capex_usd * m) for m in (1.15, 0.85)],
        "Interest +150bps / -150bps": [BASE.scale(interest_rate=BASE.interest_rate + d) for d in (0.015, -0.015)],
        "OPEX +20% / -20%": [BASE.scale(opex_usd_yr1=BASE.opex_usd_yr1 * m) for m in (1.2, 0.8)],
    }
    rows = {
        label: [metrics(lo)["Equity IRR"], metrics(hi)["Equity IRR"]]
        for label, (lo, hi) in shocks.items()
    }
    return pd.DataFrame(rows, index=["low", "high"]).T


def main() -> None:
    os.makedirs(OUT, exist_ok=True)

    scen = scenario_table()
    scen.to_csv(os.path.join(OUT, "scenario_summary.csv"))
    print(scen.round(3).to_string())

    df = build_cashflows(BASE)
    df.round(0).to_csv(os.path.join(OUT, "base_case_cashflows.csv"), index=False)

    # DSCR profile
    fig, ax1 = plt.subplots(figsize=(9, 5))
    ds = df[df["debt_service"] > 0]
    ax1.bar(ds["year"], ds["cfads"] / 1e6, color="#f4b942", label="CFADS")
    ax1.bar(ds["year"], -ds["debt_service"] / 1e6, color="#2b6cb0", label="Debt service")
    ax1.set_xlabel("Year"), ax1.set_ylabel("USD m")
    ax2 = ax1.twinx()
    ax2.plot(ds["year"], ds["cfads"] / ds["debt_service"], "k--o", ms=4, label="DSCR")
    ax2.axhline(1.30, color="red", lw=1, ls=":")
    ax2.set_ylabel("DSCR (x)")
    ax1.legend(loc="upper left"), ax2.legend(loc="upper right")
    ax1.set_title("Garissa 10 MW — CFADS vs debt service (base case)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "dscr_profile.png"), dpi=150)

    # Equity IRR tornado
    sens = sensitivity_table()
    base_irr = metrics(BASE)["Equity IRR"]
    sens.to_csv(os.path.join(OUT, "sensitivity_equity_irr.csv"))
    order = (sens["high"] - sens["low"]).abs().sort_values().index
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for i, label in enumerate(order):
        lo, hi = sens.loc[label]
        ax.barh(i, (hi - lo) * 100, left=lo * 100, color="#2b6cb0", alpha=0.8)
    ax.axvline(base_irr * 100, color="black", lw=1.2)
    ax.set_yticks(range(len(order))), ax.set_yticklabels(order)
    ax.set_xlabel("Equity IRR (%)")
    ax.set_title(f"Equity IRR sensitivity (base = {base_irr:.1%})")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "tornado_equity_irr.png"), dpi=150)

    print("\nSensitivities (equity IRR):")
    print((sens * 100).round(1).to_string())


if __name__ == "__main__":
    main()

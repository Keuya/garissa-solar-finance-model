"""Cashflow engine: builds the annual project cashflows and lender metrics."""

import numpy as np
import numpy_financial as npf
import pandas as pd

from .assumptions import Assumptions


def annuity_payment(principal: float, rate: float, tenor: int) -> float:
    if principal <= 0:
        return 0.0
    return principal * rate / (1 - (1 + rate) ** -tenor)


def build_cashflows(a: Assumptions) -> pd.DataFrame:
    yrs = np.arange(1, a.project_life_yrs + 1)

    energy = a.p50_yield_mwh * a.availability * (1 - a.degradation) ** (yrs - 1)
    revenue = energy * 1_000 * a.tariff_usd_kwh * (1 + a.tariff_escalation) ** (yrs - 1)
    opex = a.opex_usd_yr1 * (1 + a.opex_escalation) ** (yrs - 1)
    ebitda = revenue - opex

    # Tax: straight-line depreciation, no loss carry-forward modelling beyond
    # clipping taxable income at zero (conservative on timing, fine at this level).
    depreciation = np.where(yrs <= a.depreciation_yrs, a.capex_usd / a.depreciation_yrs, 0.0)

    debt = a.capex_usd * a.gearing
    equity = a.capex_usd - debt
    ds = annuity_payment(debt, a.interest_rate, a.debt_tenor_yrs)

    balance, interest, principal = debt, [], []
    for y in yrs:
        if y <= a.debt_tenor_yrs and balance > 1e-6:
            i = balance * a.interest_rate
            p = min(ds - i, balance)
            balance -= p
        else:
            i, p = 0.0, 0.0
        interest.append(i)
        principal.append(p)
    interest, principal = np.array(interest), np.array(principal)
    debt_service = interest + principal

    taxable = np.maximum(ebitda - depreciation - interest, 0.0)
    tax = taxable * a.tax_rate

    cfads = ebitda - tax
    equity_cf = cfads - debt_service

    df = pd.DataFrame({
        "year": yrs, "energy_mwh": energy, "revenue": revenue, "opex": opex,
        "ebitda": ebitda, "tax": tax, "cfads": cfads, "interest": interest,
        "principal": principal, "debt_service": debt_service, "equity_cf": equity_cf,
    })
    df.attrs.update(debt=debt, equity=equity)
    return df


def metrics(a: Assumptions) -> dict:
    df = build_cashflows(a)
    debt, equity = df.attrs["debt"], df.attrs["equity"]
    r = a.discount_rate

    disc = (1 + r) ** -df["year"].to_numpy()
    npv = float(df["cfads"] @ disc - a.capex_usd)
    project_irr = float(npf.irr(np.concatenate(([-a.capex_usd], df["cfads"]))))
    equity_irr = float(npf.irr(np.concatenate(([-equity], df["equity_cf"]))))

    ds_mask = df["debt_service"] > 0
    dscr = df.loc[ds_mask, "cfads"] / df.loc[ds_mask, "debt_service"]
    llcr_pv = float((df.loc[ds_mask, "cfads"] * (1 + a.interest_rate) ** -df.loc[ds_mask, "year"]).sum())
    llcr = llcr_pv / debt if debt > 0 else float("nan")

    cum = df["equity_cf"].cumsum()
    paid = cum[cum >= equity]
    payback = float(df.loc[paid.index[0], "year"]) if len(paid) else float("nan")

    # Real LCOE: discount energy and costs at the real rate implied by USD CPI.
    real_r = (1 + r) / (1 + 0.025) - 1
    dreal = (1 + real_r) ** -df["year"].to_numpy()
    lcoe = float((a.capex_usd + (df["opex"] * dreal).sum()) / ((df["energy_mwh"] * 1_000 * dreal).sum()))

    return {
        "Project IRR (post-tax)": project_irr,
        "Equity IRR": equity_irr,
        "NPV @ 10% (USD m)": npv / 1e6,
        "Min DSCR": float(dscr.min()),
        "Avg DSCR": float(dscr.mean()),
        "LLCR": llcr,
        "Equity payback (yrs)": payback,
        "LCOE (USD/kWh, real)": lcoe,
        "Debt (USD m)": debt / 1e6,
        "Equity (USD m)": equity / 1e6,
    }

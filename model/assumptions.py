"""Assumptions register for the Garissa Solar PV project finance model.

Every input a lender's technical or financial advisor would ask about lives
here, with its source noted. The base case is anchored to the original Excel
model (Garissa Solar Model.xlsx); the debt, tax and degradation layers are
new and follow typical East-African utility-scale solar terms.
"""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Assumptions:
    # --- Technical -------------------------------------------------------
    capacity_mw: float = 10.0            # Excel: total project size
    p50_yield_mwh: float = 15_945.0      # Excel: year-1 net energy (17.9% NCF)
    degradation: float = 0.005           # 0.5%/yr linear, panel warranty level
    availability: float = 0.99           # contractual O&M availability
    project_life_yrs: int = 25           # PPA tenor = project life

    # --- Revenue ---------------------------------------------------------
    tariff_usd_kwh: float = 0.12         # Excel: USD-denominated PPA, flat
    tariff_escalation: float = 0.0       # flat tariff (no indexation)

    # --- Costs -----------------------------------------------------------
    capex_usd: float = 7_270_000.0       # Excel build-up: $0.727/W
    opex_usd_yr1: float = 350_700.0      # Excel: O&M + labour + lease + contingency
    opex_escalation: float = 0.025       # USD CPI (Excel used 5% KES inflation;
                                         # USD PPA cashflows escalate at USD CPI)

    # --- Debt (new layer, typical DFI terms for EA solar) ----------------
    gearing: float = 0.70                # senior debt / total costs
    interest_rate: float = 0.09          # all-in USD fixed (SOFR swap + ~450bps)
    debt_tenor_yrs: int = 15             # door-to-door, annuity repayment

    # --- Tax (Kenya, simplified) ------------------------------------------
    tax_rate: float = 0.30               # corporate income tax
    depreciation_yrs: int = 20           # straight-line, simplification of
                                         # Kenya investment-deduction rules

    # --- Valuation --------------------------------------------------------
    discount_rate: float = 0.10          # nominal WACC proxy (Excel: 10%)

    def scale(self, **changes) -> "Assumptions":
        """Return a copy with the given fields replaced."""
        return replace(self, **changes)


BASE = Assumptions()

# Downside: P90 yield, tariff renegotiated down, CAPEX overrun, costlier debt.
DOWNSIDE = BASE.scale(
    p50_yield_mwh=BASE.p50_yield_mwh * 0.93,   # P50->P90 (~7% haircut)
    tariff_usd_kwh=0.10,
    capex_usd=BASE.capex_usd * 1.15,
    opex_escalation=0.04,
    interest_rate=0.105,
)

# Upside: strong irradiance year-1 basis, EPC competition, cheaper DFI debt.
UPSIDE = BASE.scale(
    p50_yield_mwh=BASE.p50_yield_mwh * 1.03,
    capex_usd=BASE.capex_usd * 0.92,
    interest_rate=0.075,
)

SCENARIOS = {"Base": BASE, "Downside": DOWNSIDE, "Upside": UPSIDE}

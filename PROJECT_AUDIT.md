# Project Audit — Garissa Solar Finance Model

## What this repository appears to contain
This repository is framed as a combined engineering and financial model for the Garissa Solar Project, linking technical assumptions to bankability outcomes such as IRR, NPV, and DSCR.

## Current strengths
- This is one of the strongest themes in your GitHub portfolio.
- It matches your background and career direction very well.
- It already signals the right blend of engineering and finance.

## What is likely missing or underdeveloped
- The repository would be stronger if it moved from a conceptual finance model to a more lender-style structure.
- The README is good, but the project likely needs clearer assumptions, outputs, and scenario logic.
- It should say more explicitly how the model handles emerging-market realities.

## How to improve the next version
1. Add an **assumptions register** covering tariff, degradation, yield, CAPEX, OPEX, debt terms, tax, inflation, FX, and curtailment.
2. Add **base / downside / upside** cases.
3. Show key outputs clearly:
   - project IRR,
   - equity IRR,
   - DSCR,
   - payback,
   - LCOE.
4. Add a **Kenya-specific risk layer** covering offtaker risk, payment delays, FX exposure, and transmission constraints.
5. Include an optional **battery storage case** and test whether it improves value under time-of-day pricing or curtailment risk.
6. Add a short **investment memo** explaining what would make the project financeable or not.

## Best way to align this project with your background
This should become your signature repository.
It is the clearest bridge between renewable energy engineering and project finance, which is where your profile is strongest.

## Energy-sector problems this project can speak to
- Bankability of utility-scale solar in emerging markets
- Offtaker and payment-risk concerns
- Sensitivity of returns to technical assumptions
- Storage integration and value capture
- Infrastructure finance for African power projects

## Suggested repository structure for the next version
```text
/docs
  project-brief.md
  assumptions-register.md
  investment-memo.md
/data
  raw/
  processed/
/models
  finance-model/
  generation-model/
/results
  charts/
  tables/
/notebooks
```

## Priority next deliverable
Create a short note titled:
**"Would This Project Pass First-Cut Credit Review? Garissa Solar Through a Lender Lens"**

That would immediately make the repository more credible for project finance and energy strategy audiences.

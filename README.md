# Create the repo scaffold and files for Felix to download and use on GitHub
import os, textwrap, json, pathlib

base = "/mnt/data/Garissa-Solar-Finance-Model"
os.makedirs(base, exist_ok=True)
os.makedirs(f"{base}/data", exist_ok=True)
os.makedirs(f"{base}/docs", exist_ok=True)
os.makedirs(f"{base}/visuals", exist_ok=True)

readme = """# Garissa Solar Finance Model 🌞

This repository contains a **financial + engineering model** for the Garissa Solar Project in Kenya.  
It explores how project design choices (capacity, efficiency, degradation, tariffs) influence **IRR, NPV, DSCR, and bankability** in emerging market contexts.

## 🔧 Key Features
- PV generation and capacity factor analysis
- Cashflow modeling (NPV, IRR, DSCR)
- Sensitivity to efficiency losses, tariff shifts, WACC, and financing terms
- Focused on **electricity markets in emerging economies**

## 📊 Why This Matters
Small engineering assumptions ripple into big financial outcomes.  
This model demonstrates:
- How efficiency links to project bankability  
- How PV can support cooling demand and peak load relief  
- Why integrating finance + engineering is critical for Africa’s energy transition  

## 🤝 Collaboration
I’m open to collaborating on:
- Improving modeling methods (Python/R integration, automation)
- Benchmarking PV projects across African and global markets
- Exploring use cases with **DFIs, investors, and developers**

If our interests align, feel free to fork, open an issue, or reach out. Let’s build impactful solutions together. 🚀

## 📁 Structure
Garissa-Solar-Finance-Model/
├── README.md
├── LICENSE
├── .gitignore
├── data/
│ └── Garissa_Solar_Model.xlsx
├── docs/
│ └── methodology.md
└── visuals/
└── charts.png


## 📄 License
MIT License — free to use and adapt with attribution.
"""

methodology = """# Methodology & Assumptions

This document summarizes **assumptions, equations, and data sources** used in the Garissa Solar Finance Model.

## 1) Project Context
- **Location:** Garissa County, Kenya
- **Technology:** Utility-scale Solar PV (option to pair with BESS)
- **Use Case:** Assess how design & financing choices affect IRR/NPV/DSCR in an emerging-market grid context.

## 2) Technical Assumptions
- **Installed Capacity (MWp):** *<set in model>*
- **Capacity Factor (%):** Derived from irradiance and losses (soiling, temperature, wiring); default *<e.g., 20–24%>*.
- **Degradation:** *<e.g., 0.5–0.8%/year>*
- **Availability/Uptime:** *<e.g., 98–99.5%>*
- **Losses:** Soiling, inverter, temperature; combined loss factor *<enter value>*.
- **Cooling Link (optional):** If modeling PV vs. AC load, align hourly PV output with cooling demand profile.

**Energy Yield**
\\[ \\text{Annual MWh} = P_{\\text{MWp}} \\times 8760 \\times CF \\times (1 - d)^{t} \\]
where *d* is annual degradation and *t* is year index.

## 3) Cost & Financing
- **CAPEX (USD/kWp):** *<enter>*
- **OPEX (USD/kW-yr or % CAPEX):** *<enter>*
- **Debt/Equity Split:** *<e.g., 70/30>*
- **Cost of Debt (post-tax):** *<enter>%*
- **Equity Hurdle/Expected Return:** *<enter>%*
- **WACC:** Weighted by D/E and costs.

**WACC**
\\[ \\text{WACC} = \\frac{E}{D+E} r_e + \\frac{D}{D+E} r_d (1-T) \\]

## 4) Revenue & Tariffs
- **PPA / Tariff (USD/MWh):** *<enter>*
- **Indexation:** *<e.g., CPI, FX>*
- **Merchant Share (if any):** *<enter>%*
- **Curtailment:** *<enter>% (if applicable)*

**Revenue**
\\[ \\text{Revenue}_t = \\text{Tariff}_t \\times \\text{MWh}_t \\times (1 - \\text{curtailment}) \\]

## 5) Cash Flow Mechanics
- **Depreciation:** Straight-line or tax rules per Kenya regulations (adjustable).
- **Tax Rate:** *<enter current corporate tax rate>*
- **Working Capital:** If applicable.
- **Decommissioning/Residual:** *<enter>*

**NPV**
\\[ \\text{NPV} = \\sum_{t=0}^{N} \\frac{FCF_t}{(1+WACC)^t} \\]

**IRR**
\\[ \\text{IRR}: \\text{discount rate s.t. } NPV=0 \\]

**DSCR**
\\[ \\text{DSCR}_t = \\frac{CFADS_t}{Debt\\ Service_t} \\]

## 6) Sensitivities
- **Efficiency Loss:** e.g., −2% absolute efficiency → revenue & IRR impact.
- **Tariff/Shocks:** ±X% tariff; time-of-day effects if applicable.
- **WACC / Cost of Debt:** ±X% points.
- **CAPEX/OPEX:** ±X%.
- **Degradation Rate:** ±X% points.

Visualize with tornado charts and IRR curves in `/visuals`.

## 7) Data Sources (examples)
- Solar resource: Global Solar Atlas / PVGIS.
- Tariffs/market: Kenya EPRA publications or PPA assumptions.
- Costs: Industry reports/vendor quotes.
- Policy: Kenyan energy acts/regulations.

## 8) How to Reproduce
1. Open `data/Garissa_Solar_Model.xlsx`.
2. Set assumptions in the Inputs tab (capacity, CF, CAPEX, OPEX, D/E, WACC, tariff).
3. Review outputs: IRR, NPV, DSCR, Sensitivities.
4. Export charts to `/visuals`.
5. (Optional) Port logic to Python/R for automation & scenario runs.

## 9) Collaboration
Issues and PRs welcome. Suggested extensions:
- Hourly PV vs. cooling load modeling.
- Storage pairing + arbitrage/peak shaving.
- DFI-aligned bankability reporting.
"""

license_text = """MIT License

Copyright (c) 2025 Felix

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the \"Software\"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

gitignore = """# OS
.DS_Store
Thumbs.db

# Python/R notebooks (if added later)
.ipynb_checkpoints/
.Rproj.user/

# Build/exports
__pycache__/
*.pyc
*.Rhistory
*.RData

# Excel temp files
~$*.xlsx
"""

# Write files
with open(f"{base}/README.md","w") as f: f.write(readme)
with open(f"{base}/docs/methodology.md","w") as f: f.write(methodology)
with open(f"{base}/LICENSE","w") as f: f.write(license_text)
with open(f"{base}/.gitignore","w") as f: f.write(gitignore)

# Create a tiny placeholder PNG for visuals/charts.png
from PIL import Image, ImageDraw, ImageFont
img = Image.new("RGB",(1200,630),"white")
draw = ImageDraw.Draw(img)
text = "Place your IRR / Sensitivity charts here"
draw.text((50, 280), text, fill="black")
img_path = f"{base}/visuals/charts.png"
img.save(img_path)

# Create a ZIP for convenient download
import zipfile, io
zip_path = "/mnt/data/Garissa-Solar-Finance-Model.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(base):
        for name in files:
            p = os.path.join(root, name)
            z.write(p, arcname=os.path.relpath(p, base))

zip_path

# Health Financing & UHC

Prototype notebooks and data workflows for **AI/ML applications in health financing**, universal health coverage (UHC), and fiscal equity—aimed at policy-facing explainability (including SHAP) rather than clinical prediction.

**Flagship demo:** [Codes/Project11.ipynb](Codes/Project11.ipynb) — Fiscal Equity Index with a **simulated district** workflow and a **UNICEF SDMX country panel** (`src/fiscal_equity.py`).

## Repository layout

| Path                                        | Description                                                        |
| ------------------------------------------- | ------------------------------------------------------------------ |
| [Codes/](Codes/)                             | Fifteen project notebooks + SHAP tutorials                         |
| [datasets/](datasets/)                       | UNICEF (`unicefdata`) and GHEC exploration; cached SDMX metadata |
| [src/fiscal_equity.py](src/fiscal_equity.py) | Reusable Fiscal Equity Index + UNICEF fetch helpers                |
| [Paper/](Paper/), [Reports/](Reports/)        | Local reference PDFs (verify rights before redistributing)         |
| Root`.docx` files                         | Manuscript / scoping notes (optional to keep private)              |

## Projects index

| #  | Title                                               | Status                                         |
| -- | --------------------------------------------------- | ---------------------------------------------- |
| 1  | AI-Driven National Health Budget Simulator          | Prototype (simulated)                          |
| 2  | Catastrophic Health Spending (CHS) Risk Predictor   | Prototype                                      |
| 3  | NHIS Claims Fraud Detection                         | Prototype                                      |
| 4  | Automated Cost-Effectiveness Analysis (CEA) Engine  | Prototype                                      |
| 5  | Predictive Funding Gap Alerts (chronic disease)     | Prototype                                      |
| 6  | AI-Mediated Pooled Procurement (regional medicines) | Prototype                                      |
| 7  | Value-Based Health Care (VBHC) Performance Monitor  | Prototype                                      |
| 8  | Informal-Sector Insurance Enrollment Expansion      | Prototype                                      |
| 9  | Pandemic Fiscal Preparedness Index                  | Prototype                                      |
| 10 | Dynamic Risk Adjustment for Insurance Risk Pools    | Prototype (XGBoost + SHAP)                     |
| 11 | **Fiscal Equity Index for UHC**               | **Flagship** — simulation + UNICEF data |
| 12 | Hospital Solvency Early-Warning System              | Stub                                           |
| 13 | CHW Attrition Risk Predictor                        | Stub                                           |
| 14 | Preventive Program Impact Evaluation (causal sim)   | Stub                                           |
| 15 | Health-Financing Litigation Risk Index              | Stub                                           |

Supporting notebooks: `Commontools.ipynb`, `shap_practice.ipynb`, `shap2.ipynb`.

## Setup

**Conda (recommended)**

```bash
conda env create -f environment.yml
conda activate ai-health-financing
jupyter lab
```

**pip**

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
jupyter lab
```

Open notebooks from `Codes/`. For Project 11, run cells top-to-bottom; the UNICEF section needs internet access.

## Publish to GitHub

From the repository root (after [Git](https://git-scm.com/) is installed):

```bash
git init -b main
git add .
git commit -m "Initial public release: health financing AI prototypes"
```

Create an empty repository on GitHub (e.g. `ai-health-financing`), then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-health-financing.git
git push -u origin main
```

Optional maintenance (strip notebook outputs before commit):

```bash
python scripts/prepare_repo.py
```

## Data sources

- [unicefdata](https://pypi.org/project/unicefdata/) — UNICEF SDG indicators via SDMX ([datasets/unicefdataset.ipynb](datasets/unicefdataset.ipynb))
- [GHEC](https://ghec-dashboard.onrender.com/) — cross-country panels ([datasets/GHEC.ipynb](datasets/GHEC.ipynb))

## License

MIT — see [LICENSE](LICENSE). Reference PDFs in `Paper/` and `Reports/` are not covered by this license; retain your own copies and citation rights.

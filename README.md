# End-to-End Insurance Pricing Simulation & Optimisation

## Project Overview

This project implements a fully parameterized, end-to-end pricing engine for a synthetic health insurance portfolio. It simulates a large policy portfolio, models claims and risk, optimises pricing under multiple strategies, and monitors portfolio performance.

---

## Key Features

- **Portfolio Simulation:** Generate 50k+ policyholders with realistic features (age, gender, plan type, smoker status, BMI, tenure, NCD, excess).
- **Claims Simulation:** Synthetic claims generation with frequency and severity models.
- **Risk Modelling:**  
  - GBM-based frequency and severity models  
  - Burn cost calculation and GLM for interpretability  
- **Pricing & Demand:**  
  - Base and market pricing  
  - Demand simulation under market shocks  
  - Policy-level price optimisation (price grid evaluated per policy)
- **Business Rules:**  
  - Underwriting rules, caps & collars, discounts  
- **Scenario & Strategy Analysis:**  
  - Run multiple market scenarios (e.g., medical inflation, price war, combined shock)
  - Compare pricing strategies (base, aggressive, conservative)  
- **Monitoring:**  
  - Average Value of Exposure (AVE) using expected vs actual
  - Control chart flags for out-of-control policies 
- **Reporting:**  
  - Expected vs actual metrics (GWP, Claims, Renewals, Contribution)
  - Pivot tables and CSV outputs for scenario x strategy results
  - Heatmaps for visualization of scenario x strategy metrics

---

## Folder Structure

```text
project_root/
├── README.md
│
├── experiment_reports/
│   ├── acceptance_heatmap.png
│   ├── avg_price_heatmap.png
│   ├── experiment_results.csv
│   ├── loss_ratio_heatmap.png
│   ├── pivot_acceptance.csv
│   ├── pivot_avg_price.csv
│   └── pivot_loss_ratio.csv
│
└── pricing_engine/
    ├── __init__.py
    ├── main.py
    │
    ├── config/
    │   ├── aggressive.py
    │   ├── base.py
    │   ├── conservative.py
    │   └── __init__.py
    │
    ├── constraints/
    │   ├── caps_collars.py
    │   ├── discounts.py
    │   ├── underwriting_rules.py
    │   └── __init__.py
    │
    ├── data/
    │   ├── generator.py
    │   ├── schema.py
    │   └── __init__.py
    │
    ├── evaluation/
    │   ├── experiment_reporting.py
    │   ├── metrics.py
    │   ├── reporting.py
    │   └── __init__.py
    │
    ├── experiments/
    │   ├── runner.py
    │   ├── scenarios.py
    │   └── __init__.py
    │
    ├── monitoring/
    │   ├── ave.py
    │   ├── control_charts.py
    │   ├── drift.py
    │   └── __init__.py
    │
    ├── pricing/
    │   ├── demand.py
    │   ├── ltv.py
    │   ├── optimisation.py
    │   ├── simulate_demand.py
    │   └── __init__.py
    │
    └── risk/
        ├── burn_cost.py
        ├── burn_cost_glm.py
        ├── frequency.py
        ├── severity.py
        ├── simulate_claims.py
        ├── true_risk.py
        └── __init__.py
```
## Getting Started

### Requirements

- Python 3.9+  
- Libraries:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

## Running the Pipeline

### 1. Single End-to-End Pricing Run

```bash
python -m pricing_engine.main
```

- Simulates a portfolio of 50k+ policies
- Generates claims, frequency & severity models
- Calculates burn cost & GLM
- Simulates demand, optimises price (policy-level)
- Applies underwriting rules, caps, and discounts
- Outputs key metrics:
  - Expected vs Actual GWP
  - Expected vs Actual Claims
  - AVE overall + AVE by plan
  - Out-of-control flags
  - GLM coefficients
  - Overall performance report

### 2. Scenario x Strategy Experiments

```bash
python -m pricing_engine.experiments.runner
```

Runs all scenarios defined in scenarios.py under all pricing strategies (base, aggressive, conservative)

Produces:

- experiment_reports/experiment_results.csv
- Pivot tables for:
    - GWP, Claims, Renewals, Contribution, LossRatio
    - AVE metrics for all the above
- Heatmaps for visualization of scenario X strategy results

Heatmaps are saved in experiment_reports/plots/:

```bash
experiment_reports/plots/
```
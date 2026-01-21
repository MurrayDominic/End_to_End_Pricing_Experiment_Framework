# End-to-End Insurance Pricing Simulation & Optimisation

## Project Overview

This project implements a **fully parameterized, end-to-end pricing engine** for a synthetic health insurance portfolio. It simulates a large policy portfolio, models claims and risk, optimises pricing under multiple strategies, and monitors portfolio performance.  

---

## Key Features

- **Portfolio Simulation:** Generate 1M+ policyholders with realistic features (age, gender, plan type, smoker status, BMI, tenure, NCD, excess).  
- **Claims Simulation:** Synthetic claims generation with frequency and severity models.  
- **Risk Modelling:**  
  - GBM-based frequency and severity models  
  - Burn cost calculation and GLM for interpretability  
- **Pricing & Demand:**  
  - Base and market pricing  
  - Demand simulation under market shocks  
  - Price optimisation using scenario × strategy framework  
- **Business Rules:**  
  - Underwriting rules, caps & collars, discounts  
- **Scenario & Strategy Analysis:**  
  - Run multiple market scenarios (e.g., medical inflation, price war, tight underwriting)  
  - Compare pricing strategies (base, aggressive, conservative)  
- **Monitoring:**  
  - Average Value of Exposure (AVE)  
  - Control chart flags for out-of-control policies  
  - Drift detection framework (placeholder for historical comparison)  
- **Reporting:**  
  - Pivot tables and CSV outputs for scenario × strategy results  
  - Heatmaps for visualization of scenario × strategy metrics  

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
python -m pricing_engine.main

- Simulates a portfolio of 100k policies
- Generates claims, frequency & severity models
- Calculates burn cost & GLM
- Simulates demand, optimises price
- Applies underwriting rules, caps, and discounts
- Outputs key metrics: avg price, expected burn cost, acceptance, GLM coefficients

### 2. Scenario × Strategy Experiments

python -m pricing_engine.experiments.runner

Runs all scenarios defined in scenarios.py under all pricing strategies (base, aggressive, conservative)

Produces:

- experiment_reports/experiment_results.csv

- Pivot tables for avg_price, acceptance, loss_ratio, AVE, out-of-control policies

- Heatmaps for visualization of scenario × strategy results

Heatmaps are saved in experiment_reports/plots/:

- avg_price_heatmap.png

- acceptance_heatmap.png

- loss_ratio_heatmap.png

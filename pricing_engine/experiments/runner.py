import pandas as pd
import numpy as np

from pricing_engine.experiments.scenarios import SCENARIOS

from pricing_engine.data.generator import generate_policy_data
from pricing_engine.risk.simulate_claims import simulate_claims
from pricing_engine.risk.frequency import fit_frequency_model, prepare_features
from pricing_engine.risk.severity import fit_severity_model
from pricing_engine.risk.burn_cost import calculate_burn_cost
from pricing_engine.pricing.simulate_demand import simulate_demand
from pricing_engine.pricing.demand import fit_demand_model
from pricing_engine.pricing.optimisation import optimise_price
from pricing_engine.constraints.underwriting_rules import apply_underwriting_rules
from pricing_engine.constraints.caps_collars import apply_caps_and_collars
from pricing_engine.constraints.discounts import apply_discounts

from pricing_engine.monitoring.ave import calculate_ave
from pricing_engine.monitoring.control_charts import flag_out_of_control
from pricing_engine.monitoring.drift import detect_drift

from pricing_engine.evaluation.experiment_reporting import summarize_experiments
from pricing_engine.evaluation.experiment_reporting import save_policy_records

from pricing_engine.config.base import CONFIG as BASE_CONFIG
from pricing_engine.config.aggressive import CONFIG as AGGRESSIVE_CONFIG
from pricing_engine.config.conservative import CONFIG as CONSERVATIVE_CONFIG

import os

PRICING_STRATEGIES = {
    "base": BASE_CONFIG,
    "aggressive": AGGRESSIVE_CONFIG,
    "conservative": CONSERVATIVE_CONFIG
}


def generate_policy_records():

    print("Policy Data...")
    df = generate_policy_data(n=50_000)

    print("Claims data...")
    df = simulate_claims(df, 1)

    print("Risk models...")
    X = prepare_features(df)
    freq_model, _ = fit_frequency_model(df)
    sev_model = fit_severity_model(df, X)

    df["expected_burn_cost"] = calculate_burn_cost(freq_model, sev_model, X)

    df["base_price"] = df["expected_burn_cost"]

    market_noise = np.random.normal(loc=1.0, scale=0.05, size=len(df))
    df["market_price"] = df["base_price"] * 1.2 * market_noise

    df = df.rename(columns={"incurred": "py_incurred"})
    return df

def run_scenario(df, name, params, strategy_name, config):

    scenario_suffix = f"{name}_{strategy_name}"

    df = simulate_claims(df, 2)
    df["incurred"] *= params["claims_inflation"]

    base_price = df["base_price"] * (1 + config["profit_margin"])

    df = simulate_demand(
        df,
        premium=base_price,
        market_price=df["market_price"]
            * config["demand_shock_factor"]
            * params["demand_shock"]
    )

    df[f"renewal_likelihood_{scenario_suffix}"] = df["renewal_likelihood"]
    df[f"actual_renewal_{scenario_suffix}"] = df["accepted"]

    demand_model, demand_features = fit_demand_model(df)

    price_grid = np.array([0.9, 1.0, 1.1, 1.2])
    variable_expenses = 25 * config["expense_multiplier"] * params["expense_change"]

    target_price, policy_ltv = optimise_price(
        base_price=base_price,
        price_grid=price_grid,
        demand_model=demand_model,
        demand_features=demand_features,
        burn_cost=df["expected_burn_cost"],
        expenses=variable_expenses
    )

    df[f"optimised_loading_{scenario_suffix}"] = (
        target_price / base_price - 1
    )

    df["quotable"] = apply_underwriting_rules(df)

    previous_price = base_price * 0.95
    final_price = apply_caps_and_collars(
        target_price,
        previous_price,
        cap=config["max_cap"],
        collar=config["min_collar"]
    )
    final_price = apply_discounts(df, final_price)

    df[f"final_price_{scenario_suffix}"] = final_price
    df[f"incurred_{scenario_suffix}"] = df["incurred"]

    accepted_mask = df[f"actual_renewal_{scenario_suffix}"] == 1

    expected_accept = df[f"renewal_likelihood_{scenario_suffix}"].mean()
    expected_premium = (df[f"renewal_likelihood_{scenario_suffix}"] * df[f"final_price_{scenario_suffix}"]).sum()
    expected_claims = (df[f"renewal_likelihood_{scenario_suffix}"] * df[f"incurred_{scenario_suffix}"]).sum()
    expected_contribution = expected_premium - expected_claims

    actual_premium = df.loc[accepted_mask, f"final_price_{scenario_suffix}"].sum()
    actual_claims = df.loc[accepted_mask, f"incurred_{scenario_suffix}"].sum()
    actual_contribution = actual_premium - actual_claims

    summary = {
        "scenario": name,
        "strategy_name": strategy_name,


        "GWP_expected": expected_premium,
        "GWP_actual": actual_premium,

        "Claims_expected": expected_claims,
        "Claims_actual": actual_claims,

        "Renewal_expected": expected_accept,
        "Renewal_actual": df[f"actual_renewal_{scenario_suffix}"].mean(),

        "Contribution_expected": expected_contribution,
        "Contribution_actual": actual_contribution,

        "AvgPremium_expected": expected_premium / len(df),
        "AvgPremium_actual": actual_premium / len(df),

        "AvgContribution_expected": expected_contribution / len(df),
        "AvgContribution_actual": actual_contribution / len(df),

        "LossRatio_expected": expected_claims / expected_premium,
        "LossRatio_actual": actual_claims / actual_premium,
    }

    summary["AVE_GWP"] = actual_premium / expected_premium
    summary["AVE_Claims"] = actual_claims / expected_claims
    summary["AVE_Renewal"] = summary["Renewal_actual"] / summary["Renewal_expected"]
    summary["AVE_Contribution"] = actual_contribution / expected_contribution
    summary["AVE_LossRatio"] = summary["LossRatio_actual"] / summary["LossRatio_expected"]

    return df, summary

def main():

    results = []

    policy_records = generate_policy_records()

    for name, params in SCENARIOS.items():
        for strategy_name, config in PRICING_STRATEGIES.items():

            print(f"Running scenario: {name} | strategy: {strategy_name}")

            policy_records, result = run_scenario(
                policy_records,
                name,
                params,
                strategy_name,
                config
            )

            results.append(result)

    save_policy_records(
        policy_records,
        filename=os.path.join("data", "policy_records.csv")
    )

    results_df = pd.DataFrame(results)
    #print("\n Scenario - Strategy Results")
    #print(results_df)

    summarize_experiments(results_df, output_folder="experiment_reports")


if __name__ == "__main__":
    main()

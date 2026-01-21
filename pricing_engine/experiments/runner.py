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

from pricing_engine.config.base import CONFIG as BASE_CONFIG
from pricing_engine.config.aggressive import CONFIG as AGGRESSIVE_CONFIG
from pricing_engine.config.conservative import CONFIG as CONSERVATIVE_CONFIG

PRICING_STRATEGIES = {
    "base": BASE_CONFIG,
    "aggressive": AGGRESSIVE_CONFIG,
    "conservative": CONSERVATIVE_CONFIG
}


def run_scenario(name, params, config):

    print("Policy Data...")
    df = generate_policy_data(n=50_000)

    print("Claims inflation...")
    df = simulate_claims(df)
    df["incurred"] *= params["claims_inflation"]

    print("risk models...")
    X = prepare_features(df)
    freq_model, _ = fit_frequency_model(df)
    sev_model = fit_severity_model(df, X)

    df["expected_burn_cost"] = calculate_burn_cost(freq_model, sev_model, X)

    print("Base & market price...")
    base_price = df["expected_burn_cost"].mean() * (1 + config["profit_margin"])
    market_price = base_price * 1.05

    print("Demand model...")
    df = simulate_demand(
        df,
        premium=base_price,
        market_price=market_price / config["demand_shock_factor"] / params["demand_shock"]
    )

    demand_model, demand_features = fit_demand_model(df)

    price_grid = base_price * np.array([0.9, 1.0, 1.1, 1.2])
    variable_expenses = 25 * config["expense_multiplier"] * params["expense_change"]

    target_price, _ = optimise_price(
        base_price=base_price,
        price_grid=price_grid,
        demand_model=demand_model,
        demand_features=demand_features,
        burn_cost=df["expected_burn_cost"].mean(),
        expenses=variable_expenses
    )


    print("Underwriting Rules...")
    df["quotable"] = apply_underwriting_rules(df) 

    print("Caps & collars...")
    previous_price = base_price * 0.95
    df["price"] = apply_caps_and_collars(
        target_price,
        previous_price,
        cap=config["max_cap"],
        collar=config["min_collar"]
    )

    print("Discounts...")
    df["price"] = apply_discounts(df, df["price"])

    df["accepted"] = df["quotable"].astype(int)
    df["renewed"] = (df["is_renewal"] == 1) & (df["accepted"] == 1)

    print("Monitoring...")
    ave_df = calculate_ave(df, segment_col="plan")
    out_of_control_flags = flag_out_of_control(df["incurred"])

    # Drift detection needs reference data, placeholder example
    # drift_results = detect_drift(current_df=df, reference_df=df, feature_cols=["age", "tenure", "smoker"])

    accepted_mask = df["accepted"] == 1
    renewal_mask = df["is_renewal"] == 1

    return {
        "scenario": name,
        "strategy_name": config["profit_margin"],

        "avg_price": df.loc[accepted_mask, "price"].mean(),
        "total_premium": (df.loc[accepted_mask, "price"]).sum(),

        "quote_acceptance": accepted_mask.mean(),
        "renewal_rate": df.loc[renewal_mask, "renewed"].mean(),

        "loss_ratio": df.loc[accepted_mask, "incurred"].sum()
                    / df.loc[accepted_mask, "price"].sum(),

        "GWP": df.loc[accepted_mask, "price"].sum(),

        "contribution": df.loc[accepted_mask, "price"].sum()
                    - df.loc[accepted_mask, "incurred"].sum(),

        "ave_mean": ave_df["ave_ratio"].mean(),
        "out_of_control_count": out_of_control_flags.sum()

    }

def main():

    results = []

    for name, params in SCENARIOS.items():
        for strategy_name, config in PRICING_STRATEGIES.items():
            print(f"Running scenario: {name} | strategy: {strategy_name}")
            result = run_scenario(name, params, config)
            result["strategy_name"] = strategy_name
            results.append(result)

    results_df = pd.DataFrame(results)
    print("\n Scenario - Strategy Results")
    print(results_df)


    summarize_experiments(results_df, output_folder="experiment_reports")

    pivot = results_df.pivot_table(
        index="scenario",
        columns="strategy_name",
        values=["avg_price", "quote_acceptance", "loss_ratio", "GWP", "contribution", "ave_mean", "out_of_control_count"]
    )
    print("\n Pivot Table")
    print(pivot)


if __name__ == "__main__":
    main()

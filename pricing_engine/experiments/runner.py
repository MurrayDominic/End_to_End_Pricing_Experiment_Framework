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

# Monitoring
from pricing_engine.monitoring.ave import calculate_ave
from pricing_engine.monitoring.control_charts import flag_out_of_control
from pricing_engine.monitoring.drift import detect_drift

# Experiment reporting
from pricing_engine.evaluation.experiment_reporting import summarize_experiments

# Pricing strategies
from pricing_engine.config.base import CONFIG as BASE_CONFIG
from pricing_engine.config.aggressive import CONFIG as AGGRESSIVE_CONFIG
from pricing_engine.config.conservative import CONFIG as CONSERVATIVE_CONFIG

PRICING_STRATEGIES = {
    "base": BASE_CONFIG,
    "aggressive": AGGRESSIVE_CONFIG,
    "conservative": CONSERVATIVE_CONFIG
}


def run_scenario(name, params, config):

    df = generate_policy_data(n=50_000)

    print("Claims inflation...")
    df = simulate_claims(df)
    df["incurred"] *= params["claims_inflation"]

    # Risk models
    print("Claims inflation...")
    X = prepare_features(df)
    freq_model, _ = fit_frequency_model(df)
    sev_model = fit_severity_model(df, X)

    df["expected_burn_cost"] = calculate_burn_cost(freq_model, sev_model, X)

    print("Base & market price...")
    base_price = df["expected_burn_cost"].mean() * (1 + config["profit_margin"])
    market_price = base_price * 1.05

    print("Demand shock...")
    df = simulate_demand(
        df,
        premium=base_price,
        market_price=market_price / config["demand_shock_factor"]
    )

    demand_model, demand_features = fit_demand_model(df)

    price_grid = base_price * np.array([0.9, 1.0, 1.1, 1.2])
    variable_expenses = 25 * config["expense_multiplier"]

    target_price, _ = optimise_price(
        base_price=base_price,
        price_grid=price_grid,
        demand_model=demand_model,
        demand_features=demand_features,
        burn_cost=df["expected_burn_cost"].mean(),
        expenses=variable_expenses
    )


    print("Underwriting Rules...")
    df["quotable"] = apply_underwriting_rules(df) & (config["underwriting_strictness"] >= 1.0)

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


    print("Monitoring...")
    ave_df = calculate_ave(df, segment_col="plan")
    out_of_control_flags = flag_out_of_control(df["incurred"])
    # Drift detection needs reference data, placeholder example
    # drift_results = detect_drift(current_df=df, reference_df=df, feature_cols=["age", "tenure", "smoker"])

    return {
        "scenario": name,
        "strategy_name": config["profit_margin"],  # readable name if desired
        "avg_price": df["price"].mean(),
        "acceptance": df["quotable"].mean(),
        "loss_ratio": df["incurred"].mean() / df["price"].mean(),
        "ave_mean": ave_df["ave_ratio"].mean(),
        "out_of_control_count": out_of_control_flags.sum()
        # "drift_detected": drift_results["drift_flag"].sum()  # uncomment if reference data is available
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
    print("\n--- Scenario x Strategy Results ---")
    print(results_df)


    summarize_experiments(results_df, output_folder="experiment_reports")

    pivot = results_df.pivot_table(
        index="scenario",
        columns="strategy_name",
        values=["avg_price", "acceptance", "loss_ratio", "ave_mean", "out_of_control_count"]
    )
    print("\n--- Pivot Table ---")
    print(pivot)


if __name__ == "__main__":
    main()

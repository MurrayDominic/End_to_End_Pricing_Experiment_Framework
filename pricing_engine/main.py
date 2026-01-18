import numpy as np

from pricing_engine.data.generator import generate_policy_data
from pricing_engine.risk.simulate_claims import simulate_claims
from pricing_engine.risk.frequency import fit_frequency_model, prepare_features
from pricing_engine.risk.severity import fit_severity_model
from pricing_engine.risk.burn_cost import calculate_burn_cost
from pricing_engine.risk.burn_cost_glm import fit_burn_cost_glm

from pricing_engine.pricing.simulate_demand import simulate_demand
from pricing_engine.pricing.demand import fit_demand_model
from pricing_engine.pricing.optimisation import optimise_price

from pricing_engine.constraints.caps_collars import apply_caps_and_collars
from pricing_engine.constraints.discounts import apply_discounts
from pricing_engine.constraints.underwriting_rules import apply_underwriting_rules

from pricing_engine.monitoring.ave import calculate_ave
from pricing_engine.monitoring.control_charts import flag_out_of_control
from pricing_engine.monitoring.drift import detect_drift

from pricing_engine.evaluation.metrics import calculate_loss_ratio
from pricing_engine.evaluation.reporting import generate_overall_report

# from pricing_engine.config.aggressive import CONFIG
from pricing_engine.config.base import CONFIG
# from pricing_engine.config.conservative import CONFIG

def main():

    print("Generating policy data...")
    df = generate_policy_data(n=100_000)

    print("Simulating claims experience...")
    df = simulate_claims(df)

    print("Preparing features...")
    X = prepare_features(df)

    # GBM
    print("Fitting frequency model...")
    freq_model, feature_cols = fit_frequency_model(df)

    # GBM
    print("Fitting severity model...")
    sev_model = fit_severity_model(df, X)

    print("Calculating burn cost...")
    df["expected_burn_cost"] = calculate_burn_cost(
        freq_model,
        sev_model,
        X
    )

    # GLM
    print("Fitting GLM burn cost model...")
    burn_cost_glm = fit_burn_cost_glm(
        df,
        df["expected_burn_cost"]
    )

    print("Creating base and market prices...")
    base_price = df["expected_burn_cost"].mean() * (1 + CONFIG["profit_margin"])
    market_price = base_price * 1.05

    print("Simulating demand...")
    df = simulate_demand(
        df,
        premium=base_price,
        market_price=market_price / CONFIG["demand_shock_factor"]
    )

    print("Fitting demand model...")
    demand_model, demand_features = fit_demand_model(df)

    print("Optimising price...")
    price_grid = base_price * np.linspace(0.8, 1.4, 15)
    expenses = 25 * CONFIG["expense_multiplier"]
    burn_cost = df["expected_burn_cost"].mean()

    target_price, target_ltv = optimise_price(

        base_price=base_price,
        price_grid=price_grid,
        demand_model=demand_model,
        demand_features=demand_features,
        burn_cost=burn_cost,
        expenses=expenses
    )

    print("Applying underwriting rules...")
    df["quotable"] = apply_underwriting_rules(df)

    print("Applying caps & collars...")
    previous_price = base_price * 0.95  # proxy for last year price

    df["capped_price"] = np.where(
        df["quotable"],
        apply_caps_and_collars(
            price=target_price,
            previous_price=previous_price,
            cap=CONFIG["max_cap"],
            collar=CONFIG["min_collar"]
        ),
        np.nan
    )

    print("Applying discounts...")
    df["final_price"] = np.where(
        df["quotable"],
        apply_discounts(df, df["capped_price"]),
        np.nan
    )

    ave_df = calculate_ave(df, segment_col="plan")
    print("\nAVE by plan:")
    print(ave_df)

    out_of_control = flag_out_of_control(df["incurred"])
    print("\nOut of control policies:", out_of_control.sum())

    # Drift
    # current_df = df_this_month
    # reference_df = df_last_month
    # feature_cols = ["age", "tenure", "smoker"]
    # drift_results = detect_drift(current_df, reference_df, feature_cols)

    df = calculate_loss_ratio(df)
    overall_ave = calculate_ave(df)
    print(overall_ave)
    overall_report = generate_overall_report(df)
    print(overall_report)

    # Checks 
    print("\n--- Checks ---")
    print("Average incurred:", round(df["incurred"].mean(), 2))
    print("Average expected burn cost:", round(df["expected_burn_cost"].mean(), 2))
    print("Average final price:", round(df["final_price"].mean(), 2))

    print("\nDecline rate:", round(1 - df["quotable"].mean(), 3))

    print("\nGLM coefficients:")
    print(burn_cost_glm.params)

    print("\n--- Pricing Decision ---")
    print(f"Base price: £{base_price:,.0f}")
    print(f"Target price (optimised): £{target_price:,.0f}")
    print(f"Expected LTV: £{target_ltv:,.0f}")

if __name__ == "__main__":
    main()
    

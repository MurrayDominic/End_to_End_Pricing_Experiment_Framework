import numpy as np
import pandas as pd

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

from pricing_engine.monitoring.control_charts import flag_out_of_control
from pricing_engine.evaluation.metrics import calculate_loss_ratio
from pricing_engine.evaluation.reporting import generate_overall_report

from pricing_engine.config.base import CONFIG



def main():

    print("Generating policy data...")
    df = generate_policy_data(n=100_000)

    print("Simulating claims experience...")
    df = simulate_claims(df)

    print("Preparing features...")
    X = prepare_features(df)

    print("Fitting frequency model...")
    freq_model, feature_cols = fit_frequency_model(df)

    print("Fitting severity model...")
    sev_model = fit_severity_model(df, X)

    print("Calculating burn cost...")
    df["expected_burn_cost"] = calculate_burn_cost(
        freq_model,
        sev_model,
        X
    )

    print("Fitting GLM burn cost model...")
    burn_cost_glm = fit_burn_cost_glm(
        df,
        df["expected_burn_cost"]
    )

    print("Creating base and market prices (policy level)...")
    df["base_price"] = df["expected_burn_cost"] * (1 + CONFIG["profit_margin"])
    df["market_price"] = df["base_price"] * 1.2 * np.random.normal(1.0, 0.05, size=len(df))

    print("Simulating demand...")
    df = simulate_demand(
        df,
        premium=df["base_price"],
        market_price=df["market_price"] / CONFIG["demand_shock_factor"]
    )

    df["renewal_likelihood"] = df["accepted"]
    df["actual_renewal"] = df["accepted"]

    print("Fitting demand model...")
    demand_model, demand_features = fit_demand_model(df)

    print("Optimising price (policy-level)...")
    price_grid = np.linspace(0.8, 1.4, 15)
    expenses = 25 * CONFIG["expense_multiplier"]

    target_price, target_ltv = optimise_price(
        base_price=df["base_price"],
        price_grid=price_grid,
        demand_model=demand_model,
        demand_features=demand_features,
        burn_cost=df["expected_burn_cost"],
        expenses=expenses
    )

    df["optimised_price"] = target_price
    df["optimised_loading"] = (target_price / df["base_price"]) - 1

    print("Applying underwriting rules...")
    df["quotable"] = apply_underwriting_rules(df)

    print("Applying caps & collars...")
    previous_price = df["base_price"] * 0.95

    df["capped_price"] = np.where(
        df["quotable"],
        apply_caps_and_collars(
            price=df["optimised_price"],
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

    accepted_mask = df["actual_renewal"] == 1

    # expected
    expected_premium = (df["renewal_likelihood"] * df["final_price"]).sum()
    expected_claims = (df["renewal_likelihood"] * df["incurred"]).sum()

    # actual
    actual_premium = df.loc[accepted_mask, "final_price"].sum()
    actual_claims = df.loc[accepted_mask, "incurred"].sum()

    print("\n--- Expected vs Actual ---")
    print(f"Expected GWP: {expected_premium:,.0f}")
    print(f"Actual GWP: {actual_premium:,.0f}")

    print(f"Expected Claims: {expected_claims:,.0f}")
    print(f"Actual Claims: {actual_claims:,.0f}")

    print("\n--- AVE ---")
    print(f"AVE GWP: {actual_premium / expected_premium:.2f}")
    print(f"AVE Claims: {actual_claims / expected_claims:.2f}")

    out_of_control = flag_out_of_control(df["incurred"])
    print("\nOut of control policies:", out_of_control.sum())

    df = calculate_loss_ratio(df)

    overall_report = generate_overall_report(
        df,
        price_col="final_price",
        accept_col="quotable",
        expenses=expenses
    )
    print(overall_report)

    print("\n--- Checks ---")
    print("Average incurred:", round(df["incurred"].mean(), 2))
    print("Average expected burn cost:", round(df["expected_burn_cost"].mean(), 2))
    print("Average final price:", round(df["final_price"].mean(), 2))

    print("\nDecline rate:", round(1 - df["quotable"].mean(), 3))

    print("\nGLM coefficients:")
    print(burn_cost_glm.params)

    print("\n--- Pricing Decision ---")
    print(f"Base price (avg): £{df['base_price'].mean():,.0f}")
    print(f"Target price (avg): £{df['optimised_price'].mean():,.0f}")
    print(f"Expected LTV (avg): £{target_ltv.mean():,.0f}")


if __name__ == "__main__":
    main()
import pandas as pd

from data.generator import generate_policy_data
from risk.simulate_claims import simulate_claims

from risk.frequency import fit_frequency_model, prepare_features
from risk.severity import fit_severity_model
from risk.burn_cost import calculate_burn_cost
from risk.burn_cost_glm import fit_burn_cost_glm


def main():

    # Generate portfolio
    print("Generating policy data")
    df = generate_policy_data(n=100_000)

    # Simulate realised claims experience
    print("Simulating claims experience")
    df = simulate_claims(df)

    # Prepare model features
    print("Preparing features")
    X = prepare_features(df)

    # Fit frequency model (GBM)
    print("Fitting frequency model")
    freq_model, feature_cols = fit_frequency_model(df)

    # Fit severity model (GBM)
    print("Fitting severity model")
    sev_model = fit_severity_model(df, X)

    # burn cost from GBMs
    print("Calculating expected burn cost...")
    df["expected_burn_cost"] = calculate_burn_cost(
        freq_model,
        sev_model,
        X
    )

    # Fit GLM on burn cost
    print("Fitting GLM burn cost model")
    burn_cost_glm = fit_burn_cost_glm(
        df,
        df["expected_burn_cost"]
    )

    # checks
    print("\n checks")
    print("Average incurred:", df["incurred"].mean())
    print("Average expected burn cost:", df["expected_burn_cost"].mean())
    print("\nGLM coefficients:")
    print(burn_cost_glm.params)



if __name__ == "__main__":
    main()
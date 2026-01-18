import pandas as pd

def calculate_loss_ratio(df, price_col="final_price"):
    # Compute overall and segment-level loss ratio

    df = df.copy()
    df["loss_ratio"] = df["incurred"] / df[price_col]
    return df

def calculate_ave_ratio(df, expected_col="expected_burn_cost", price_col="final_price"):
    #Calculate actual vs expected metrics

    df = df.copy()
    df["ave_ratio"] = df["incurred"] / df[expected_col]
    df["premium_ratio"] = df[price_col] / df[expected_col]
    return df

def segment_kpis(df, segment_col="plan"):
    # Compute KPIs by segment

    grouped = df.groupby(segment_col).agg(
        avg_loss_ratio=("incurred", lambda x: (x / df.loc[x.index, "final_price"]).mean()),
        avg_premium=("final_price", "mean"),
        acceptance_rate=("accepted", "mean"),
        ave_ratio=("incurred", lambda x: (x / df.loc[x.index, "expected_burn_cost"]).mean())
    )
    return grouped
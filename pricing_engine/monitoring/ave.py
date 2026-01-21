import pandas as pd

def calculate_ave(df, segment_col=None):

    if segment_col:
        group = df.groupby(segment_col)
        ave_df = pd.DataFrame({
            "actual_incurred": group["incurred"].mean(),
            "expected_incurred": group["expected_burn_cost"].mean(),
            "ave_ratio": group["incurred"].mean() / group["expected_burn_cost"].mean(),
            "actual_acceptance": group["accepted"].mean()
        })
    else:
        ave_df = pd.DataFrame({
            "actual_incurred": [df["incurred"].mean()],
            "expected_incurred": [df["expected_burn_cost"].mean()],
            "ave_ratio": [df["incurred"].mean() / df["expected_burn_cost"].mean()],
            "actual_acceptance": [df["accepted"].mean()]
        })

    return ave_df
import numpy as np

rng = np.random.default_rng(seed=777)

def simulate_demand(df, premium, market_price):
    """
    Simulates observed accept / reject decisions.
    """

    rel_price = premium / market_price

    # ---- Latent willingness to pay (truth) ----
    latent_utility = (
        1.5                           # base 
        - 4.0 * rel_price             # price sensitivity
        + 0.03 * df["tenure"]          # loyal customers
        + 0.02 * (df["age"] > 50)      # older being less price sensitive
        + np.where(df["plan"] == "Premium", 0.6, 0.0)
        + rng.normal(0, 0.6, size=len(df))  # other
    )

    prob_accept = 1 / (1 + np.exp(-latent_utility))

    accepted = rng.binomial(1, prob_accept)

    df = df.copy()
    df["accepted"] = accepted
    df["rel_price"] = rel_price

    return df
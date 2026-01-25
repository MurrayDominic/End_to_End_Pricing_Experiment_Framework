import numpy as np

rng = np.random.default_rng(seed=100)

def simulate_demand(df, premium, market_price):
    rel_price = premium / market_price

    latent_utility = (
    0.3                                
    - 5.0 * (rel_price - 1.0)           
    + 0.04 * df["tenure"]             
    + 0.15 * (df["age"] > 50)         
    + np.where(df["plan"] == "Premium", 0.5, 0.0)
    + rng.normal(0, 0.7, size=len(df)) 
)

    prob_accept = 1 / (1 + np.exp(-latent_utility))
    accepted = rng.binomial(1, prob_accept)

    df = df.copy()
    df["rel_price"] = rel_price
    df["accepted"] = accepted

    # scenario-specific outputs (temporary)
    df["renewal_likelihood"] = prob_accept
    df["actual_renewal"] = accepted

    return df
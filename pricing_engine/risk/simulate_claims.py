import numpy as np
from pricing_engine.risk.true_risk import true_risk_score

rng = np.random.default_rng(seed=123)

def simulate_claims(df):

    risk = true_risk_score(df)

    # Frequency - annual
    lambda_freq = np.exp(-3.5 + 0.4 * risk)
    n_claims = rng.poisson(lam=lambda_freq)

    # Severity
    base_severity = 600
    severity_mean = base_severity * risk

    incurred = []
    for n, mean_sev in zip(n_claims, severity_mean):
        if n == 0:
            incurred.append(0.0)
        else:
            claims = rng.gamma(
                shape=2.0,
                scale=mean_sev / 2.0,
                size=n
            )
            incurred.append(claims.sum())

    df = df.copy()
    df["n_claims"] = n_claims
    df["incurred"] = incurred

    return df
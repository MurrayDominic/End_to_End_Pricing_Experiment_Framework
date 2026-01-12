import statsmodels.api as sm
import numpy as np
import pandas as pd

GLM_FEATURES = [
    "age",
    "tenure",
    "smoker",
    "ncd",
    "excess"
]

def fit_burn_cost_glm(df, burn_cost):
    X = df[GLM_FEATURES].copy()
    X["smoker"] = (X["smoker"] == "Y").astype(int)
    X = sm.add_constant(X)

    y = np.log(burn_cost + 1)

    model = sm.GLM(
        y,
        X,
        family=sm.families.Gaussian()
    ).fit()

    return model
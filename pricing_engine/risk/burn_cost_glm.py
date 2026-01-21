import numpy as np
import pandas as pd
import statsmodels.api as sm

GLM_FEATURES = [
    "age",
    "tenure",
    "smoker",
    "ncd",
    "excess"
]

def fit_burn_cost_glm(df, burn_cost):

    burn_cost = burn_cost.copy()


    burn_cost = burn_cost.replace([np.inf, -np.inf], np.nan)
    burn_cost = burn_cost.fillna(0)
    burn_cost = burn_cost.clip(lower=0)

    y = np.log1p(burn_cost) 

    # feature
    X = df[GLM_FEATURES].copy()
    X["smoker"] = (X["smoker"] == "Y").astype(int)
    X["ncd"] = X["ncd"].astype(int)
    X["excess"] = X["excess"].astype(int)
    X["tenure"] = X["tenure"].clip(0, 50)
    X = sm.add_constant(X)
    X = X.astype(float)

    # fit GLM
    model = sm.GLM(
        y,
        X,
        family=sm.families.Gaussian()
    ).fit()

    return model

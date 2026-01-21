import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

FEATURES = [
    "rel_price",    
    "age",
    "tenure",
    "plan"
]

def prepare_demand_features(df):
    X = df[FEATURES].copy()
    X = pd.get_dummies(X, columns=["plan"], drop_first=True) #numeric (one-hot)
    return X

def fit_demand_model(df):
    X = prepare_demand_features(df)
    y = df["accepted"]  # simulated or historical

    #basic model
    model = LogisticRegression(
        max_iter=500,
        solver="lbfgs"
    )
    model.fit(X, y)
    return model, X

def predict_demand(model, X):
    return model.predict_proba(X)[:, 1]
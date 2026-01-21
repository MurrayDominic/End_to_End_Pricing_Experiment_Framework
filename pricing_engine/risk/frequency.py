import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

FEATURES = [
    "age",
    "tenure",
    "smoker",
    "bmi",
    "plan",
    "ncd",
    "excess"
]

def prepare_features(df):
    X = df[FEATURES].copy()
    X["smoker"] = (X["smoker"] == "Y").astype(int)
    X = pd.get_dummies(X, columns=["bmi", "plan"], drop_first=True)
    return X

def fit_frequency_model(df):
    X = prepare_features(df)
    y = df["n_claims"]

    # Hyperparameter tunning can be done here
    model = GradientBoostingRegressor(
        loss="squared_error",
        max_depth=3,
        n_estimators=150,
        learning_rate=0.05,
        random_state=42
    )

    model.fit(X, y)
    return model, X.columns

def predict_frequency(model, X):
    return np.clip(model.predict(X), 0, None)
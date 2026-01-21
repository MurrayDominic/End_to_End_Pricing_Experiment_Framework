import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

def fit_severity_model(df, X):
    mask = df["n_claims"] > 0

    y = df.loc[mask, "incurred"] / df.loc[mask, "n_claims"]

    # Hyperparameter tunning can be done here
    model = GradientBoostingRegressor(
        loss="squared_error",
        max_depth=3,
        n_estimators=200,
        learning_rate=0.05,
        random_state=42
    )

    model.fit(X.loc[mask], y)
    return model

def predict_severity(model, X):
    return np.clip(model.predict(X), 1.0, None)
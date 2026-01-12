import numpy as np

def true_risk_score(df):

    #This represents the true underlying morbidity risk.

    age_factor = 0.015 * df["age"]

    smoker_factor = np.where(df["smoker"] == "Y", 0.6, 0.0)

    bmi_factor = df["bmi"].map({
        "Underweight": 0.1,
        "Normal": 0.0,
        "Overweight": 0.3,
        "Obese": 0.7
    }).values

    plan_factor = df["plan"].map({
        "Budget": 0.8,
        "Standard": 1.0,
        "Premium": 1.3
    }).values

    excess_factor = df["excess"].astype(int)
    excess_factor = -0.0002 * excess_factor  # higher excess → lower utilisation

    base = 0.8

    risk_score = (
        base
        + age_factor
        + smoker_factor
        + bmi_factor
        + excess_factor
    ) * plan_factor

    return np.clip(risk_score, 0.3, 5.0)
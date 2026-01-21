def apply_underwriting_rules(df):
    # decline for unhealthy members
    decline = (
        (df["age"] > 85) |
        ((df["smoker"] == "Y") & (df["bmi"] == "Obese")) |
        (df["tenure"] < 0.1)
    )
    return ~decline
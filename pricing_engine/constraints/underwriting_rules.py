def apply_underwriting_rules(df):
    """
    Returns boolean: whether policy is quotable.
    """

    decline = (
        (df["age"] > 85) |
        ((df["smoker"] == "Y") & (df["bmi"] == "Obese")) |
        (df["tenure"] < 0.1)
    )

    return ~decline
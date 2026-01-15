def apply_discounts(df, price):

    # Applies commercial discounts

    discount = 0.0

    # Multi-year / loyalty
    discount += 0.05 * (df["tenure"] > 3)

    # High excess incentive
    discount += 0.03 * (df["excess"].astype(int) >= 1000)

    # NCD reward
    discount += df["ncd"].astype(int) / 200

    discount = min(discount, 0.25)

    final_price = price * (1 - discount)

    return final_price
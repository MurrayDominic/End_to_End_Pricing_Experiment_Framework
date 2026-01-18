def apply_discounts(df, price):

    #Applies commercial discounts at policy level
    discount = 0.0

    # Multi-year / loyalty
    discount += 0.05 * (df["tenure"] > 3).astype(int)

    # High excess incentive
    discount += 0.03 * (df["excess"].astype(int) >= 1000).astype(int)

    # NCD reward (e.g. 0–30% -> 0–15%)
    discount += df["ncd"].astype(int) / 200

    # Cap total discount at 25% PER POLICY
    discount = discount.clip(upper=0.25)

    final_price = price * (1 - discount)

    return final_price
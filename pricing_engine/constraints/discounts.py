def apply_discounts(df, price):

    discount = 0.0

    # loyalty
    discount += 0.05 * (df["tenure"] > 3).astype(int)

    # High excess discount
    discount += 0.03 * (df["excess"].astype(int) >= 1000).astype(int)

    # NCD 
    discount += df["ncd"].astype(int) / 200

    # Cap total discount at 25% PER POLICY
    discount = discount.clip(upper=0.25)

    final_price = price * (1 - discount)

    return final_price
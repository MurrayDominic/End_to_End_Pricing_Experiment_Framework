import numpy as np

def optimise_price(
    base_price,
    price_grid,
    demand_model,
    demand_features,
    burn_cost,
    expenses
):
    best_price = base_price
    best_ltv = -np.inf

    for price in price_grid:
        X = demand_features.copy()
        X["rel_price"] = price / base_price

        p_accept = demand_model.predict_proba(X)[:, 1]

        profit_per_quote = p_accept * (price - burn_cost - expenses)


        ltv = profit_per_quote.mean()

        if ltv > best_ltv:
            best_ltv = ltv
            best_price = price

    return best_price, best_ltv

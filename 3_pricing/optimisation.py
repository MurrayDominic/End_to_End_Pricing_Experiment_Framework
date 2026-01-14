# maximize sum(retention_i × margin_i)

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

        demand_prob = demand_model.predict_proba(X)[:, 1].mean()

        ltv = (
            price * demand_prob
            - burn_cost
            - expenses
        )

        if ltv > best_ltv:
            best_ltv = ltv
            best_price = price

    return best_price, best_ltv
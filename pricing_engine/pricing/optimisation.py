import numpy as np

#  doesnt include past renewal data

def optimise_price(
    base_price,
    price_grid,
    demand_model,
    demand_features,
    burn_cost,
    expenses
):
    n_policies = len(base_price)
    n_grid = len(price_grid)

    best_price = np.zeros(n_policies)
    best_ltv = np.full(n_policies, -np.inf)

    for m in price_grid:
        price = base_price * m

        X = demand_features.copy()
        X["rel_price"] = price / base_price

        p_accept = demand_model.predict_proba(X)[:, 1]

        profit_per_quote = p_accept * (price - burn_cost - expenses)

        improve_mask = profit_per_quote > best_ltv

        best_ltv[improve_mask] = profit_per_quote[improve_mask]
        best_price[improve_mask] = price[improve_mask]

    return best_price, best_ltv

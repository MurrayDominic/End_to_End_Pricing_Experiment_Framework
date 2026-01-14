import numpy as np

def apply_caps_and_collars(
    price,
    previous_price,
    cap=0.20,
    collar=-0.15
):
    """
    Limits price movement vs previous price.
    """

    max_price = previous_price * (1 + cap)
    min_price = previous_price * (1 + collar)

    capped_price = np.clip(price, min_price, max_price)

    return capped_price
new_price = np.clip(
    base_price * (1 + change),
    base_price * 0.85,
    base_price * 1.15
)
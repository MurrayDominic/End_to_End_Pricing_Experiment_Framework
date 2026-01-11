def generate_policy_data(n=100_000):
    return pd.DataFrame({
        "age": np.random.randint(18, 80, n),
        "tenure": np.random.exponential(3, n),
        "ncd": np.random.choice([0, 20, 30, 40, 50], n),
        "region": np.random.choice(["A", "B", "C"], n),
        "base_risk": np.random.gamma(2, 1, n)
    })
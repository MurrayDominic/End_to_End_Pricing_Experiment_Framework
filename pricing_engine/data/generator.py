import numpy as np
import pandas as pd

rng = np.random.default_rng(seed = 100)

def generate_policy_data(n=1_000_000):

    #age = rng.integers(0, 90, size = n)
    #age = np.clip(
    #    rng.normal(45, 18, size=n), 
    #    1, 100).astype(int)
    
    mix = rng.choice([0, 1], size=n, p=[0.25, 0.75])

    age = np.where(
        mix == 0,
        rng.normal(10, 6, size=n),    # children
        rng.normal(48, 15, size=n)    # adults
    )

    age = np.clip(age, 0, 100).astype(int)

    gender = rng.choice(
        ['M', 'F'],
        size = n,
        p = [0.45, 0.55]
    )

    region = rng.choice(
        ['South West', 'South East', 'London', 'East of England', 'West Midlands', 'East Midlands', 'North West', 'North East', 'Yorkshire and the Humber', 'Wales', 'Scotland', 'Northern Ireland'],
        size = n,
        p = [0.1, 0.1, 0.3, 0.05, 0.05, 0.1, 0.05, 0.06, 0.05, 0.06, 0.07, 0.01]
    )

    
    tenure = rng.exponential(scale=4, size = n)
    tenure = np.clip(tenure, 0, 30)

    smoker = rng.choice(
        ['Y', 'N'],
        size = n,
        p = [0.15, 0.85]
    )

    bmi = rng.choice(
        ['Underweight', 'Normal', 'Overweight', 'Obese'],
        size = n,
        p = [0.05, 0.40, 0.35, 0.20]
    )

    plan = rng.choice(
        ['Budget', 'Standard', 'Premium'],
        size = n,
        p = [0.1, 0.4, 0.5]
    )

    # not realistic, low tenures won't be able to have high NCD
    ncd = rng.choice(
        ["0", '10', '20', '30'],
        size = n,
        p = [0.1, 0.2, 0.4, 0.3]
    )    

    excess = rng.choice(
        ['0', '250', '500', '1000', '2000'],
         size = n,
         p = [0.4, 0.2, 0.2, 0.1, 0.1]
    )

 #   is_renewal = np.random.binomial(1, 0.6, size = n)

    df = pd.DataFrame({
        "age": age,
        "gender": gender,
        "region": region,
        "tenure": tenure,
        "smoker": smoker,
        "bmi": bmi,
        "plan": plan,
        "ncd": ncd,
        'excess': excess,
#        'is_renewal': is_renewal
    })

    return df 

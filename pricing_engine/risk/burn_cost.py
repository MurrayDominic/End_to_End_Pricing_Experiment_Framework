import numpy as np
import pandas as pd

def calculate_burn_cost(freq_model, sev_model, X):
    freq = freq_model.predict(X)
    sev = sev_model.predict(X)
    return freq * sev
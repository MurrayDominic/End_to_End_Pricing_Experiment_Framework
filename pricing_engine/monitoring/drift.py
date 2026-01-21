import pandas as pd
from scipy.stats import ks_2samp

def detect_drift(current_df, reference_df, feature_cols):

    drift_results = {}
    for col in feature_cols:
        stat, p_value = ks_2samp(reference_df[col], current_df[col])
        drift_results[col] = p_value
    return drift_results
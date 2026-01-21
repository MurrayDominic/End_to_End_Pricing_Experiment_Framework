import pandas as pd

def moving_average(series, window=12):
    return series.rolling(window).mean()

def control_limits(series, k=3):

    mean = series.mean()
    std = series.std()
    upper = mean + k * std
    lower = mean - k * std
    return lower, upper

def flag_out_of_control(series, k=3):
    lower, upper = control_limits(series, k)
    return (series < lower) | (series > upper)
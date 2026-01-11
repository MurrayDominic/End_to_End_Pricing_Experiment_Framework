# loss ratio, GWP, Retention, Margin, AvE, Segment-level movement



results = {
    "loss_ratio": burn_cost.sum() / premium.sum(),
    "retention": retention.mean(),
    "profit": profit.sum()
}

ave = (actual - expected) / expected

# Control charts, rolling mean, confidence bands
import pandas as pd

def generate_summary_report(df, segment_col="plan", filename='Report'):
    # segment-level KPI table

    from pricing_engine.evaluation.metrics import segment_kpis
    report = segment_kpis(df, segment_col)
    
    if filename:
        report.to_csv(filename)
    
    return report

def generate_overall_report(df):

    report = {
        "avg_loss_ratio": df["loss_ratio"].mean(),
        "avg_premium": df["final_price"].mean(),
        "quote_acceptance_rate": df["accepted"].mean(),
        "portfolio_ltv": ( df.loc[accepted_mask, "price"].sum() - df.loc[accepted_mask, "incurred"].sum() - expenses * accepted_mask.sum())
    }
    return report
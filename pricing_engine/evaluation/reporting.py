import pandas as pd

def generate_summary_report(df, segment_col="plan", filename='Report'):
    # segment-level KPI table

    from pricing_engine.evaluation.metrics import segment_kpis
    report = segment_kpis(df, segment_col)
    
    if filename:
        report.to_csv(filename)
    
    return report

def generate_overall_report(df, price_col="final_price", accept_col="quotable", expenses=0):
    accepted_mask = df[accept_col].astype(bool)

    portfolio_ltv = (
        df.loc[accepted_mask, price_col].sum()
        - df.loc[accepted_mask, "incurred"].sum()
        - expenses * accepted_mask.sum()
    )

    return {
        "portfolio_ltv": portfolio_ltv,
        "gwp": df.loc[accepted_mask, price_col].sum(),
        "claims": df.loc[accepted_mask, "incurred"].sum(),
        "loss_ratio": df.loc[accepted_mask, "incurred"].sum() / df.loc[accepted_mask, price_col].sum()
    }
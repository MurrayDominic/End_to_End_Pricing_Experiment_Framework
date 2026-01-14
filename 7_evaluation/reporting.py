import pandas as pd

def generate_summary_report(df, segment_col="plan", filename=None):
    """
    Returns segment-level KPI table and optionally saves to CSV.
    """
    from metrics import segment_kpis
    report = segment_kpis(df, segment_col)
    
    if filename:
        report.to_csv(filename)
    
    return report

def generate_overall_report(df, filename=None):
    """
    Returns overall KPIs as a dictionary.
    """
    from metrics import calculate_loss_ratio, calculate_ave_ratio
    
    df = calculate_loss_ratio(df)
    df = calculate_ave_ratio(df)
    
    overall = {
        "avg_loss_ratio": df["loss_ratio"].mean(),
        "avg_ave_ratio": df["ave_ratio"].mean(),
        "avg_premium": df["final_price"].mean(),
        "acceptance_rate": df["accepted"].mean()
    }
    
    if filename:
        pd.DataFrame([overall]).to_csv(filename, index=False)
    
    return overall
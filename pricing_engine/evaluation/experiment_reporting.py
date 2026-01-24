import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def save_policy_records(policy_records, filename="policy_records.csv"):

    policy_records.to_csv(filename, index=False)
    print(f"Policy Records saved to {filename}")

def save_experiment_results(results_df, filename="experiment_results.csv"):

    results_df.to_csv(filename, index=False)
    print(f"Experiment results saved to {filename}")

def pivot_experiment_results(results_df, value_cols):
    return {
        col: results_df.pivot_table(
            index="scenario",
            columns="strategy_name",
            values=col
        )
        for col in value_cols
    }

def plot_experiment_results(pivot_table, metric_name="avg_price", output_folder="plots"):
    os.makedirs(output_folder, exist_ok=True)

    ratio_metrics = {
        "loss_ratio",
        "quote_acceptance",
    }

    # Color map logic
    if metric_name == "loss_ratio":
        cmap = "RdYlGn_r"   # green lower is better
    else:
        cmap = "RdYlGn"
        center = None

    # Annotation formatting (metric-based)
    def format_value(x):
        if pd.isna(x):
            return ""
        if metric_name in ratio_metrics:
            return f"{x * 100:.0f}%"
        else:
            return f"{int(round(x)):,}"

    annot = pivot_table.applymap(format_value)

    plt.figure(figsize=(10, 6))
    sns.heatmap(
        pivot_table,
        annot=annot,
        fmt="",
        cmap=cmap
    )

    plt.title(f"{metric_name.replace('_', ' ').title()} by Scenario x Strategy")
    plt.ylabel("Scenario")
    plt.xlabel("Strategy")

    plot_file = os.path.join(output_folder, f"heatmap_{metric_name}.png")
    plt.savefig(plot_file, bbox_inches="tight")
    plt.close()

    print(f"Heatmap saved to {plot_file}")

def summarize_experiments(results_df, output_folder="plots"):
    os.makedirs(output_folder, exist_ok=True)

    save_experiment_results(
        results_df,
        filename=os.path.join(output_folder, "experiment_results.csv")
    )

    values = ["avg_price", "quote_acceptance", "loss_ratio", "GWP", "contribution"]

    pivots = pivot_experiment_results(results_df, values)

    for col, pivot_df in pivots.items():
        pivot_df.to_csv(
            os.path.join(output_folder, f"pivot_{col}.csv")
        )
        plot_experiment_results(pivot_df, col, output_folder)
    



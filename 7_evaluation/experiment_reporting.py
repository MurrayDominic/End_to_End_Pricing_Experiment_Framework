import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def save_experiment_results(results_df, filename="experiment_results.csv"):
    """
    Saves the raw scenario × strategy results to CSV.
    """
    results_df.to_csv(filename, index=False)
    print(f"Experiment results saved to {filename}")


def pivot_experiment_results(results_df):
    """
    Creates pivot tables for avg_price, acceptance, and loss_ratio
    indexed by scenario, columns = strategy
    """
    pivot_price = results_df.pivot_table(
        index="scenario",
        columns="strategy_name",
        values="avg_price"
    )

    pivot_accept = results_df.pivot_table(
        index="scenario",
        columns="strategy_name",
        values="acceptance"
    )

    pivot_loss = results_df.pivot_table(
        index="scenario",
        columns="strategy_name",
        values="loss_ratio"
    )

    return pivot_price, pivot_accept, pivot_loss


def plot_experiment_results(pivot_table, metric_name="avg_price", output_folder="plots"):
    """
    Plots scenario × strategy results as a heatmap for quick visualization.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title(f"{metric_name.replace('_',' ').title()} by Scenario × Strategy")
    plt.ylabel("Scenario")
    plt.xlabel("Strategy")
    
    plot_file = os.path.join(output_folder, f"{metric_name}_heatmap.png")
    plt.savefig(plot_file, bbox_inches="tight")
    plt.close()
    print(f"Heatmap saved to {plot_file}")


def summarize_experiments(results_df, output_folder="plots"):
    """
    Full experiment summary: saves CSV and generates heatmaps for all metrics.
    """
    save_experiment_results(results_df, filename=os.path.join(output_folder, "experiment_results.csv"))

    pivot_price, pivot_accept, pivot_loss = pivot_experiment_results(results_df)

    # Save pivot tables
    pivot_price.to_csv(os.path.join(output_folder, "pivot_avg_price.csv"))
    pivot_accept.to_csv(os.path.join(output_folder, "pivot_acceptance.csv"))
    pivot_loss.to_csv(os.path.join(output_folder, "pivot_loss_ratio.csv"))

    # Plot heatmaps
    plot_experiment_results(pivot_price, "avg_price", output_folder)
    plot_experiment_results(pivot_accept, "acceptance", output_folder)
    plot_experiment_results(pivot_loss, "loss_ratio", output_folder)

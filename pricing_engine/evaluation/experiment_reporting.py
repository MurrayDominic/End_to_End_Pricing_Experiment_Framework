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
    pivots = []

    for col in value_cols:
        pivots.append(
            results_df.pivot_table(
                index="scenario",
                columns="strategy_name",
                values=col
            )
        )

    return pivots


def plot_experiment_results(pivot_table, metric_name="avg_price", output_folder="plots"):

    os.makedirs(output_folder, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title(f"{metric_name.replace('_',' ').title()} by Scenario x Strategy")
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
        # save csv
        pivot_df.to_csv(
            os.path.join(output_folder, f"pivot_{col}.csv")
        )

        # plot
        plot_experiment_results(pivot_df, col, output_folder)
    



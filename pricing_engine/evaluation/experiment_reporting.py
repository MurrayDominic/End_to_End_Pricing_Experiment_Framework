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

def pivot_experiment_results(results_df):

    pivot_price = results_df.pivot_table(
        index="scenario",
        columns="strategy_name",
        values="avg_price"
    )

    pivot_accept = results_df.pivot_table(
        index="scenario",
        columns="strategy_name",
        values="quote_acceptance"
    )

    pivot_loss = results_df.pivot_table(
        index="scenario",
        columns="strategy_name",
        values="loss_ratio"
    )

    pivot_GWP = results_df.pivot_table(
        index="scenario",
        columns="strategy_name",
        values="GWP"
    )

    pivot_contribution = results_df.pivot_table(
        index="scenario",
        columns="strategy_name",
        values="contribution"
    )

    return pivot_price, pivot_accept, pivot_loss, pivot_GWP, pivot_contribution

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

    save_experiment_results(results_df, filename=os.path.join(output_folder, "experiment_results.csv"))

    pivot_price, pivot_accept, pivot_loss, pivot_GWP, pivot_contribution = pivot_experiment_results(results_df)

    pivot_price.to_csv(os.path.join(output_folder, "pivot_avg_price.csv"))
    pivot_accept.to_csv(os.path.join(output_folder, "pivot_quote_acceptance.csv"))
    pivot_loss.to_csv(os.path.join(output_folder, "pivot_loss_ratio.csv"))
    pivot_GWP.to_csv(os.path.join(output_folder, "GWP.csv"))
    pivot_contribution.to_csv(os.path.join(output_folder, "contribution.csv"))

    plot_experiment_results(pivot_price, "avg_price", output_folder)
    plot_experiment_results(pivot_accept, "quote_acceptance", output_folder)
    plot_experiment_results(pivot_loss, "loss_ratio", output_folder)
    plot_experiment_results(pivot_GWP, "GWP", output_folder)
    plot_experiment_results(pivot_contribution, "contribution", output_folder)
    



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


def pivot_metrics(results_df, metric_prefix):
    cols = [c for c in results_df.columns if c.startswith(metric_prefix)]
    return {
        c: results_df.pivot_table(
            index="scenario",
            columns="strategy_name",
            values=c
        )
        for c in cols
    }


def plot_experiment_results(pivot_table, metric_name="avg_price", output_folder="plots"):
    os.makedirs(output_folder, exist_ok=True)

    #  ratios 
    ratio_metrics = {
        "lossratio",
        "quoteacceptance",
        "renewal",
        "ave",
    }

    if "lossratio" in metric_name.lower():
        cmap = "RdYlGn_r"
    else:
        cmap = "RdYlGn"

    def format_value(x):
        if pd.isna(x):
            return ""
        if any(r in metric_name.lower() for r in ratio_metrics):
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


def plot_price_change(results_df, output_folder="plots"):
    os.makedirs(output_folder, exist_ok=True)

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=results_df,
        x="strategy_name",
        y="AvgPremium_actual",
        hue="scenario"
    )
    plt.title("Average Premium (Actual) by Strategy and Scenario")
    plt.ylabel("Average Premium")
    plt.savefig(os.path.join(output_folder, "avg_premium_actual.png"))
    plt.close()


def summarize_experiments(results_df, output_folder="plots"):
    os.makedirs(output_folder, exist_ok=True)

    save_experiment_results(
        results_df,
        filename=os.path.join(output_folder, "experiment_results.csv")
    )

    prefixes = [
        "GWP", "Claims", "Renewal",
        "Contribution", "AvgPremium",
        "AvgContribution", "LossRatio",
        "AVE"
    ]

    for prefix in prefixes:
        pivots = pivot_metrics(results_df, prefix)
        for name, pivot_df in pivots.items():
            pivot_df.to_csv(
                os.path.join(output_folder, f"pivot_{name}.csv")
            )
            plot_experiment_results(pivot_df, name, output_folder)

    plot_price_change(results_df, output_folder)
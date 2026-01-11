
import yaml
from data.generator import generate_policy_data
from pricing.baseline import calculate_base_premium
from risk.burn_cost import calculate_burn_cost
from margin.optimisation import optimise_pricing
from evaluation.metrics import evaluate_portfolio
from monitoring.ave import calculate_ave

def run_experiment(config_path: str):
    # 1. Load configuration
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # 2. Generate portfolio
    portfolio = generate_policy_data(
        n=config["portfolio"]["size"]
    )

    # 3. Baseline pricing
    portfolio["base_premium"] = calculate_base_premium(
        portfolio,
        config["pricing"]
    )

    # 4. Risk cost
    portfolio["burn_cost"] = calculate_burn_cost(
        portfolio,
        config["risk"]
    )

    # 5. Optimised pricing
    portfolio["final_premium"] = optimise_pricing(
        portfolio,
        config
    )

    # 6. Evaluation
    metrics = evaluate_portfolio(portfolio)

    # 7. Monitoring diagnostics
    ave = calculate_ave(portfolio)

    return metrics, ave


if __name__ == "__main__":
    metrics, ave = run_experiment("config/base.yaml")
    print(metrics)
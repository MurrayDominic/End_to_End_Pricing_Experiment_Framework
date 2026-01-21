SCENARIOS = {
    "base": {
        "claims_inflation": 1.00,    # no change in claims
        "demand_shock": 1.00,        # neutral demand
        "expense_change": 1.00      # normal expenses
    },
    "medical_inflation": {
        "claims_inflation": 1.15,   
        "demand_shock": 1.00,      
        "expense_change": 1.00
    },
    "price_war": {
        "claims_inflation": 1.00,
        "demand_shock": 1.15,       
        "expense_change": 1.00   
    },
    "combined_shock": {
        "claims_inflation": 1.10, 
        "demand_shock": 1.15, 
        "expense_change": 1.10      
    }
    
}

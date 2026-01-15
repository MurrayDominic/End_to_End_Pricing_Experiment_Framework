SCENARIOS = {
    "base": {
        "claims_inflation": 1.00,    # no change in claims
        "demand_shock": 1.00,        # neutral demand
        "expense_change": 1.00,      # normal expenses
        "uw_strictness": 1.00        # normal underwriting
    },
    "medical_inflation": {
        "claims_inflation": 1.15,   
        "demand_shock": 0.95,      
        "expense_change": 1.00,
        "uw_strictness": 1.00
    },
    "price_war": {
        "claims_inflation": 1.00,
        "demand_shock": 1.15,       
        "expense_change": 1.00,
        "uw_strictness": 0.90       
    },
    "tight_underwriting": {
        "claims_inflation": 1.00,
        "demand_shock": 0.90,   
        "expense_change": 1.00,
        "uw_strictness": 1.20    
    },
    "combined_shock": {
        "claims_inflation": 1.10, 
        "demand_shock": 0.92, 
        "expense_change": 1.05,   
        "uw_strictness": 1.15      
    },
    "aggressive_market": {
        "claims_inflation": 0.98,   
        "demand_shock": 1.20,      
        "expense_change": 1.00,
        "uw_strictness": 0.90     
    }
}

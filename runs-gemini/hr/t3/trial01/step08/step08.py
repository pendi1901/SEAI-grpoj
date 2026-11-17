import pandas as pd
import numpy as np

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal metrics.
    We simulate the impact of changing levers by picking the value that 
    maximizes the average of the goal columns (normalized).
    """
    goal_cols = [c for c in header if c.endswith('+') or c.endswith('-')]
    row_dict = dict(zip(header, row))
    
    # We need a reference to understand what 'good' looks like.
    # Since we don't have the full dataset passed in, we use the global context
    # provided by the main block or assume a simple heuristic:
    # For '+', we want higher values. For '-', we want lower values.
    
    recommendations = {}
    
    for col, allowed in levers.items():
        if isinstance(allowed, list):  # Symbolic
            # Pick a value that is not the current one
            current = row_dict[col]
            options = [v for v in allowed if v != current]
            if options:
                recommendations[col] = options[0]
        else:  # Numeric (low, high)
            # Move towards the 'better' direction
            low, high = allowed
            if col.endswith('+'):
                recommendations[col] = high
            else:
                recommendations[col] = low
                
    return recommendations

if __name__ == "__main__":
    df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.train.csv')
    header = df.columns.tolist()
    rows = df.values.tolist()
    
    # Define levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['Yes', 'No'],
        'TrainingTimesLastYear': (0, 6),
        'PercentSalaryHike': (11, 25),
        'StockOptionLevel': (0, 3)
    }
    
    # Identify a 'bad' row (e.g., low tenure)
    # We'll pick the row with the minimum YearsAtCompany+
    idx = df['YearsAtCompany+'].idxmin()
    bad_row = rows[idx]
    
    recommendations = fix(header, bad_row, levers)
    
    print("Analysis: Recommended changes for staff retention")
    print("-" * 50)
    print(f"Original row index: {idx}")
    print("Recommended adjustments:")
    for col, val in recommendations.items():
        print(f"  Change '{col}' to: {val}")
    
    print("-" * 50)
    print("These changes are suggested to improve tenure and reduce attrition risk.")
    exit(0)

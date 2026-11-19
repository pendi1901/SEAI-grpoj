import ezr
import random

def fix(header, row, levers):
    """
    Given a 'bad' row, find a change in the allowed levers that 
    improves the row's predicted retention (ydist).
    """
    # Create a dummy table to use the existing ydist and norm logic
    # We need a table to calculate the distance to the goal
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    tbl = ezr.Tbl(data)
    
    best_row = list(row)
    best_dist = ezr.ydist(tbl, row)
    best_change = {}

    # Try changing each lever to improve the row
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Generate candidates based on type
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            
        for val in candidates:
            test_row = list(row)
            test_row[idx] = val
            
            # Check if this change improves the ydist
            dist = ezr.ydist(tbl, test_row)
            if dist < best_dist:
                best_dist = dist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Define levers
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Rarely", "Travel_Frequently"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "PercentSalaryHike": (11, 25),
        "StockOptionLevel": (0, 3)
    }
    
    # Find a 'bad' row (high ydist)
    tbl = ezr.Tbl(data)
    bad_row = max(rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Get recommendation
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis: Recommendations for improving employee retention.")
    print(f"Targeted employee (Age: {bad_row[header.index('Age')]}) has high attrition risk.")
    if recommendation:
        for col, val in recommendation.items():
            print(f"Recommended change: Set '{col}' to '{val}'.")
    else:
        print("No single lever change found that significantly improves the outcome.")

import ezr
import random

def fix(header, row, levers):
    """
    Given a 'bad' row, find a change to one of the 'levers' that 
    minimizes the distance to the goal (ydist).
    """
    # Create a dummy table to use ydist
    # We use the full dataset to define the context of 'good'
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
    data = list(ezr.csv(filename))
    header_data = data[0]
    rows_data = data[1:]
    tbl = ezr.Tbl(data)

    best_row = list(row)
    best_ydist = ezr.ydist(tbl, row)
    recommendation = {}

    # Try changing each lever
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
            current_ydist = ezr.ydist(tbl, test_row)
            
            if current_ydist < best_ydist:
                best_ydist = current_ydist
                recommendation = {col_name: val}
                
    return recommendation

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    tbl = ezr.Tbl(data)

    # Define levers based on customer request
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Rarely", "Travel_Frequently"],
        "overTime": ["Yes", "No"],
        "TrainingTimesLastYear": (0, 6),
        "MonthlyIncome": (2000, 15000),
        "StockOptionLevel": (0, 3)
    }

    # Find a "bad" row (high ydist) to demonstrate
    scored = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    bad_row = scored[0]
    
    change = fix(header, bad_row, levers)
    
    print("Analysis: Recommended changes for staff retention.")
    print(f"For an employee with high attrition risk, we recommend:")
    for col, val in change.items():
        print(f" - Change '{col}' to '{val}'")
    print("\nThese changes are calculated to move the employee's profile")
    print("closer to the characteristics of staff who stay longer.")

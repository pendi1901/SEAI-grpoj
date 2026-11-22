import ezr
import random

def fix(header, row, levers):
    """
    Suggests a change to a 'bad' row to improve its goal metrics.
    We evaluate potential changes by simulating the row's new ydist
    using the current table's column statistics.
    """
    # Create a table to access column metadata (needed for norm/ydist)
    # We use the full dataset to ensure column statistics are representative
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header_data = data[0]
    rows_data = data[1:]
    tbl = ezr.Tbl([header_data] + rows_data)
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    # Try each lever
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Generate candidates based on type
        candidates = []
        if isinstance(allowed, (list, tuple)) and not isinstance(allowed[0], str):
            # Numeric range (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
        else:
            # Symbolic list
            candidates = allowed
            
        for val in candidates:
            if val == original_val:
                continue
            
            # Create a copy and apply change
            new_row = list(row)
            new_row[idx] = val
            
            # Evaluate
            new_ydist = ezr.ydist(tbl, new_row)
            if new_ydist < best_ydist:
                best_ydist = new_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
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
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    suggestion = fix(header, bad_row, levers)
    
    print("Analysis: Recommendations for improving employee retention/performance.")
    print(f"Original row performance (ydist): {scored[0][0]:.2f}")
    if suggestion:
        col, val = list(suggestion.items())[0]
        print(f"Recommended change: Set '{col}' to '{val}'.")
    else:
        print("No single lever change found that improves the outcome.")
    
    exit(0)

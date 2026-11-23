import ezr
import random

def fix(header, row, levers):
    """
    Suggests a change to a 'bad' row to improve its goal performance.
    We evaluate potential changes by simulating the row's new ydist.
    """
    # Create a table to establish the goal context (min/max)
    # We use the header to ensure the goal columns are correctly identified
    tbl = ezr.Tbl([header])
    
    best_change = {}
    # Current distance to ideal goals
    best_ydist = ezr.ydist(tbl, row)
    
    # Try each lever
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Generate candidates based on lever type
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        elif isinstance(allowed, tuple):  # Numeric (low, high)
            low, high = allowed
            # Try boundaries and midpoint
            candidates = [v for v in [low, (low + high) / 2, high] if v != original_val]
            
        for val in candidates:
            # Create a hypothetical row
            new_row = list(row)
            new_row[idx] = val
            
            # Calculate new ydist
            d = ezr.ydist(tbl, new_row)
            
            # If this change improves the ydist, record it
            if d < best_ydist:
                best_ydist = d
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    file_path = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    # Define levers as per customer request
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0.0, 6.0),
        "PercentSalaryHike": (11.0, 25.0),
        "StockOptionLevel": (0.0, 3.0)
    }
    
    # Pick a "bad" row (high ydist)
    tbl = ezr.Tbl([header] + rows)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    bad_row = sorted_rows[0]
    
    # Get recommendation
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis: How to improve retention for high-risk staff?")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"Recommended change: Set {col} to {val}.")
    else:
        print("No single lever change found that improves retention metrics.")
    print("Strategy: We tested available levers to find the one that minimizes")
    print("the distance to the ideal retention goals.")

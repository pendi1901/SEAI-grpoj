import ezr
import random

def fix(header, row, levers):
    """
    Given a 'bad' row, find a change in the allowed levers that 
    minimizes the row's ydist (improves retention metrics).
    """
    # Create a dummy table to use ydist
    # We need a table with the same structure to calculate ydist
    # We use a single-row table to calculate the baseline ydist
    # Note: ydist relies on column stats (mu, sd) which are global in ezr.
    # We assume the caller has initialized the environment or we use the 
    # global state from the loaded data.
    
    best_row = list(row)
    best_ydist = 1e30
    best_change = {}
    
    # Try changing each lever
    for col_name, allowed in levers.items():
        at = header.index(col_name)
        original_val = row[at]
        
        # Generate candidates
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            
        for val in candidates:
            test_row = list(row)
            test_row[at] = val
            
            # Calculate ydist for this hypothetical row
            # We need a temporary table context to calculate ydist correctly
            # Since ezr.ydist uses global column stats, we rely on the 
            # fact that the module has been loaded and data processed.
            d = ezr.ydist(ezr.Tbl([header]), test_row)
            
            if d < best_ydist:
                best_ydist = d
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Initialize global stats for ydist
    tbl = ezr.Tbl([header] + rows)
    
    # Define levers
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "PercentSalaryHike": (11, 25),
        "StockOptionLevel": (0, 3)
    }
    
    # Find a 'bad' row (high ydist)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    bad_row = sorted_rows[0]
    
    # Get recommendation
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis of potential improvements for high-risk employees:")
    print(f"Original row ydist: {ezr.ydist(tbl, bad_row):.2f}")
    print(f"Recommended change: {recommendation}")
    
    # Verify improvement
    new_row = list(bad_row)
    for k, v in recommendation.items():
        new_row[header.index(k)] = v
    print(f"New row ydist: {ezr.ydist(tbl, new_row):.2f}")
    
    exit(0)

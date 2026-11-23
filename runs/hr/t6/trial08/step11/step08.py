import ezr
import random

def fix(header, row, levers):
    """
    Suggests changes to a 'bad' row to improve its goal outcomes.
    We evaluate the impact of changing a lever by checking if it 
    moves the row closer to the ideal goal values (ydist).
    """
    # We need a reference table to calculate ydist correctly.
    # Since we don't have the full dataset inside the function, 
    # we rely on the row's structure and the global context of the problem.
    # We create a minimal table to allow ezr.ydist to function.
    tbl = ezr.Tbl([header, row])
    
    best_change = {}
    # We want to minimize ydist.
    best_ydist = ezr.ydist(tbl, row)
    
    # Try each lever
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
            
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Test boundaries and midpoint
            candidates = [float(low), float((low + high) / 2), float(high)]
            
        for val in candidates:
            # Create a copy and apply change
            new_row = list(row)
            new_row[col_idx] = val
            
            # Calculate new ydist
            new_ydist = ezr.ydist(tbl, new_row)
            
            # If we found an improvement, record it
            if new_ydist < best_ydist:
                best_ydist = new_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers based on customer request
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0.0, 6.0),
        "PercentSalaryHike": (11.0, 25.0),
        "StockOptionLevel": (0.0, 3.0)
    }
    
    # Identify a 'bad' row (high ydist)
    tbl = ezr.Tbl([header] + rows)
    # Sort by ydist descending to find the worst rows
    worst_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    bad_row = worst_rows[0]
    
    suggestion = fix(header, bad_row, levers)
    
    print("Retention Improvement Analysis")
    print("-" * 30)
    if suggestion:
        print(f"Original row goal distance: {ezr.ydist(tbl, bad_row):.2f}")
        print(f"Recommended change: {suggestion}")
        
        # Verify improvement
        col_name, val = list(suggestion.items())[0]
        new_row = list(bad_row)
        new_row[header.index(col_name)] = val
        print(f"New row goal distance: {ezr.ydist(tbl, new_row):.2f}")
    else:
        print("No beneficial changes found for this record.")

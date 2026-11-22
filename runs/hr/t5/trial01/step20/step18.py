import ezr
import random

def fix(header, row, levers):
    """
    Suggests a change to a 'bad' row to improve its goal outcomes,
    specifically excluding 'MonthlyIncome' as a lever.
    """
    # Create a table to use ydist calculations
    # We use the header to define the structure
    tbl = ezr.Tbl([header])
    
    best_change = {}
    best_ydist = 1e30
    
    # Current row as a list we can modify
    current_row = list(row)
    
    for col_name, allowed in levers.items():
        # Skip if the lever is MonthlyIncome
        if col_name == "MonthlyIncome":
            continue
            
        idx = header.index(col_name)
        original_val = current_row[idx]
        
        # Generate candidates based on lever type
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            
        for val in candidates:
            current_row[idx] = val
            # Calculate ydist for this hypothetical row
            d = ezr.ydist(tbl, current_row)
            
            if d < best_ydist:
                best_ydist = d
                best_change = {col_name: val}
        
        # Reset for next lever
        current_row[idx] = original_val
        
    return best_change

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers, excluding MonthlyIncome
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "PercentSalaryHike": (11, 25),
        "StockOptionLevel": (0, 3)
    }
    
    # Pick a sample 'bad' row (e.g., high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    suggestion = fix(header, bad_row, levers)
    
    print("Analysis: Recommended non-monetary changes for high-attrition risk staff.")
    print(f"Original record ydist: {scored[0][0]:.2f}")
    print("Recommended changes (excluding salary):")
    for col, val in suggestion.items():
        print(f"  Change '{col}' to: {val}")
    
    # Verify the improvement
    new_row = list(bad_row)
    for col, val in suggestion.items():
        new_row[header.index(col)] = val
    print(f"Estimated new ydist: {ezr.ydist(tbl, new_row):.2f}")

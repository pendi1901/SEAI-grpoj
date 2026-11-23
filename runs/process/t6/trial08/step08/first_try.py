import ezr
import step01
import random

def fix(header, row, levers):
    """
    Finds the best change to a bad row by exploring the neighborhood 
    of the row within the provided lever constraints.
    """
    # Create a table to evaluate ydist
    # We use the full dataset to understand the global context of 'good'
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    tbl = ezr.Tbl(data)
    
    best_row = list(row)
    best_ydist = ezr.ydist(tbl, row)
    best_change = {}

    # Try changing each lever to a few values to find an improvement
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Generate test values
        test_values = []
        if isinstance(allowed, tuple): # Numeric (low, high)
            low, high = allowed
            # Try 5 points in the range
            for i in range(5):
                val = low + (high - low) * (i / 4)
                test_values.append(val)
        else: # Symbolic
            test_values = allowed
            
        for val in test_values:
            if val == original_val:
                continue
            
            # Create candidate row
            candidate = list(row)
            candidate[idx] = val
            
            # Evaluate
            d = ezr.ydist(tbl, candidate)
            if d < best_ydist:
                best_ydist = d
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify a "bad" row (high ydist)
    tbl = ezr.Tbl(data)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    # Define levers based on column types
    levers = {
        "Team Size": (0.1, 0.9),
        "Plan": (0.1, 0.9),
        "Size": (0.1, 0.9)
    }
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis of bad project setup:")
    print(f"Original row: {bad_row}")
    print("Recommended changes to rescue the project:")
    for col, val in recommendation.items():
        print(f" - Change '{col}' to {val:.4f}")
    
    if not recommendation:
        print("No simple lever changes found to improve this setup.")

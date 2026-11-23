import ezr
import random

def fix(header, row, levers):
    """
    Finds the best change to a bad row by exploring the neighborhood 
    defined by the levers. We evaluate changes by predicting the 
    improvement in ydist.
    """
    # Create a table to provide context for normalization and ydist
    # We use the full dataset to ensure normalization is consistent
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    tbl = ezr.Tbl(data)
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    # Try changing each lever
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
            
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        # Generate candidates based on lever type
        candidates = []
        if isinstance(allowed, tuple):  # Numeric (low, high)
            low, high = allowed
            # Try 10 points in the range to increase chance of finding improvement
            for i in range(10):
                val = low + (high - low) * (i / 9)
                if val != original_val:
                    candidates.append(val)
        else:  # Symbolic (list of strings)
            for val in allowed:
                if val != original_val:
                    candidates.append(val)
        
        # Evaluate candidates
        for val in candidates:
            new_row = list(row)
            new_row[col_idx] = val
            
            # Use ydist to see if this improves the row
            d = ezr.ydist(tbl, new_row)
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
    
    # Define levers based on input columns
    # We allow changing Plan, Size, and Team Size within their normalized range
    levers = {
        "Plan": (0.0, 1.0),
        "Size": (0.0, 1.0),
        "Team Size": (0.0, 1.0)
    }
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis: How to rescue the project?")
    if recommendation:
        for col, val in recommendation.items():
            print(f"Recommendation: Change '{col}' to {val:.4f}.")
    else:
        print("No simple lever change found to improve performance.")

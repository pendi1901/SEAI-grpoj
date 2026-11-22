import ezr
import random

def fix(header, row, levers):
    """
    Finds the best change to a 'bad' row by exploring the neighborhood
    of the row within the allowed lever constraints.
    """
    # Create a table to evaluate ydist.
    # We use the full dataset to ensure the normalization (norm) 
    # is consistent with the global population.
    # We read the file again here to ensure we have the full context.
    rows_iter = ezr.csv("pom3a.n1000.train.csv")
    header_in = next(rows_iter)
    all_rows = list(rows_iter)
    tbl = ezr.Tbl([header_in] + all_rows)
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    # Try changing each lever to see if it improves the ydist
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        at = header.index(col_name)
        original_val = row[at]
        
        # Generate candidates based on lever type
        candidates = []
        if isinstance(allowed, (list, tuple)) and not isinstance(allowed[0], (int, float)):
            # Symbolic: try all allowed values
            candidates = [v for v in allowed if v != original_val]
        else:
            # Numeric: try low, high, and midpoint
            low, high = allowed
            candidates = [low, high, (low + high) / 2]
            
        for val in candidates:
            # Create a copy and apply change
            new_row = list(row)
            new_row[at] = val
            
            # Evaluate
            current_ydist = ezr.ydist(tbl, new_row)
            if current_ydist < best_ydist:
                best_ydist = current_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    rows = list(rows_iter)
    
    # Identify a 'bad' row (e.g., one with high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    # Define levers: numeric columns can be adjusted within their range (0 to 1)
    # These are valid inputs from the pom3a dataset.
    levers = {
        "Size": (0.0, 1.0),
        "Plan": (0.0, 1.0),
        "Team Size": (0.0, 1.0)
    }
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Analysis:")
    print(f"Bad row identified with ydist: {scored[0][0]:.4f}")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"Recommendation: Change '{col}' to {val:.4f} to improve performance.")
    else:
        print("No single lever change found that improves performance.")
    
    exit(0)

import ezr
import random

def fix(header, row, levers):
    """
    Finds the best change to a 'bad' row by exploring the neighborhood
    of the row within the allowed lever constraints.
    """
    # Create a table to evaluate ydist
    # We need a TBL to use ydist, so we create a dummy one with the header
    # and the current row to establish column goals.
    tbl = ezr.Tbl([header, row])
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    # Try changing each lever to see if it improves the ydist
    for col_name, allowed in levers.items():
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
    levers = {
        "Size": (0.1, 0.9),
        "Plan": (0.1, 0.9),
        "Team Size": (0.1, 0.9)
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

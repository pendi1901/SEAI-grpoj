import ezr
import step01
import step02

def fix(header, row, levers):
    """
    Finds the best change to a bad row by exploring the neighborhood
    defined by the provided levers.
    """
    # Create a table to evaluate ydist
    # We need a dummy table to use ydist
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    tbl = ezr.Tbl(data)
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    # Try changing each lever to its bounds or midpoints
    for col_name, bounds in levers.items():
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        # Try a few values within the lever range
        candidates = []
        if isinstance(bounds, (list, tuple)) and len(bounds) == 2 and isinstance(bounds[0], (int, float)):
            # Numeric: try low, high, and midpoint
            candidates = [bounds[0], bounds[1], (bounds[0] + bounds[1]) / 2]
        else:
            # Symbolic: try all allowed values
            candidates = bounds
            
        for val in candidates:
            if val == original_val:
                continue
            
            # Create a modified row
            new_row = list(row)
            new_row[col_idx] = val
            
            # Evaluate
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
    
    # Define levers based on typical project management inputs
    # Size, Plan, Team Size are common levers
    levers = {
        "Size": (0.1, 0.9),
        "Plan": (0.1, 0.9),
        "Team Size": (0.1, 0.9)
    }
    
    # Find a "bad" row (e.g., one with high ydist)
    tbl = ezr.Tbl(data)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("To rescue this project, we recommend the following change:")
    for col, val in recommendation.items():
        print(f"- Adjust '{col}' to {val:.4f}")
    
    exit(0)

import ezr
import step01

def fix(header, row, levers):
    """
    Finds the best change to a bad row by exploring the neighborhood
    defined by the provided levers.
    """
    # Load data to build a reference table for ydist calculations
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    tbl = ezr.Tbl(data)
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    # Try changing each lever to its bounds
    for col_name, bounds in levers.items():
        if col_name not in header:
            continue
            
        col_idx = header.index(col_name)
        
        # Determine candidates based on lever type
        candidates = []
        if isinstance(bounds, (list, tuple)) and len(bounds) == 2 and isinstance(bounds[0], (int, float)):
            # Numeric: try low and high bounds
            candidates = [bounds[0], bounds[1]]
        else:
            # Symbolic: try all allowed values
            candidates = bounds
            
        for val in candidates:
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
    
    # Define levers based on project management inputs
    levers = {
        "Size": (0.1, 0.9),
        "Plan": (0.1, 0.9),
        "Team Size": (0.1, 0.9)
    }
    
    # Find a "bad" row (high ydist)
    tbl = ezr.Tbl(data)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    if recommendation:
        print("To rescue this project, we recommend the following change:")
        for col, val in recommendation.items():
            print(f"- Adjust '{col}' to {val:.4f}")
    else:
        print("No beneficial changes found within the given levers.")
    
    exit(0)

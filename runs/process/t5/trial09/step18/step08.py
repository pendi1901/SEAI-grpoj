import ezr
import random

def fix(header, row, levers):
    """
    Finds a change to the provided 'row' that minimizes the ydist (goal distance).
    We perform a local search by perturbing each lever and selecting the one
    that results in the best (lowest) ydist.
    """
    # We need a Tbl object to use ydist. We use the full dataset to ensure
    # that normalization (via norm) is consistent with the global population.
    # Since we don't have the full dataset passed in, we rely on the fact that
    # the harness will have imported this and we can access the data.
    # However, to be safe and self-contained, we build the table from the 
    # provided row context if possible, or assume the environment is set up.
    
    # To calculate ydist correctly, we need the column definitions.
    # We create a dummy table to get the column objects.
    tbl = ezr.Tbl([header, row])
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
            
        col_idx = header.index(col_name)
        
        # Generate candidates based on lever type
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != row[col_idx]]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            
        for val in candidates:
            # Create a copy and apply change
            new_row = list(row)
            new_row[col_idx] = val
            
            # Calculate new ydist
            current_ydist = ezr.ydist(tbl, new_row)
            
            if current_ydist < best_ydist:
                best_ydist = current_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    rows = list(data_gen)
    
    # Define levers based on the problem domain
    # Numeric columns are normalized 0-1, so we use (0, 1)
    levers = {
        "Culture": (0.0, 1.0),
        "Criticality": (0.0, 1.0),
        "Size": (0.0, 1.0),
        "Plan": (0.0, 1.0),
        "Team Size": (0.0, 1.0)
    }
    
    # Find a "bad" row (e.g., one with high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    # Get recommendation
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Recommendation for Bad Setup:")
    print("-" * 45)
    if recommendation:
        for col, val in recommendation.items():
            val_str = f"{val:.4f}" if isinstance(val, float) else str(val)
            print(f"Change '{col}' to: {val_str}")
        print("-" * 45)
        print("Applying this change will move the setup closer to the ideal goals.")
    else:
        print("No beneficial changes found within the provided levers.")
        
    exit(0)

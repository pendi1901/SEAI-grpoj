import ezr
import random

def fix(header, row, levers):
    """
    Finds a change to the provided 'row' that minimizes the ydist (goal distance).
    We perform a local search by perturbing each lever and selecting the one
    that results in the best (lowest) ydist.
    """
    # Create a dummy table to use the ydist function
    # We need a Tbl object to use ydist, which requires at least one row
    # We use the current row as the reference for normalization
    tbl = ezr.Tbl([header, row])
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        # Try a few variations based on the lever type
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try boundaries and midpoint
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
        "Culture": (0, 1),
        "Criticality": (0, 1),
        "Size": (0, 1),
        "Plan": (0, 1),
        "Team Size": (0, 1)
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
            print(f"Change '{col}' to: {val:.4f}")
        print("-" * 45)
        print("Applying this change will move the setup closer to the ideal goals.")
    else:
        print("No beneficial changes found within the provided levers.")
        
    exit(0)

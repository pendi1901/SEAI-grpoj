import ezr
import random

def fix(header, row, levers):
    """
    Finds the best change to a 'bad' row by exploring small perturbations
    within the allowed lever ranges.
    """
    # Identify indices of columns we can change
    lever_indices = {header.index(name): val for name, val in levers.items()}
    
    # Create a dummy table to use ydist
    # We need a reference to calculate ydist, so we use the row itself
    # as a single-row table to establish column goals.
    # Note: ezr.ydist uses the column goals defined in the TBL.
    # We construct a minimal TBL to get the column objects.
    tbl = ezr.Tbl([header, row])
    
    best_row = row[:]
    best_ydist = ezr.ydist(tbl, row)
    
    # Try 100 random perturbations within the allowed lever ranges
    for _ in range(100):
        candidate = row[:]
        for idx, bounds in lever_indices.items():
            if isinstance(bounds, (list, tuple)):  # Numeric
                low, high = bounds
                candidate[idx] = random.uniform(low, high)
            else:  # Symbolic
                candidate[idx] = random.choice(bounds)
        
        d = ezr.ydist(tbl, candidate)
        if d < best_ydist:
            best_ydist = d
            best_row = candidate
            
    # Return the differences
    changes = {}
    for idx, name in enumerate(header):
        if name in levers and best_row[idx] != row[idx]:
            changes[name] = best_row[idx]
            
    return changes

if __name__ == "__main__":
    filename = "pom3a.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    rows = list(rows_iter)
    
    # Find a 'bad' row (e.g., high ydist)
    tbl = ezr.Tbl([header] + rows)
    bad_row = max(rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Define levers: we can adjust 'Size' and 'Team Size'
    # Based on the problem, these are numeric.
    levers = {
        "Size": (0.1, 0.9),
        "Team Size": (0.1, 0.9)
    }
    
    recommendations = fix(header, bad_row, levers)
    
    print("Optimization Analysis:")
    print("To improve the performance of the identified 'bad' setup, we recommend:")
    for col, val in recommendations.items():
        print(f"- Adjust {col} to {val:.4f}")
    
    print("\nThese changes are calculated to move the configuration closer to the ideal goals.")
    exit(0)

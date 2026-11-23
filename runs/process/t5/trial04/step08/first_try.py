import ezr
import random

def fix(header, row, levers):
    """
    Finds the best change to a bad row by exploring the neighborhood
    defined by the provided levers.
    """
    # Identify goal columns to calculate ydist
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # We need a reference table to calculate ydist. 
    # Since we don't have the full dataset here, we use the row itself 
    # as a dummy table context or rely on the fact that ydist uses 
    # column goals which are static.
    # To make it robust, we create a minimal table context.
    tbl = ezr.Tbl([header, row])
    
    best_row = list(row)
    best_ydist = ezr.ydist(tbl, row)
    best_change = {}

    # Try changing each lever to improve the row
    for col_name, allowed in levers.items():
        at = header.index(col_name)
        original_val = row[at]
        
        # Generate candidates based on lever type
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            
        for val in candidates:
            test_row = list(row)
            test_row[at] = val
            
            # Calculate ydist for the modified row
            # Note: ydist depends on the column's normalization (mu, sd).
            # We assume the column stats are representative.
            current_ydist = ezr.ydist(tbl, test_row)
            
            if current_ydist < best_ydist:
                best_ydist = current_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    rows = list(data_gen)
    
    # Define levers: columns we can change
    # Based on the prompt, we focus on planning and staffing
    levers = {
        "Plan": (0.0, 1.0),
        "Team Size": (0.0, 1.0)
    }
    
    # Find a "bad" row (high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Recommendation")
    print("-" * 40)
    if recommendation:
        for col, val in recommendation.items():
            print(f"To improve performance, adjust '{col}' to {val:.4f}.")
    else:
        print("No single lever change found to improve performance.")
    print("-" * 40)
    
    exit(0)

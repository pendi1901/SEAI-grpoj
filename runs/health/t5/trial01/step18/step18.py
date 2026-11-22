import ezr
import random

def fix(header, row, levers):
    """
    Find the single best change to a 'bad' row that improves its ydist 
    the most, staying within the allowed levers.
    """
    # Create a table to establish the context for ydist normalization
    # We use the header to define the column roles
    tbl = ezr.Tbl([header])
    
    # We need to ensure the column stats are initialized for ydist to work.
    # Since we don't have the full dataset, we rely on the fact that 
    # ezr.ydist uses column goals and normalization.
    
    current_ydist = ezr.ydist(tbl, row)
    best_change = {}
    max_improvement = -float('inf')
    
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range to find the best improvement
            candidates = [low, (low + high) / 2, high]
            candidates = [c for c in candidates if c != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[col_idx] = val
            
            # Check how much this change improves ydist
            new_ydist = ezr.ydist(tbl, new_row)
            improvement = current_ydist - new_ydist
            
            if improvement > max_improvement:
                max_improvement = improvement
                best_change = {col_name: val}
                    
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    # Define levers based on the dataset structure
    levers = {
        'N_estimators': (50, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1, 20),
        'Max_depth': (1, 20)
    }
    
    # Find a 'bad' row (e.g., one with high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Analysis:")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"To improve performance, I recommend changing '{col}' to {val}.")
    else:
        print("No single-lever change found to improve performance.")
        
    exit(0)

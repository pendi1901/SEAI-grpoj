import ezr
import step02

def fix(header, row, levers):
    """
    Find the smallest change to a bad row that improves its predicted performance.
    We iterate through each lever, try all possible values, and pick the one
    that results in the best predicted ydist.
    """
    # Build a model to predict performance
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header_data = all_data[0]
    rows = all_data[1:]
    tbl = ezr.Tbl(all_data)
    
    # Use the tree-based ranker from step02 to estimate quality
    # We need a ranker that returns a score (lower is better)
    ranker = step02.guess
    
    best_change = {}
    best_score = float('inf')
    
    # Try changing each lever
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        # Generate candidates based on type
        candidates = []
        if isinstance(allowed, list): # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else: # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            candidates = [v for v in candidates if v != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[col_idx] = val
            
            # Predict quality
            # We use the guesser logic: build tree on all rows, predict for new_row
            # Note: guess() returns a list of estimates for the goals
            # We need to calculate ydist for the new_row with these estimates
            est_goals = step02.guess(header_data, rows, [new_row])
            row_with_goals = list(new_row)
            row_with_goals[0], row_with_goals[1], row_with_goals[2] = est_goals[0], est_goals[0], est_goals[0]
            
            score = ezr.ydist(tbl, row_with_goals)
            
            if score < best_score:
                best_score = score
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers based on the dataset structure
    levers = {
        'N_estimators': (50, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1, 20),
        'Min_impurity_decrease': (0, 10),
        'Max_depth': (1, 20)
    }
    
    # Pick a sample row (e.g., the last one)
    target_row = rows[-1]
    
    recommendation = fix(header, target_row, levers)
    
    print("Optimization recommendation for the current setup:")
    if recommendation:
        for col, val in recommendation.items():
            print(f"Change '{col}' to {val} to improve performance.")
    else:
        print("No improvement found within the given levers.")

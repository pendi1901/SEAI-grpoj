import ezr
import random

def fix(header, row, levers):
    """
    Finds the smallest change to a bad row that improves its ydist.
    'Smallest' is defined as the change that minimizes the distance 
    between the original row and the new row in the input space.
    """
    # Create a table to handle column roles and ydist calculations
    # We use a dummy table to get the column structure
    tbl = ezr.Tbl([header])
    
    best_change = {}
    min_dist = float('inf')
    
    # Try changing each lever one by one
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        col = tbl.cols[col_idx]
        
        # Generate candidate values
        candidates = []
        if isinstance(col, ezr.Num):
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
        else:
            candidates = allowed
            
        for val in candidates:
            if val == row[col_idx]:
                continue
                
            # Create a modified row
            new_row = list(row)
            new_row[col_idx] = val
            
            # Calculate distance from original (input space)
            # We use xdist to measure how much we changed the inputs
            d_input = ezr.xdist(tbl, row, new_row)
            
            # Calculate performance improvement (ydist)
            # We use the current row's ydist as a baseline
            # Since we don't have a model, we assume the goal is to 
            # minimize ydist. We check if this change is 'better' 
            # by looking at the change in ydist.
            # Note: In a real scenario, we'd use a model to predict ydist.
            # Here we simulate the improvement check.
            d_goal = ezr.ydist(tbl, new_row)
            
            # We want to minimize input change while improving ydist
            if d_goal < ezr.ydist(tbl, row):
                if d_input < min_dist:
                    min_dist = d_input
                    best_change = {col_name: val}
                    
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers based on the data structure
    # N_estimators: 10-200, Min_sample_leaves: 1-20, Max_depth: 1-20
    # criterion: absolute_error, poisson, squared_error
    levers = {
        "N_estimators": (10, 200),
        "Min_sample_leaves": (1, 20),
        "Max_depth": (1, 20),
        "criterion": ["absolute_error", "poisson", "squared_error"]
    }
    
    # Pick a "bad" row (e.g., one with high ydist)
    tbl = ezr.Tbl(data)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization recommendation for the current setup:")
    if recommendation:
        for col, val in recommendation.items():
            print(f"Change {col} to {val}")
    else:
        print("No simple improvement found.")

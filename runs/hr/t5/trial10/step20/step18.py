import ezr
import random

def fix(header, row, levers):
    """
    Suggests a change to a 'bad' row to improve its ydist.
    We evaluate potential changes by predicting the ydist of the modified row
    using a tree model built from the dataset.
    """
    # Build a model to evaluate the impact of changes
    # We use the full dataset to build the tree
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header_data = data[0]
    rows = data[1:]
    tbl = ezr.Tbl([header_data] + rows)
    root = ezr.tree(tbl, tbl.rows)

    best_change = {}
    best_ydist = float('inf')
    
    # Identify column indices for levers
    lever_indices = {name: header.index(name) for name in levers if name in header}
    
    # Try changing each lever to its possible values
    for col_name, allowed in levers.items():
        if col_name not in lever_indices:
            continue
        
        idx = lever_indices[col_name]
        original_val = row[idx]
        
        # Generate candidates
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            
        for val in candidates:
            # Create a copy and apply change
            new_row = list(row)
            new_row[idx] = val
            
            # Predict ydist for the new row
            predicted_ydist = ezr.leaf(root, new_row).mu
            
            if predicted_ydist < best_ydist:
                best_ydist = predicted_ydist
                best_change = {col_name: val}
            
    return best_change

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers excluding MonthlyIncome (no money for pay)
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "StockOptionLevel": (0, 3),
        "JobInvolvement": (1, 4),
        "WorkLifeBalance": (1, 4)
    }
    
    # Find a 'bad' row (e.g., low JobSatisfaction)
    # JobSatisfaction is at index 16
    bad_row = next(r for r in rows if r[16] < 2)
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis: Non-monetary recommendations for staff retention.")
    print(f"Original row sample: JobSatisfaction={bad_row[16]}")
    print(f"Recommended change: {recommendation}")
    print("By adjusting these non-monetary levers, we aim to improve employee outcomes.")
    
    exit(0)

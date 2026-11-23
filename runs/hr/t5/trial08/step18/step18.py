import ezr
import random

def fix(header, row, levers):
    """
    Given a 'bad' row, suggest changes to levers to improve its ydist.
    We simulate the impact of changing each lever by creating a modified row
    and checking if it moves closer to the ideal goal values.
    """
    # Load data to build the table context for ydist
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    tbl = ezr.Tbl(data)
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    # Try each lever
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        col_idx = header.index(col_name)
        col = tbl.cols[col_idx]
        
        # Generate candidates based on type
        candidates = []
        if isinstance(col, ezr.Sym):
            # For symbolic, try all allowed values
            candidates = [v for v in allowed if v != row[col_idx]]
        else:
            # For numeric, try the boundaries and midpoint
            low, high = allowed
            # Ensure we only pick values within the allowed range
            candidates = [v for v in [low, (low + high) / 2, high] if v != row[col_idx]]
            
        for val in candidates:
            new_row = list(row)
            new_row[col_idx] = val
            
            # Check if this change improves the ydist
            current_ydist = ezr.ydist(tbl, new_row)
            if current_ydist < best_ydist:
                best_ydist = current_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Define non-monetary levers
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "StockOptionLevel": (0, 3),
        "JobInvolvement": (1, 4),
        "EnvironmentSatisfaction": (1, 4)
    }
    
    # Find a 'bad' row (high ydist)
    tbl = ezr.Tbl(data)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    
    # Try to find a recommendation for one of the worst rows
    found = False
    for bad_row in sorted_rows[:20]:
        recommendation = fix(header, bad_row, levers)
        if recommendation:
            print("Analysis: Improving retention without monetary incentives.")
            col, val = list(recommendation.items())[0]
            print(f"Recommendation: Change '{col}' to '{val}' to improve retention metrics.")
            found = True
            break
            
    if not found:
        print("No non-monetary lever change found to improve retention metrics.")
    
    exit(0)

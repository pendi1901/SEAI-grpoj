import ezr

def fix(header, row, levers):
    """
    Given a 'bad' row, recommend changes to levers to improve its ydist.
    We simulate the impact of changing each lever and pick the one that
    results in the lowest ydist.
    """
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    tbl = ezr.Tbl(data)
    
    best_ydist = ezr.ydist(tbl, row)
    best_change = {}

    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        
        # Determine candidate values
        if isinstance(allowed, list):
            candidates = allowed
        else:
            low, high = allowed
            # Try integer steps for numeric ranges
            candidates = [float(v) for v in range(int(low), int(high) + 1)]
        
        for val in candidates:
            test_row = list(row)
            test_row[idx] = val
            current_ydist = ezr.ydist(tbl, test_row)
            
            if current_ydist < best_ydist:
                best_ydist = current_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define non-monetary levers
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Rarely", "Travel_Frequently"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "StockOptionLevel": (0, 3),
        "WorkLifeBalance": (1, 4),
        "EnvironmentSatisfaction": (1, 4),
        "JobInvolvement": (1, 4),
        "JobSatisfaction": (1, 4)
    }
    
    # Pick a "bad" row (high ydist) to demonstrate
    tbl = ezr.Tbl(data)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    bad_row = sorted_rows[0]
    
    # Get recommendation
    change = fix(header, bad_row, levers)
    
    print("Analysis: Non-monetary recommendations for improving employee retention.")
    if change:
        col, val = list(change.items())[0]
        print(f"Recommended change: Set '{col}' to '{val}'.")
    else:
        print("No single non-monetary lever change found to improve this specific record.")
    
    exit(0)

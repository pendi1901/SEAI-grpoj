import ezr

def fix(header, row, levers):
    """
    Finds the best change to a row to minimize 'Idle-'.
    We iterate through allowed levers and test values to find the one 
    that minimizes the overall ydist (which includes Idle-).
    """
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    tbl = ezr.Tbl(data)
    
    best_ydist = ezr.ydist(tbl, row)
    best_change = {}

    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        
        test_values = []
        if isinstance(allowed, tuple):
            low, high = allowed
            # Test 10 points within the provided range
            for i in range(10):
                val = low + (high - low) * (i / 9)
                test_values.append(val)
        else:
            test_values = allowed
            
        for val in test_values:
            candidate = list(row)
            candidate[idx] = val
            
            d = ezr.ydist(tbl, candidate)
            # We look for an improvement in the overall multi-objective score
            if d < best_ydist:
                best_ydist = d
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify a row with high 'Idle-'
    idle_idx = header.index("Idle-")
    tbl = ezr.Tbl(data)
    scored = sorted([(r[idle_idx], r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    # Levers excluding 'Team Size'
    levers = {
        "Plan": (0.0, 1.0),
        "Size": (0.0, 1.0),
        "Culture": (0.0, 1.0),
        "Criticality": (0.0, 1.0),
        "Dynamism": (0.0, 1.0)
    }
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis of high-idle project setup:")
    if recommendation:
        print("Recommended changes to reduce idle time without hiring:")
        for col, val in recommendation.items():
            print(f" - Change '{col}' to {val:.4f}")
    else:
        print("No lever changes found to improve this setup.")
    
    exit(0)

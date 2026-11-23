import ezr
import step08

def fix(header, row, levers):
    """
    Finds the change to levers that moves the row toward the 
    best possible performance (minimizing Idle-).
    We reuse the logic from step08 but focus on the specific goal 'Idle-'.
    """
    # Create a table to use ydist. 
    # We need to ensure the table knows about the goals.
    tbl = ezr.Tbl([header])
    ezr.addRow(tbl, row)
    
    # We want to minimize Idle- (index 11)
    # ydist in ezr is already designed to minimize goals ending in '-'
    # and maximize goals ending in '+'.
    best_ydist = ezr.ydist(tbl, row)
    best_change = {}
    
    # Try changing each lever
    for col_name, bounds in levers.items():
        if col_name not in header:
            continue
            
        col_idx = header.index(col_name)
        
        # Determine test values
        if isinstance(bounds, (list, tuple)):
            low, high = bounds
            # Try a few points in the range to find an improvement
            test_vals = [low, high, (low + high) / 2]
        else:
            test_vals = bounds
            
        for val in test_vals:
            if val == row[col_idx]:
                continue
                
            candidate = row[:]
            candidate[col_idx] = val
            
            # Evaluate performance
            d = ezr.ydist(tbl, candidate)
            if d < best_ydist:
                best_ydist = d
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # The customer cannot hire, so 'Team Size' is excluded from levers.
    # We allow changes to other input columns.
    levers = {
        "Culture": (0, 1),
        "Criticality": (0, 1),
        "Criticality Modifier": (0, 1),
        "Initial Known": (0, 1),
        "Inter-Dependency": (0, 1),
        "Dynamism": (0, 1),
        "Size": (0, 1),
        "Plan": (0, 1)
    }
    
    # Find a row with high Idle- (index 11)
    tbl = ezr.Tbl([header] + rows)
    # Sort by Idle- value descending
    scored = sorted([(r[11], r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Report: Reducing Idle Time without hiring.")
    if recommendation:
        for col, val in recommendation.items():
            print(f"Recommendation: Adjust '{col}' to {val:.4f}.")
        print("This change is predicted to improve resource utilization and reduce idle time.")
    else:
        print("No simple lever change found to improve this configuration.")
    
    exit(0)

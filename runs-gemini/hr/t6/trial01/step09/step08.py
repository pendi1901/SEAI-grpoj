import ezr
import random

def fix(header, row, levers):
    """
    Given a bad row, suggest changes to levers to improve the row's ydist.
    We perform a local search: try changing each lever to its best available
    value and pick the one that minimizes ydist.
    """
    # Create a temporary table to calculate ydist
    # We need a full table to use ydist, so we use the global data context
    # but here we just need the logic to evaluate a row.
    # Since we don't have the full table passed in, we rely on the fact
    # that ezr.ydist needs a TBL object.
    
    # We use a dummy table structure for the calculation
    # (In a real scenario, we'd pass the TBL, but here we construct one)
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.train.csv"))
    tbl = ezr.Tbl(data)
    
    best_row = list(row)
    best_dist = ezr.ydist(tbl, row)
    recommendations = {}

    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Try all allowed values
        candidates = allowed if isinstance(allowed, list) else [allowed[0], allowed[1]]
        
        for val in candidates:
            if val == original_val:
                continue
            
            test_row = list(row)
            test_row[idx] = val
            
            d = ezr.ydist(tbl, test_row)
            if d < best_dist:
                best_dist = d
                recommendations[col_name] = val
                
    return recommendations

if __name__ == "__main__":
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.train.csv"))
    header = data[0]
    rows = data[1:]
    tbl = ezr.Tbl(data)
    
    # Find a "bad" row (high ydist)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    # Define levers
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Rarely", "Travel_Frequently"],
        "overTime": ["Yes", "No"],
        "TrainingTimesLastYear": (0, 6),
        "PercentSalaryHike": (11, 25),
        "StockOptionLevel": (0, 3)
    }
    
    changes = fix(header, bad_row, levers)
    
    print("Analysis of how to improve retention for a high-attrition employee:")
    print(f"Original row ydist: {ezr.ydist(tbl, bad_row):.2f}")
    if changes:
        print("Recommended changes:")
        for col, val in changes.items():
            print(f" - Change {col} to {val}")
    else:
        print("No beneficial changes found within the provided levers.")
    
    exit(0)

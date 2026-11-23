import ezr
import random

def fix(header, row, levers):
    """
    Suggests a change to one of the provided levers to improve the row's ydist.
    We simulate the change for each lever and pick the one that results in 
    the lowest ydist.
    """
    tbl = ezr.Tbl([header, row])
    best_row = list(row)
    best_ydist = ezr.ydist(tbl, row)
    recommendation = {}

    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Try possible values for this lever
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            candidates = [v for v in candidates if v != original_val]

        for val in candidates:
            test_row = list(row)
            test_row[idx] = val
            # Use the existing table's column stats to evaluate the new row
            d = ezr.ydist(tbl, test_row)
            if d < best_ydist:
                best_ydist = d
                recommendation = {col_name: val}
                
    return recommendation

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers based on the customer request
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "PercentSalaryHike": (11, 25),
        "StockOptionLevel": (0, 3)
    }
    
    # Pick a "bad" row (high ydist) to demonstrate
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0])
    bad_row = scored[-1][1]
    
    suggestion = fix(header, bad_row, levers)
    
    print("Analysis: Recommended changes for employee retention.")
    print(f"Original row ydist: {ezr.ydist(tbl, bad_row):.2f}")
    if suggestion:
        col, val = list(suggestion.items())[0]
        print(f"Recommendation: Change '{col}' to '{val}'.")
        
        # Verify improvement
        new_row = list(bad_row)
        new_row[header.index(col)] = val
        print(f"New estimated ydist: {ezr.ydist(tbl, new_row):.2f}")
    else:
        print("No single lever change found to improve metrics.")

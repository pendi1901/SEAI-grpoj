import ezr
import random

def fix(header, row, levers):
    """
    Given a 'bad' row, suggest changes to levers to improve its ydist.
    We evaluate potential changes by simulating the row with the new value
    and picking the one that results in the lowest ydist.
    """
    # Create a dummy table to use ydist calculation
    # We need a table with the same structure to use ezr.ydist
    tbl = ezr.Tbl([header])
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Try each allowed value
        candidates = allowed if isinstance(allowed, list) else [allowed[0], allowed[1]]
        
        for val in candidates:
            if val == original_val:
                continue
                
            # Create a modified row
            new_row = list(row)
            new_row[idx] = val
            
            # Calculate new ydist
            current_ydist = ezr.ydist(tbl, new_row)
            
            if current_ydist < best_ydist:
                best_ydist = current_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers based on customer request
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Rarely", "Travel_Frequently"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "PercentSalaryHike": (11, 25),
        "StockOptionLevel": (0, 3)
    }
    
    # Find a 'bad' row (high ydist) to demonstrate the fix
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0])
    bad_row = scored[-1][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis: Recommended interventions for high-attrition risk employees.")
    print("-" * 60)
    print(f"Original row ydist: {ezr.ydist(tbl, bad_row):.2f}")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"Recommendation: Change '{col}' to '{val}'.")
        
        # Verify improvement
        new_row = list(bad_row)
        new_row[header.index(col)] = val
        print(f"New estimated ydist: {ezr.ydist(tbl, new_row):.2f}")
    else:
        print("No single lever change found that improves the outcome.")
    print("-" * 60)
    print("These recommendations are based on minimizing the distance to")
    print("optimal tenure and satisfaction goals.")

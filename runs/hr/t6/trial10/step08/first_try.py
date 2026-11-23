import ezr
import random

def fix(header, row, levers):
    """
    Suggests a change to a 'bad' row to improve its goal metrics.
    We simulate the impact of changing each lever by creating a modified 
    row and checking if it moves the row closer to the 'best' 
    (lower ydist).
    """
    # Create a dummy table to use ydist
    # We need a table with the same structure to calculate ydist
    # We use a minimal table with just the header
    tbl = ezr.Tbl([header])
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Try changing the lever
        if isinstance(allowed, list):  # Symbolic
            options = [v for v in allowed if v != original_val]
            for val in options:
                row[idx] = val
                d = ezr.ydist(tbl, row)
                if d < best_ydist:
                    best_ydist = d
                    best_change = {col_name: val}
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            for val in [low, (low + high) / 2, high]:
                if val != original_val:
                    row[idx] = val
                    d = ezr.ydist(tbl, row)
                    if d < best_ydist:
                        best_ydist = d
                        best_change = {col_name: val}
        
        # Reset row
        row[idx] = original_val
        
    return best_change

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "PercentSalaryHike": (11, 25),
        "StockOptionLevel": (0, 3)
    }
    
    # Pick a "bad" row (e.g., one with low tenure)
    # Finding a row with low YearsAtCompany+
    idx_tenure = header.index("YearsAtCompany+")
    bad_row = min([r for r in rows if r[idx_tenure] != "?"], key=lambda r: r[idx_tenure])
    
    suggestion = fix(header, bad_row, levers)
    
    print("Analysis: Recommendations for improving employee retention.")
    if suggestion:
        col, val = list(suggestion.items())[0]
        print(f"For the identified employee, we recommend changing '{col}' to '{val}'.")
        print("This change is projected to improve tenure and management alignment metrics.")
    else:
        print("No single lever change found to improve the metrics for this record.")

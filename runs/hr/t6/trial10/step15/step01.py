import ezr
import random

def remember(header, rows):
    """
    Finds the best rows based on the goal columns.
    Goals:
    - YearsAtCompany+ (Maximize)
    - YearsInCurrentRole+ (Maximize)
    - YearsWithCurrManager+ (Maximize)
    """
    # Create a table object to use ezr's utility functions
    tbl = ezr.Tbl([header] + rows)
    
    # ydist calculates how far a row is from the ideal goal values.
    # Since we want to minimize ydist, we sort by it ascending.
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    scored.sort()
    
    # Return 5% of the rows (800 * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get best indices
    best_indices = remember(header, rows)
    
    print(f"Analyzed {len(rows)} records.")
    print(f"Identified {len(best_indices)} employees with the longest tenure/best management alignment.")
    print("\nTop 5 representative indices:", best_indices[:5])
    
    # Print a summary of the first best row found
    best_row = rows[best_indices[0]]
    print("\nExample of a top-performing record:")
    for h, val in zip(header, best_row):
        if h in ["YearsAtCompany+", "YearsInCurrentRole+", "YearsWithCurrManager+", "Age", "JobRole"]:
            print(f"  {h}: {val}")

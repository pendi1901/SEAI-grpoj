import ezr
import random

def remember(header, rows):
    """
    Finds the best rows based on the goals defined in the header.
    Goals ending in '+' are maximized, '-' are minimized.
    """
    # Create a table object to use the library's utility functions
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows (distance from the ideal goal)
    # Lower ydist is better.
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending)
    scored.sort(key=lambda x: x[0])
    
    # Return top 5% of rows (800 rows * 0.05 = 40)
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
    
    # Print summary of the best rows
    print(f"Found {len(best_indices)} employees with optimal working arrangements.")
    print("Top 3 examples (Age, YearsAtCompany+, YearsInCurrentRole+, YearsWithCurrManager+):")
    
    # Indices for specific columns of interest
    idx_age = header.index("Age")
    idx_yac = header.index("YearsAtCompany+")
    idx_yicr = header.index("YearsInCurrentRole+")
    idx_ywcm = header.index("YearsWithCurrManager+")
    
    for i in best_indices[:3]:
        r = rows[i]
        print(f"  Age: {r[idx_age]}, Years at Company: {r[idx_yac]}, "
              f"Years in Role: {r[idx_yicr]}, Years with Manager: {r[idx_ywcm]}")

import ezr
import random

def remember(header, rows):
    """
    Finds the best rows based on the goals defined in the header.
    Goals ending in '+' are maximized, '-' are minimized.
    """
    # Create a table object to use the library's utility functions
    # We reconstruct the header with the original names to match the Tbl structure
    tbl = ezr.Tbl([header] + rows)
    
    # ydist calculates how far a row is from the ideal goal values
    # We want to minimize ydist (closer to 0 is better)
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by ydist ascending (best first)
    scored.sort(key=lambda x: x[0])
    
    # Return top 5% of rows (or at least 1)
    limit = max(1, int(len(rows) * 0.05))
    return [idx for score, idx in scored[:limit]]

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get indices of the best rows
    best_indices = remember(header, rows)
    
    # Print a summary for the customer
    print(f"Analysis of {len(rows)} employee records.")
    print(f"Identified {len(best_indices)} staff members with optimal working arrangements.")
    print("-" * 40)
    
    # Show a sample of the best rows
    # We look at columns related to working arrangements: 
    # YearsAtCompany+, YearsInCurrentRole+, YearsSinceLastPromotion, YearsWithCurrManager+
    cols_to_show = [31, 32, 33, 34]
    print(f"{'Index':<10} | {'YearsAtCo':<10} | {'YearsInRole':<12} | {'YearsSinceProm':<15}")
    for idx in best_indices[:5]:
        row = rows[idx]
        print(f"{idx:<10} | {row[31]:<10} | {row[32]:<12} | {row[33]:<15}")
    
    print("-" * 40)
    print("These employees represent the top performers based on tenure and role stability.")

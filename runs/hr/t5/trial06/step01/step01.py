import ezr
import random

def remember(header, rows):
    """
    Finds the best rows based on the goals defined in the header.
    Goals ending in '+' are maximized, '-' are minimized.
    """
    # Create a table object to use the library's utility functions
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows. ydist measures how far a row is from 
    # the ideal goal values (0 for '-', 1 for '+').
    # Lower ydist is better.
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by ydist ascending (best first)
    scored.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (or at least 1)
    limit = max(1, len(rows) // 20)
    return [idx for score, idx in scored[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the best rows
    best_indices = remember(header, rows)
    
    # Print a summary for the customer
    print(f"Analysis of {len(rows)} employee records.")
    print(f"Identified {len(best_indices)} staff members with optimal working arrangements.")
    print("-" * 40)
    
    # Show the average of the best rows compared to the whole dataset
    best_rows = [rows[i] for i in best_indices]
    
    # Print a few key attributes of the best group
    print("Characteristics of the 'stay unusually long' group (averages/modes):")
    for col_idx, name in enumerate(header):
        if name in ["Age", "MonthlyIncome", "TotalWorkingYears", "YearsAtCompany+"]:
            vals = [r[col_idx] for r in best_rows if r[col_idx] != "?"]
            if vals:
                avg = sum(vals) / len(vals)
                print(f"  {name:20}: {avg:.1f}")
    
    print("-" * 40)
    print("These employees represent the top performers based on tenure and satisfaction goals.")

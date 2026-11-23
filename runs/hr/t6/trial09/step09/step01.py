import ezr
import random

def remember(header, rows):
    """
    Finds the best rows based on the goals defined in the header.
    Goals ending in '+' are maximized, '-' are minimized.
    """
    # Create a table object to use ezr's utility functions
    # We reconstruct the header with the required format for ezr.Tbl
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows (distance from the ideal goal)
    # Lower ydist is better.
    scored = []
    for i, row in enumerate(rows):
        scored.append((ezr.ydist(tbl, row), i))
    
    # Sort by ydist ascending (best first)
    scored.sort()
    
    # Return top 5% of rows (800 rows * 0.05 = 40)
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
    
    # Print summary for the customer
    print(f"Analysis complete. Identified {len(best_indices)} employees with optimal working arrangements.")
    print("Top 3 representative rows (indices):", best_indices[:3])
    
    # Example: Show average of a key column for these top performers
    # YearsAtCompany+ is at index 31
    target_col = 31
    avg_years = sum(rows[i][target_col] for i in best_indices) / len(best_indices)
    print(f"Average 'YearsAtCompany+' for this group: {avg_years:.1f} years.")
    
    exit(0)

import ezr
import random

def remember(header, rows):
    """
    Finds the best rows based on the goal columns.
    Goals: YearsAtCompany+, YearsInCurrentRole+, YearsWithCurrManager+ (maximize)
    Others ending in - (minimize).
    """
    # Create a table object to use the library's utility functions
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows. ydist measures how far a row is from the ideal.
    # The library defines ydist as the distance from the best possible goals.
    # We want to minimize ydist to find the "best" rows.
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending)
    scored.sort()
    
    # Return the top 5% of rows (or at least 1)
    limit = max(1, len(rows) // 20)
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
    print(f"Analysis complete. Found {len(best_indices)} records of staff with long-term tenure.")
    print("Top 3 representative rows (indices):", best_indices[:3])
    
    # Display the average of the goal columns for these specific rows
    print("\nAverage metrics for these top performers:")
    goal_cols = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    for idx in goal_cols:
        vals = [rows[i][idx] for i in best_indices if isinstance(rows[i][idx], (int, float))]
        if vals:
            avg = sum(vals) / len(vals)
            print(f"  {header[idx]}: {avg:.2f}")

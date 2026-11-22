import ezr
import random

def remember(header, rows):
    """
    Finds the best rows based on goals.
    Goals: YearsAtCompany+, YearsInCurrentRole+, YearsWithCurrManager+ (maximize)
    Others ending in - are minimized.
    """
    # Create a table object to use ezr's utility functions
    tbl = ezr.Tbl([header] + rows)
    
    # ydist calculates how far a row is from the ideal goal values.
    # Lower ydist means the row is closer to the "best" (maximized/minimized goals).
    # We want rows that stay "unusually long", which correlates with high values
    # in the '+' columns.
    
    # Sort rows by ydist (ascending: best first)
    indexed_rows = list(enumerate(rows))
    indexed_rows.sort(key=lambda x: ezr.ydist(tbl, x[1]))
    
    # Return top 5% of rows (800 rows * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    return [idx for idx, row in indexed_rows[:limit]]

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get best indices
    best_indices = remember(header, rows)
    
    # Print summary for the customer
    print(f"Analysis of {len(rows)} records.")
    print(f"Identified {len(best_indices)} employees with the longest tenure/best retention metrics.")
    print("\nTop 3 representative rows (indices):")
    for i in best_indices[:3]:
        row = rows[i]
        # Extract relevant tenure columns for display
        tenure_info = {
            "YearsAtCompany": row[header.index("YearsAtCompany+")],
            "YearsInCurrentRole": row[header.index("YearsInCurrentRole+")],
            "YearsWithCurrManager": row[header.index("YearsWithCurrManager+")]
        }
        print(f"Row {i}: {tenure_info}")
    
    exit(0)

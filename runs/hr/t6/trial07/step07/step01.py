import ezr
import random

def remember(header, rows):
    """
    Finds the best rows based on the goals defined in the header.
    Goals ending in '+' are maximized, '-' are minimized.
    """
    # Create a table object to use ezr's utility functions
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (distance from ideal goals)
    # ydist calculates how far a row is from the best possible outcome
    # Lower ydist is better.
    indexed_rows = list(enumerate(rows))
    indexed_rows.sort(key=lambda x: ezr.ydist(tbl, x[1]))
    
    # Return the top 5% of rows (or at least 1)
    limit = max(1, len(rows) // 20)
    return [idx for idx, row in indexed_rows[:limit]]

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the best rows
    best_indices = remember(header, rows)
    
    print(f"Analysis complete. Found {len(best_indices)} top-performing staff records.")
    print("These individuals represent the 'best' working arrangements based on the provided goals.")
    
    # Print a summary of the first few best rows
    print("\nSample of top records (Age, YearsAtCompany+, YearsInCurrentRole+):")
    for idx in best_indices[:3]:
        row = rows[idx]
        # Find indices for specific columns
        age_idx = header.index('Age')
        yac_idx = header.index('YearsAtCompany+')
        yicr_idx = header.index('YearsInCurrentRole+')
        print(f"Row {idx}: Age={row[age_idx]}, YearsAtCompany={row[yac_idx]}, YearsInCurrentRole={row[yicr_idx]}")

import ezr
import step07

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We prioritize rows where 'Size' and 'Criticality' are high,
    then use the acquire logic to find the best within the budget.
    """
    # Filter for "large, high-criticality" projects
    size_idx = header.index("Size")
    crit_idx = header.index("Criticality")
    
    # Identify indices of rows that match the criteria
    candidates = [
        i for i, row in enumerate(rows) 
        if row[size_idx] != "?" and row[size_idx] > 0.5 and 
           row[crit_idx] != "?" and row[crit_idx] > 0.5
    ]
    
    # If no rows match, fall back to all rows
    if not candidates:
        candidates = list(range(len(rows)))
        
    # Create a subset of rows to search within
    subset_rows = [rows[i] for i in candidates]
    
    # Use the logic from step07 to find the best within the budget
    # We map the subset index back to the original index
    def oracle_wrapper(row):
        # Find original index by matching the row object
        # Since we are modifying the row in-place, we can find it in the original list
        for i, r in enumerate(rows):
            if r is row:
                full_row = label(i)
                for j in range(len(row)):
                    row[j] = full_row[j]
                return row
        return row
    
    # Initialize table with the subset of rows
    tbl = ezr.Tbl([header] + subset_rows)
    
    # Acquire returns the rows that were labeled
    labeled = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row in the labeled subset
    best_row = min(labeled, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row in the original list
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals
    masked_rows = [
        ["?" if (h.endswith("-") or h.endswith("+")) else v for h, v in zip(header, r)]
        for r in rows
    ]
    
    def label(i):
        return rows[i]
    
    best_idx = choose(header, masked_rows, label)
    
    print(f"Optimization complete for high-criticality, large-scale project.")
    print(f"Best setup found at index: {best_idx}")
    print(f"Setup values: {rows[best_idx]}")
    
    exit(0)

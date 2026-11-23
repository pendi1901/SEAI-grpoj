import ezr
import step07

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We prioritize rows where 'Size' and 'Criticality' are high,
    then use the acquire logic to find the best within the budget.
    """
    # Filter for "large, high-criticality" projects
    # Size and Criticality are numeric (uppercase).
    # We define "large" as Size > 0.5 and "high-criticality" as Criticality > 0.5
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
        # Find original index
        orig_idx = rows.index(row)
        return label(orig_idx)
    
    tbl = ezr.Tbl([header] + subset_rows)
    labeled = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row in the labeled subset
    best_row = min(labeled, key=lambda r: ezr.ydist(tbl, r))
    
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

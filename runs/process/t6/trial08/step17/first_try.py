import ezr
import step07

def choose(header, rows, label):
    """
    Find the best setup for a large, high-criticality project.
    We filter for 'large' and 'critical' projects first, then use 
    the acquisition strategy to find the best within that subset.
    """
    # 1. Filter for large, high-criticality projects
    # 'Size' and 'Criticality' are input columns (numeric)
    size_idx = header.index("Size")
    crit_idx = header.index("Criticality")
    
    # Define 'large' and 'critical' as being above the median
    all_sizes = [r[size_idx] for r in rows]
    all_crits = [r[crit_idx] for r in rows]
    med_size = sorted(all_sizes)[len(all_sizes) // 2]
    med_crit = sorted(all_crits)[len(all_crits) // 2]
    
    # Identify indices of rows that meet the criteria
    candidates = [i for i, r in enumerate(rows) 
                  if r[size_idx] >= med_size and r[crit_idx] >= med_crit]
    
    # If no rows meet criteria, fall back to all rows
    if not candidates:
        candidates = list(range(len(rows)))
        
    # 2. Use the acquisition strategy on the candidates
    # We create a mapping to handle the label budget
    labeled_cache = {}
    
    def oracle_wrapper(idx):
        if idx not in labeled_cache:
            labeled_cache[idx] = label(idx)
            # Update the row in the original list
            for i, val in enumerate(labeled_cache[idx]):
                rows[idx][i] = val
        return rows[idx]

    # Use the acquire logic from step07
    # We pass a subset of rows to the acquire function
    subset_rows = [rows[i] for i in candidates]
    tbl = ezr.Tbl([header] + subset_rows)
    
    # We need to map the acquire results back to the original indices
    best_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones
    best_row = min(best_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the original index
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    full_rows = [list(r) for r in data[1:]]
    
    # Mask goals
    masked_rows = []
    for r in full_rows:
        new_row = list(r)
        for i, name in enumerate(header):
            if name.endswith(('-', '+')):
                new_row[i] = "?"
        masked_rows.append(new_row)
    
    labeled_indices = set()
    def label_func(idx):
        labeled_indices.add(idx)
        return full_rows[idx]
    
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Best setup for a large, critical project found at index: {best_idx}")
    print(f"Total setups labeled: {len(labeled_indices)}")
    print(f"Best row values: {full_rows[best_idx]}")
    exit(0)

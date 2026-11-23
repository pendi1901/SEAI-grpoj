import ezr

def choose(header, rows, label):
    """
    Find the best setup for a large, high-criticality project.
    We filter for 'large' and 'critical' projects first, then use 
    the acquisition strategy to find the best within that subset.
    """
    # 1. Filter for large, high-criticality projects
    size_idx = header.index("Size")
    crit_idx = header.index("Criticality")
    
    all_sizes = [r[size_idx] for r in rows]
    all_crits = [r[crit_idx] for r in rows]
    med_size = sorted(all_sizes)[len(all_sizes) // 2]
    med_crit = sorted(all_crits)[len(all_crits) // 2]
    
    # Identify indices of rows that meet the criteria
    candidates = [i for i, r in enumerate(rows) 
                  if r[size_idx] >= med_size and r[crit_idx] >= med_crit]
    
    if not candidates:
        candidates = list(range(len(rows)))
        
    # 2. Use the acquisition strategy on the candidates
    # We use a dictionary to cache labels by index, not by row object
    labeled_cache = {}

    def oracle_wrapper(row):
        # Find the index of the row in the original list
        idx = -1
        for i, r in enumerate(rows):
            if r is row:
                idx = i
                break
        
        if idx not in labeled_cache:
            real_vals = label(idx)
            for i, val in enumerate(real_vals):
                row[i] = val
            labeled_cache[idx] = row
        return row

    # Create a table from the candidate rows
    subset_rows = [rows[i] for i in candidates]
    tbl = ezr.Tbl([header] + subset_rows)
    
    # Use the acquire logic from ezr
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

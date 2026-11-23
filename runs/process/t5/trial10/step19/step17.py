import ezr
import random

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We filter for rows with high 'Size' and 'Criticality' and then use 
    the acquisition strategy to find the best among them within the 50-label budget.
    """
    # 1. Filter for 'large' and 'high criticality' projects
    # Size and Criticality are numeric columns (0.0 to 1.0)
    size_idx = header.index("Size")
    crit_idx = header.index("Criticality")
    
    # We define 'large and damaging' as being in the top 25% for both
    candidates = []
    for i, row in enumerate(rows):
        if row[size_idx] > 0.75 and row[crit_idx] > 0.75:
            candidates.append((i, row))
            
    # If we don't have enough candidates, fall back to the whole set
    if len(candidates) < 10:
        search_space = list(enumerate(rows))
    else:
        search_space = candidates

    # 2. Prepare for acquisition
    # We must ensure the table only contains rows that have been labeled
    # or are ready to be labeled. Since ezr.acquire expects a TBL with 
    # rows that have goals, we must be careful.
    indices = [x[0] for x in search_space]
    subset_rows = [x[1] for x in search_space]
    
    # We use a simple wrapper to handle the labeling budget
    labeled_cache = {}
    def oracle_wrapper(row):
        # Find the original index to call the provided label function
        for i, r in enumerate(subset_rows):
            if r is row:
                idx = indices[i]
                if idx not in labeled_cache:
                    labeled_cache[idx] = label(idx)
                    # Update the row in place so the TBL reflects the new data
                    for j in range(len(labeled_cache[idx])):
                        row[j] = labeled_cache[idx][j]
                return row
        return row

    # Create a table for the subset. 
    # Note: We must ensure the TBL is initialized with rows that have goals
    # or it will fail during normalization. We label a small initial set.
    initial_count = min(len(subset_rows), 4)
    for i in range(initial_count):
        oracle_wrapper(subset_rows[i])
        
    tbl = ezr.Tbl([header] + subset_rows)
    
    # Acquire labels
    labeled = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # 3. Find the best row among the labeled ones
    # We use ydist to determine the best.
    best_row = min(labeled, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the original index
    for i, r in enumerate(subset_rows):
        if r is best_row:
            return indices[i]
            
    return indices[0]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask goals
    masked_rows = []
    for r in rows:
        new_row = list(r)
        for i, name in enumerate(header):
            if name[-1] in "+-":
                new_row[i] = "?"
        masked_rows.append(new_row)
        
    def label_func(i):
        return rows[i]
    
    random.seed(1234567891)
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Analysis: Found the best configuration for a large, high-criticality project.")
    print(f"Best setup found at index: {best_idx}")
    print(f"Row data: {rows[best_idx]}")

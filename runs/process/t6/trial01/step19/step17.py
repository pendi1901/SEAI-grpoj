import ezr

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We filter for rows where 'Size' and 'Criticality' are high,
    then use the acquire strategy to find the best within the budget.
    """
    # Identify indices for Size (index 6) and Criticality (index 1)
    size_idx = 6
    crit_idx = 1
    
    # Calculate medians to define "large" and "high criticality"
    all_sizes = [r[size_idx] for r in rows if isinstance(r[size_idx], (int, float))]
    all_crits = [r[crit_idx] for r in rows if isinstance(r[crit_idx], (int, float))]
    med_size = sorted(all_sizes)[len(all_sizes)//2]
    med_crit = sorted(all_crits)[len(all_crits)//2]
    
    # Filter rows that match the "large and high criticality" criteria
    candidates = [i for i, r in enumerate(rows) 
                  if r[size_idx] >= med_size and r[crit_idx] >= med_crit]
    
    # If no rows match, fall back to all rows
    if not candidates:
        candidates = list(range(len(rows)))
        
    # The oracle wrapper must return the full row (including goals)
    def oracle_wrapper(row):
        # Find the index of the row by matching the input row object
        for i in candidates:
            if rows[i] is row:
                revealed = label(i)
                rows[i] = revealed
                return revealed
        return row

    # Create a table from the original rows (with hidden goals)
    # We must pass the full header and rows to Tbl so it knows about the goal columns
    tbl = ezr.Tbl([header] + rows)
    
    # Use acquire to find the best within the 50-label budget
    # We restrict the acquire process to our candidates
    subset_rows = [rows[i] for i in candidates]
    labeled = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the candidates based on the final model
    best_row = min(subset_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the original index
    for i in candidates:
        if rows[i] is best_row:
            return i
    return candidates[0]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Mask goals
    test_rows = []
    for row in all_rows:
        new_row = row[:]
        new_row[9] = new_row[10] = new_row[11] = "?"
        test_rows.append(new_row)
        
    def label_func(i):
        return all_rows[i]
        
    best_idx = choose(header, test_rows, label_func)
    
    print(f"Best configuration for large, high-criticality project found at index: {best_idx}")
    print(f"Goal values: {all_rows[best_idx][9:]}")
    
    exit(0)

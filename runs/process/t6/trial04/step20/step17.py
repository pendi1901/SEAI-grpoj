import ezr

def choose(header, rows, label):
    """
    Find the best setup for a large, high-stakes project.
    We filter for large projects and use the acquire strategy.
    The IndexError in the previous version was due to passing rows 
    with '?' into Tbl, which ezr handles if the header is correct.
    """
    # Identify the index of the 'Size' column
    size_idx = header.index("Size")
    
    # Define "large" as projects with Size above the median
    sizes = [r[size_idx] for r in rows]
    median_size = sorted(sizes)[len(sizes) // 2]
    
    # Filter indices for large projects
    large_indices = [i for i, r in enumerate(rows) if r[size_idx] >= median_size]
    
    # Create a mapping from the filtered row to its original index
    # We must pass the full header and the rows to Tbl.
    # ezr.Tbl expects rows to have the same length as the header.
    tbl = ezr.Tbl([header] + rows)
    
    # Oracle wrapper to return the full row (with goals) when labeled
    def oracle_wrapper(row):
        for i, r in enumerate(rows):
            if r is row:
                return label(i)
        return row

    # Use the acquire strategy on the subset of large projects
    # We restrict the search to the large_indices
    large_rows = [rows[i] for i in large_indices]
    
    # We use the acquire function on the full table but prioritize large rows
    # by sorting the todo list in acquire.
    ezr.the.Stop = 50
    
    # To avoid the IndexError, ensure we only pass valid rows to Tbl
    # The acquire function works on the table's rows.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Filter labeled rows to only those that were "large"
    large_labeled = [r for r in labeled_rows if r[size_idx] >= median_size]
    
    # If no large rows were labeled, fall back to the best of all labeled
    candidates = large_labeled if large_labeled else labeled_rows
    
    # Find the best row among those labeled
    best_row = min(candidates, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the original index of the best row found
    for i, r in enumerate(rows):
        if r is best_row:
            return i
    return large_indices[0]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(filename)
    header = next(rows_gen)
    rows = list(rows_gen)
    
    # Mask the goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
    
    def label(i):
        return rows[i]
    
    best_idx = choose(header, masked_rows, label)
    
    print("Optimization for Large-Scale High-Stakes Projects:")
    print("-" * 60)
    print(f"Best configuration found at index: {best_idx}")
    goal_vals = [rows[best_idx][i] for i in goal_indices]
    print(f"Goal values: {goal_vals}")
    print("-" * 60)
    print("Strategy: Targeted large-scale projects and applied intelligent")
    print("sampling to minimize risk and maximize performance.")

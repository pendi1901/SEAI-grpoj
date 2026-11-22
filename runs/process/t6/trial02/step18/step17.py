import ezr

def choose(header, rows, label):
    """
    Find the best setup for a large, high-criticality project.
    We use ezr's acquire function to intelligently sample the space
    within the 50-label budget.
    """
    # 1. Setup: Create a table for distance calculations.
    # We use a copy of rows to avoid mutating the original input.
    tbl = ezr.Tbl([header] + [list(r) for r in rows])
    
    # 2. Oracle: Map the acquire function's row-based label calls 
    # back to the index-based label function provided by the harness.
    # We cache results to ensure we don't exceed the 50-label budget.
    labeled_cache = {}

    def smart_label(row):
        # Find the index of the row in the original list
        # We search for the row by identity or content
        idx = -1
        for i, r in enumerate(rows):
            if r is row:
                idx = i
                break
        
        if idx not in labeled_cache:
            full_row = label(idx)
            labeled_cache[idx] = full_row
            # Update the row in place to reflect the new values
            for i in range(len(row)):
                row[i] = full_row[i]
        return row

    # 3. Acquire: Use ezr's built-in acquisition logic.
    # We set the budget to 50 as per the rules.
    ezr.the.Stop = 50
    labeled_rows = ezr.acquire(tbl, cap=50, label=smart_label)
    
    # 4. Find the best row among the labeled ones.
    # ydist calculates distance to the ideal goal values.
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found.
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Mask goals for the harness simulation
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_func(idx):
        return all_rows[idx]
        
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Optimization complete.")
    print(f"Best row found at index: {best_idx}")
    print(f"Goal values for best row: {[all_rows[best_idx][i] for i in goal_indices]}")
    
    exit(0)

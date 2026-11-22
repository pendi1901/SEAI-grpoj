import ezr
import random

def choose(header, rows, label):
    """
    Find the best setup for a large, high-criticality project.
    We filter for rows that match 'large' and 'critical' criteria,
    then use the acquire logic to find the best among them within the budget.
    """
    # Identify indices for 'Size' and 'Criticality'
    # Based on header: Size is index 6, Criticality is index 1
    size_idx = 6
    crit_idx = 1
    
    # Filter rows that are 'large' (Size > 0.7) and 'critical' (Criticality > 0.7)
    # This focuses our search on the high-stakes, large-project space.
    candidates = [i for i, r in enumerate(rows) if r[size_idx] > 0.7 and r[crit_idx] > 0.7]
    
    # If we don't have enough candidates, fall back to all rows
    if len(candidates) < 10:
        candidates = list(range(len(rows)))
        
    # We use a subset of the data to build the TBL for acquire
    # We must ensure we don't exceed 50 labels total.
    budget = 50
    labeled = {}

    def oracle_wrapper(row):
        # Find original index
        idx = rows.index(row)
        if idx not in labeled:
            if len(labeled) >= budget:
                return row # Return masked if budget exhausted
            labeled[idx] = label(idx)
            # Update row in place
            for i in range(len(row)):
                row[i] = labeled[idx][i]
        return row

    # Create a TBL from the candidates
    candidate_rows = [rows[i] for i in candidates]
    tbl = ezr.Tbl([header] + candidate_rows)
    
    # Use acquire to find the best within the budget
    # acquire() returns the rows it labeled
    labeled_rows = ezr.acquire(tbl, cap=budget, label=oracle_wrapper)
    
    # Find the best row among those labeled
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    return rows.index(best_row)

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Mask the goals
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define label function
    def label(i):
        return all_rows[i]
    
    random.seed(1234567891)
    best_idx = choose(header, masked_rows, label)
    
    print(f"--- High-Stakes Project Optimization ---")
    print(f"Best setup found at index: {best_idx}")
    print(f"Row data: {all_rows[best_idx]}")
    print("\nStrategy: Filtered for large, high-criticality projects and used")
    print("intelligent acquisition to find the optimal configuration within")
    print("a 50-label budget.")

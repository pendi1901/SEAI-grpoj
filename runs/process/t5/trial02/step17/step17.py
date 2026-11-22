import ezr
import random

def choose(header, rows, label):
    """
    Find the best setup for a large, high-criticality project.
    We focus on the high-stakes subspace and use intelligent acquisition.
    """
    # Identify indices for 'Size' and 'Criticality'
    # Based on header: Size is index 6, Criticality is index 1
    size_idx = 6
    crit_idx = 1
    
    # Filter rows that are 'large' (Size > 0.7) and 'critical' (Criticality > 0.7)
    # We store the original index to return it later.
    candidates = []
    for i, r in enumerate(rows):
        if r[size_idx] != "?" and r[size_idx] > 0.7 and r[crit_idx] > 0.7:
            candidates.append((i, r))
    
    # If we don't have enough candidates, fall back to all rows
    if len(candidates) < 10:
        candidates = [(i, r) for i, r in enumerate(rows)]
        
    # We track labeled rows to ensure we don't exceed the budget
    budget = 50
    labeled_data = {}

    def oracle_wrapper(row):
        # Find the original index by matching the row object
        # Since acquire() might pass a row that is a copy, we use the 
        # index stored in our candidate list.
        for idx, r in candidates:
            if r is row:
                if idx not in labeled_data:
                    if len(labeled_data) >= budget:
                        return row
                    labeled_data[idx] = label(idx)
                # Return the fully labeled row
                return labeled_data[idx]
        return row

    # Create a TBL from the candidates
    candidate_rows = [r for i, r in candidates]
    tbl = ezr.Tbl([header] + candidate_rows)
    
    # Use acquire to find the best within the budget
    # acquire() returns the rows it labeled
    labeled_rows = ezr.acquire(tbl, cap=budget, label=oracle_wrapper)
    
    # Find the best row among those labeled
    # We compare based on ydist
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the original index of the best row
    for idx, r in candidates:
        if r is best_row:
            return idx
    return candidates[0][0]

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

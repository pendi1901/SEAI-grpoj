import ezr
import random

def choose(header, rows, label):
    """
    Find the best setup for a 'large' project.
    'Large' is defined by the 'Size' column. We filter for large projects
    (Size > 0.7) and use the acquire strategy to find the best among them
    within the 50-label budget.
    """
    # Identify the index for 'Size'
    size_idx = header.index("Size")
    
    # Filter for large projects
    large_indices = [i for i, r in enumerate(rows) if r[size_idx] > 0.7]
    
    # If no large projects found, fall back to all rows
    candidates = large_indices if large_indices else range(len(rows))
    
    # Map indices to rows for the acquire strategy
    row_to_idx = {id(rows[i]): i for i in candidates}
    
    # Create a table for the subset
    subset_rows = [rows[i] for i in candidates]
    tbl = ezr.Tbl([header] + subset_rows)
    
    # Oracle wrapper to track labels and update rows
    labeled_count = 0
    
    def oracle_wrapper(row):
        nonlocal labeled_count
        idx = row_to_idx[id(row)]
        true_row = label(idx)
        # Update row in place
        for i in range(len(true_row)):
            row[i] = true_row[i]
        labeled_count += 1
        return row

    # Use acquire to find the best within the budget
    # We limit the budget to 50
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among those labeled
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    return row_to_idx[id(best_row)]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Keep original for oracle
    original_rows = [list(r) for r in rows]
    
    # Mask goals
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
    
    labeled_indices = set()
    def label(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= 50:
                raise Exception("Budget exceeded!")
            labeled_indices.add(i)
        return original_rows[i]
    
    random.seed(1234567891)
    best_idx = choose(header, masked_rows, label)
    
    print(f"Strategy complete. Labeled {len(labeled_indices)} setups.")
    print(f"The best setup for a large project is at index {best_idx}.")
    print(f"Goal values: {[original_rows[best_idx][i] for i in goal_indices]}")

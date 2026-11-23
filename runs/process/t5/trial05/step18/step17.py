import ezr
import random

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We prioritize rows with high 'Size' and 'Criticality' values.
    We use a subset of rows to build a valid table context before 
    running the acquisition to avoid normalization errors on '?' cells.
    """
    # 1. Identify high-risk candidates (Large and High Criticality)
    size_idx = header.index('Size')
    crit_idx = header.index('Criticality')
    
    # Sort by size and criticality descending
    scored = sorted(range(len(rows)), 
                    key=lambda i: rows[i][size_idx] + rows[i][crit_idx], 
                    reverse=True)
    
    # 2. Setup for labeling
    # We need a table with at least some numeric data to avoid 
    # division by zero or type errors during normalization.
    # We label a few high-risk rows first to seed the table.
    labeled_indices = {}

    def oracle_wrapper(i):
        if i not in labeled_indices:
            true_vals = label(i)
            row = list(rows[i])
            for j, val in enumerate(true_vals):
                row[j] = val
            labeled_indices[i] = row
        return labeled_indices[i]

    # Seed with 5 high-risk rows to establish column statistics
    for i in scored[:5]:
        oracle_wrapper(i)
    
    # Create the table using the labeled rows
    tbl = ezr.Tbl([header] + list(labeled_indices.values()))
    
    # 3. Run the acquisition
    # We use the remaining budget (50 - 5 = 45)
    # We pass a wrapper that ensures we only label rows we haven't seen
    def acquire_label(row):
        # Find index of row
        for i, r in enumerate(rows):
            if r is row:
                return oracle_wrapper(i)
        return row

    ezr.acquire(tbl, cap=50, label=acquire_label)
    
    # 4. Return the best row found among those labeled
    best_idx = -1
    best_ydist = float('inf')
    
    for idx, row in labeled_indices.items():
        current_ydist = ezr.ydist(tbl, row)
        if current_ydist < best_ydist:
            best_ydist = current_ydist
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    header = next(rows_gen)
    all_rows = list(rows_gen)
    
    # Mask goals
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    masked_rows = []
    for r in all_rows:
        new_row = list(r)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_func(i):
        return all_rows[i]
    
    random.seed(1234567891)
    best_index = choose(header, masked_rows, label_func)
    
    print("Optimization Analysis for Large, High-Criticality Projects:")
    print(f"Best setup found at index: {best_index}")
    print(f"Row details: {all_rows[best_index]}")

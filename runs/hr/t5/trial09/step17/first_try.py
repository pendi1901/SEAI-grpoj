import ezr
import random

def choose(header, rows, label):
    """
    Finds the best laboratory staff arrangement using a budget of 50 labels.
    """
    # Filter for Laboratory Technician role
    idx_role = header.index("jobRole")
    lab_indices = [i for i, r in enumerate(rows) if r[idx_role] == "Laboratory Technician"]
    
    # We only care about lab staff
    lab_rows = [rows[i] for i in lab_indices]
    
    # Keep track of labeled rows to stay within budget
    labeled_indices = {}
    
    def oracle(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= 50:
                raise Exception("Budget exceeded")
            labeled_indices[i] = label(lab_indices[i])
        return labeled_indices[i]

    # Initialize table with the lab rows (goals are '?')
    # We need a valid table structure to use ydist
    tbl = ezr.Tbl([header] + lab_rows)
    
    # Use the acquire strategy to find the best row
    # We pass a wrapper that maps our local index to the global index
    def label_wrapper(row):
        # Find global index by matching row content (assuming unique enough)
        # Or simply use the oracle function defined above
        # Since acquire expects a row, we find the index of this row in our subset
        idx_in_subset = next(i for i, r in enumerate(lab_rows) if r == row)
        true_vals = oracle(idx_in_subset)
        for j, val in enumerate(true_vals):
            row[j] = val
        return row

    # Acquire labels
    best_rows = ezr.acquire(tbl, cap=50, label=label_wrapper)
    
    # Find the best row among those we labeled
    best_row = min(best_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the global index of the best row
    return next(i for i, r in enumerate(rows) if r == best_row)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask goal columns
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define label function
    def label_func(i):
        return rows[i]
    
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Analysis: Best laboratory staff arrangement found at index {best_idx}.")
    print("This selection was made by prioritizing retention metrics within the laboratory staff subset.")
    print("Goal metrics for this employee:")
    for idx in goal_indices:
        print(f"  {header[idx]}: {rows[best_idx][idx]}")

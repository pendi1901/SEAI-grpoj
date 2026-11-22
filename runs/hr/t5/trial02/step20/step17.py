import ezr
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement for laboratory staff using at most 50 labels.
    """
    # Identify the jobRole column index
    job_role_idx = header.index('jobRole')
    
    # Filter rows for 'Laboratory Technician'
    # We keep track of the original indices to return the correct one
    lab_data = [(i, r) for i, r in enumerate(rows) if r[job_role_idx] == 'Laboratory Technician']
    if not lab_data:
        return 0
    
    lab_indices, lab_rows = zip(*lab_data)
    lab_rows = [list(r) for r in lab_rows]
    
    # Create a table for the lab staff
    tbl = ezr.Tbl([header] + lab_rows)
    
    # Oracle wrapper to track labels and update the table
    # We must ensure the row passed to acquire is updated with numeric values
    # before ydist/norm is called on it.
    labeled_count = 0
    
    def oracle_wrapper(row):
        nonlocal labeled_count
        if labeled_count >= 50:
            raise Exception("Label budget exceeded!")
        
        # Find which original index this row corresponds to
        # We look for the row in our lab_rows list
        idx_in_lab = lab_rows.index(row)
        original_idx = lab_indices[idx_in_lab]
        
        # Get true values
        true_row = label(original_idx)
        
        # Update row in place with true values
        for col_idx, val in enumerate(true_row):
            row[col_idx] = val
            
        labeled_count += 1
        return row

    # Use active learning to find the best arrangement
    # We limit the budget to 50
    ezr.the.Stop = 50
    
    # acquire() will call our oracle_wrapper, which updates the row
    # and the table stats (mu, sd) so that norm() works correctly.
    labeled = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones using ydist
    # We use the table's ydist function which now has updated stats
    best_row = min(labeled, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the original index of the best row
    idx_in_lab = lab_rows.index(best_row)
    return lab_indices[idx_in_lab]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Keep a copy of the original rows to simulate the oracle
    full_data = [list(r) for r in rows]
    
    # Mask the goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    masked_rows = []
    for r in rows:
        new_row = list(r)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
            
    def label(i):
        return full_data[i]
    
    best_idx = choose(header, masked_rows, label)
    
    print(f"Active learning complete for laboratory staff.")
    print(f"Best arrangement found at row index: {best_idx}")
    print("This arrangement was identified by focusing on laboratory technicians")
    print("and using a multi-objective active learning strategy.")
    
    exit(0)

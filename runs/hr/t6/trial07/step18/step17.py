import ezr
import step07

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff
    only, using the acquisition strategy within a budget of 50 labels.
    """
    # Filter rows to only include Laboratory Technicians
    job_role_idx = header.index('jobRole')
    lab_rows = [r for r in rows if r[job_role_idx] == 'Laboratory Technician']
    
    # Map these filtered rows back to their original indices in the full dataset
    # We use the row content to identify them since they are unique enough
    # or we can rely on the fact that the harness expects the index of the row
    # in the original 'rows' list provided to the function.
    original_indices = [i for i, r in enumerate(rows) if r[job_role_idx] == 'Laboratory Technician']
    
    # Create a mapping for the oracle
    row_to_orig_idx = {id(lab_rows[i]): original_indices[i] for i in range(len(lab_rows))}
    
    # Define a local oracle that translates the lab_rows index to the original index
    def local_label(row):
        orig_idx = row_to_orig_idx[id(row)]
        true_goals = label(orig_idx)
        goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
        for i, val in zip(goal_indices, true_goals):
            row[i] = val
        return row

    # Use the logic from step07 to find the best row among the filtered set
    tbl = ezr.Tbl([header] + lab_rows)
    labeled_rows = ezr.acquire(tbl, cap=50, label=local_label)
    
    # Find the best row among the ones we labeled
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    return row_to_orig_idx[id(best_row)]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Mask goals
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i):
        return [all_rows[i][idx] for idx in goal_indices]
    
    best_idx = choose(header, masked_rows, label)
    
    print(f"Analysis complete for Laboratory Technician staff.")
    print(f"The best working arrangement found is at row index {best_idx}.")
    print(f"Details: {all_rows[best_idx]}")

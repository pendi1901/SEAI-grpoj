import ezr
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement for laboratory staff using active learning.
    We filter for 'Laboratory Technician' in the 'jobRole' column, then use
    ezr.acquire to find the best row within a budget of 50 labels.
    """
    # Identify indices
    job_role_idx = header.index('jobRole')
    
    # Filter rows for laboratory staff
    lab_staff_indices = [i for i, r in enumerate(rows) if r[job_role_idx] == 'Laboratory Technician']
    lab_staff_rows = [rows[i] for i in lab_staff_indices]
    
    # Create a table for the lab staff subset
    tbl = ezr.Tbl([header] + lab_staff_rows)
    
    # Map row objects back to their original indices in the main 'rows' list
    # to satisfy the harness's expectation of returning an index.
    row_to_idx = {id(r): lab_staff_indices[i] for i, r in enumerate(lab_staff_rows)}

    def oracle_wrapper(row):
        # Retrieve the true row from the harness using the index
        idx = row_to_idx[id(row)]
        true_row = label(idx)
        # Update the row in-place with the true goal values
        for i, name in enumerate(header):
            if name.endswith('+') or name.endswith('-'):
                row[i] = true_row[i]
        return row

    # Use ezr.acquire to perform the active learning on the lab staff subset
    # It returns the rows that were labeled
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones
    # Best is defined by the lowest ydist (closest to ideal goals)
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    return row_to_idx[id(best_row)]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # The harness provides a label function that reveals the hidden goals
    # We simulate this for the standalone run
    def mock_label(i):
        return rows[i]

    # Run the selection process
    best_idx = choose(header, rows, mock_label)
    
    print(f"Analysis complete for laboratory staff.")
    print(f"The best working arrangement was found at row index: {best_idx}")
    print(f"This row was identified as having the most optimal goal metrics after targeted interviews.")

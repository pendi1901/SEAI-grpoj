import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement for laboratory staff using at most 50 labels.
    We filter for 'Laboratory Technician' in the 'jobRole' column, then use
    the 'acquire' strategy to find the best row.
    """
    # Identify the jobRole column index
    job_role_idx = header.index('jobRole')
    
    # Filter rows for Laboratory Technicians
    # We keep the original index to return it later
    indexed_rows = [(i, r) for i, r in enumerate(rows) if r[job_role_idx] == 'Laboratory Technician']
    lab_rows = [r for _, r in indexed_rows]
    
    # Map these filtered rows to their original indices
    row_to_idx = {id(r): i for i, r in indexed_rows}
    
    # Create a table for the lab staff
    tbl = ezr.Tbl([header] + lab_rows)
    
    # Define the oracle to reveal goals for the specific row
    def oracle_wrapper(row):
        idx = row_to_idx[id(row)]
        labeled_data = label(idx)
        # Update the row in place with the revealed goals
        for i, val in enumerate(labeled_data):
            row[i] = val
        # Update the table's column statistics with the new information
        # Only update columns that are goals
        for at, col in tbl.cols.items():
            if header[at].endswith('+') or header[at].endswith('-'):
                ezr.add(col, labeled_data[at], 1)
        return row

    # Run the acquisition process on the lab staff subset
    # We use the 'acquire' strategy to intelligently pick rows to label
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the ones we labeled
    # A row is better if its ydist is lower (closer to goals)
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the original index of the best row found
    return row_to_idx[id(best_row)]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Keep a copy of the original rows to provide the 'true' values when labeled
    original_rows = [list(r) for r in rows]
    
    # Create masked rows for the choose function
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    masked_rows = []
    for r in rows:
        new_row = list(r)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    labeled_count = 0
    def label_func(i):
        global labeled_count
        labeled_count += 1
        if labeled_count > 50:
            raise Exception("Budget exceeded!")
        return original_rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Analysis complete for Laboratory Staff.")
    print(f"Used {labeled_count} labels to find the optimal arrangement.")
    print(f"The best row index found is: {best_idx}")
    print("This row represents the working arrangement that maximizes retention/performance for lab technicians.")
    
    exit(0)

import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement using at most 50 labels.
    We use the 'acquire' strategy from ezr to intelligently select
    rows that help us find the global optimum.
    """
    # Create a table structure to manage the data.
    # We must ensure the table knows about the goals before we call ydist.
    # Since rows are passed with '?' in goal columns, we initialize the table
    # with the rows, but we will update them as we label.
    tbl = ezr.Tbl([header] + rows)
    
    # Map rows to their original indices
    row_to_idx = {id(r): i for i, r in enumerate(rows)}
    
    def oracle_wrapper(row):
        idx = row_to_idx[id(row)]
        labeled_data = label(idx)
        # Update the row in place with the revealed goals
        for i, val in enumerate(labeled_data):
            row[i] = val
        # Update the table's column statistics with the new information
        # We remove the old row's contribution and add the new one
        # Note: ezr.addCols with inc=-1 removes, inc=1 adds.
        # However, since we are filling '?', we just add the new values.
        # We must update the column stats for the goals.
        for at, col in tbl.cols.items():
            if header[at].endswith('+') or header[at].endswith('-'):
                ezr.add(col, labeled_data[at], 1)
        return row

    # Run the acquisition process
    # ezr.acquire returns the rows that were labeled
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the ones we labeled
    # A row is better if its ydist is lower (closer to goals)
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
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
    
    print(f"Analysis complete.")
    print(f"Used {labeled_count} labels to find the optimal arrangement.")
    print(f"The best row index found is: {best_idx}")
    print("This row represents the working arrangement that maximizes retention/performance.")
    
    exit(0)

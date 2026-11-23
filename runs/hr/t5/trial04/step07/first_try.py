import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement by using a budget of 50 labels.
    We use the 'acquire' strategy from ezr to intelligently sample the
    rows that are most likely to be optimal based on the goal columns.
    """
    # Create a table structure to handle the data
    # We need to pass the header and rows to Tbl
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function in ezr is designed to spend a label budget
    # to find the best rows. It uses a combination of random sampling
    # and iterative refinement based on distance to goals.
    # We set the budget to 50 as requested.
    
    # We need to wrap the label function to handle the row indices
    # expected by the harness.
    def oracle_wrapper(row):
        # Find the index of this row in the original list to call label(i)
        # Note: This assumes rows are unique enough or we can identify them.
        # Since we are passed the rows, we find the index in the provided list.
        idx = rows.index(row)
        true_goals = label(idx)
        # Update the row with the true goal values
        for i, name in enumerate(header):
            if name.endswith('+') or name.endswith('-'):
                row[i] = true_goals[i]
        return row

    # Use ezr.acquire to perform the active learning
    # It returns the rows that were labeled
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones
    # Best is defined by the lowest ydist (closest to ideal goals)
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # The harness provides a label function that reveals the hidden goals
    def mock_label(i):
        return rows[i]

    # Run the selection process
    best_idx = choose(header, rows, mock_label)
    
    print(f"Analysis complete.")
    print(f"The best working arrangement was found at row index: {best_idx}")
    print(f"This row was identified as having the most optimal goal metrics after 50 targeted interviews.")

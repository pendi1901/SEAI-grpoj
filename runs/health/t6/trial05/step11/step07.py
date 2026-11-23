import ezr

def choose(header, rows, label):
    """
    Find the best row by using a budget of 50 labels.
    We use the acquire logic from ezr to intelligently sample the space.
    """
    # We need to work with a TBL that has the full data structure.
    # Since we don't have the goals yet, we create a TBL with the header.
    # We will populate it as we label.
    
    # Create a TBL with the header and all rows (goals are '?')
    # This allows ezr to understand the columns.
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function expects rows to have goals.
    # We define a wrapper that calls the provided label() function
    # and updates the row in place.
    def oracle_wrapper(row):
        # Find the index of this row in the original list
        # We use id() to ensure we match the exact object
        for i, r in enumerate(rows):
            if r is row:
                goals = label(i)
                row[0], row[1], row[2] = goals[0], goals[1], goals[2]
                # Update the TBL's column statistics with the new goals
                ezr.addCols(tbl, row)
                return row
        return row

    # We need to ensure the TBL has the correct column roles
    # The TBL was initialized with '?' in goals, so we need to re-add
    # the rows once they are labeled.
    # We reset the rows in the TBL to be empty so we can add them via acquire.
    tbl.rows = []
    
    # Configure the acquisition budget
    ezr.the.Stop = 50
    ezr.the.Start = 4
    
    # acquire() will call our oracle_wrapper, which updates the TBL
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    for i, r in enumerate(rows):
        if r is best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Keep a copy of the original goals to simulate the oracle
    original_goals = [[r[0], r[1], r[2]] for r in rows]
    
    # Mask the goals in the rows passed to choose()
    for row in rows:
        row[0] = row[1] = row[2] = "?"
        
    def mock_label(i):
        return original_goals[i]
    
    best_idx = choose(header, rows, mock_label)
    print(f"Best setup found at index: {best_idx}")

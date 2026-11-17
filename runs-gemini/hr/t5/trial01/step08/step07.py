import ezr
import random

def choose(header, rows, label):
    """
    Find the best row by acquiring labels for a subset of rows
    using the ezr.acquire logic, then returning the index of the best one.
    """
    # Create a table structure to handle the data
    # We need to ensure the table knows about the goals
    tbl = ezr.Tbl([header] + rows)
    
    # Use ezr.acquire to select and label up to 50 rows.
    # acquire returns the rows that were labeled.
    # We pass a wrapper to label that maps the index back to the original row.
    def oracle_wrapper(row):
        # Find the index of this row in the original list
        # Note: rows are unique enough in this dataset for index lookup
        idx = rows.index(row)
        labeled_row = label(idx)
        # Update the row in place with the true values
        for i, val in enumerate(labeled_row):
            row[i] = val
        return row

    # The acquire function uses the budget (the.Stop) to label rows
    # and returns the rows that were labeled.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the ones we labeled
    # A row is better when its ydist is lower
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Store original goals to simulate the oracle
    original_rows = [list(r) for r in rows]
    
    # Mask goals in the rows passed to choose()
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i):
        return original_rows[i]
        
    best_idx = choose(header, masked_rows, label)
    
    print("Analysis: Identifying the optimal working arrangement.")
    print(f"After 50 interviews, the best employee record identified is at index {best_idx}.")
    print("This record represents the arrangement that most closely aligns with organizational goals.")

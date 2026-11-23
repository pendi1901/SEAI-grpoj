import ezr
import random

def choose(header, rows, label):
    """
    Find the best row among the provided rows by using a budget of 50 labels.
    We use the 'acquire' strategy from ezr to intelligently select rows to label.
    """
    # Create a table object.
    # Note: rows currently have '?' for goals.
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # The oracle function to pass to ezr.acquire.
    # The harness label(i) returns the full row (including goals).
    # We need to map the row object back to its index to call the harness.
    # We store the original index in the row object temporarily if needed,
    # but here we can use a lookup dictionary.
    row_to_idx = {id(r): i for i, r in enumerate(rows)}

    def oracle_wrapper(row):
        idx = row_to_idx[id(row)]
        real_row = label(idx)
        # Update the row in place so the TBL reflects the new data
        for i in range(len(real_row)):
            row[i] = real_row[i]
        return row

    # Use ezr.acquire to intelligently pick 50 rows to label.
    # ezr.acquire returns the rows that were labeled.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # After labeling, find the best row among all rows that were labeled.
    # We use ydist to determine the best.
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row.
    return row_to_idx[id(best_row)]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals for the choose function
    masked_rows = []
    for r in rows:
        new_row = list(r)
        for i, name in enumerate(header):
            if name[-1] in "+-":
                new_row[i] = "?"
        masked_rows.append(new_row)
    
    # Define the label function for the harness
    def label_func(i):
        return rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Best setup found at index: {best_idx}")
    print(f"Row data: {rows[best_idx]}")

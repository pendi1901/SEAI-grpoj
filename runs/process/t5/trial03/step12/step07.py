import ezr
import random

def choose(header, rows, label):
    """
    Find the best row by using the acquire strategy from ezr.
    We have a budget of 50 labels.
    """
    # Create a table object to manage the data.
    # We use the provided rows (which have '?' in goal columns).
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function expects an oracle that returns a full row.
    # The harness label(i) returns the full row for rows[i].
    # We need to map the row object back to its index to call the label function.
    # Since rows are passed by reference, we can use a dictionary for O(1) lookup.
    row_to_idx = {id(r): i for i, r in enumerate(rows)}

    def oracle_wrapper(row):
        idx = row_to_idx[id(row)]
        true_row = label(idx)
        # Update the row in place with the true values
        for i in range(len(true_row)):
            row[i] = true_row[i]
        return row

    # Use the acquire strategy to explore and label.
    # This returns the set of rows that were labeled.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among those labeled.
    # We use ydist to evaluate quality.
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row.
    return row_to_idx[id(best_row)]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Keep a copy of the original rows to simulate the oracle
    original_rows = [list(r) for r in rows]
    
    # Mask the goals in the rows provided to the choose function
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
    
    # Define the label function for the harness
    labeled_indices = set()
    
    def label(i):
        if i not in labeled_indices:
            labeled_indices.add(i)
        if len(labeled_indices) > 50:
            raise Exception("Budget exceeded!")
        return original_rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label)
    
    print(f"Strategy complete. Labeled {len(labeled_indices)} setups.")
    print(f"The best setup found is at index {best_idx}.")
    print(f"Goal values for this setup: {[original_rows[best_idx][i] for i in goal_indices]}")

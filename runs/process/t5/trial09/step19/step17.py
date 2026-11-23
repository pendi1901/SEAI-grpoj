import ezr
import random

def choose(header, rows, label):
    """
    Find the best setup for a large, high-stakes project.
    We use the acquire() function which is designed to find the best rows
    with a limited labeling budget.
    """
    # Create a table object. Rows currently have '?' for goals.
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # The acquire function expects the oracle to return a row with 
    # the goal values filled in.
    def oracle_wrapper(row):
        # Find the index of the row in the original list
        idx = rows.index(row)
        labeled_vals = label(idx)
        # Update the row in place with the true goal values
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        for i, val in zip(goal_indices, labeled_vals):
            row[i] = val
        # Update the table's internal column statistics now that we have data
        ezr.addCols(tbl, row)
        return row

    # Use ezr.acquire to perform the search. 
    # It will call label() at most 50 times.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # After labeling, find the best row among those labeled.
    # We use ydist which relies on the now-populated goal columns.
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    rows = list(data_gen)
    
    # Keep a copy of the original rows to act as the oracle
    original_rows = [list(r) for r in rows]
    
    # Mask the goals in the rows provided to the choose function
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for r in rows:
        new_row = list(r)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    labels_called = 0
    def label_oracle(i):
        global labels_called
        labels_called += 1
        if labels_called > 50:
            raise Exception("Budget exceeded!")
        return [original_rows[i][idx] for idx in goal_indices]
    
    best_idx = choose(header, masked_rows, label_oracle)
    
    print("High-Stakes Project Optimization Complete.")
    print("-" * 50)
    print(f"Best setup found at index: {best_idx}")
    print(f"Total labels used: {labels_called}")
    
    best_row = original_rows[best_idx]
    goals = {header[i]: best_row[i] for i in goal_indices}
    print(f"Goal values for the selected setup: {goals}")
    print("-" * 50)
    print("This configuration minimizes risk by balancing cost, score, and idle time.")
    
    exit(0)

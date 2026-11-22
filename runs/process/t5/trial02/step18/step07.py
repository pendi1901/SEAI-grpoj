import ezr
import random

def choose(header, rows, label):
    """
    Find the best row using a budget of 50 labels.
    We use the acquire logic from ezr to intelligently sample the space.
    """
    # Create a TBL object to manage the data.
    # We initialize it with the header and all rows (currently with '?' in goals).
    tbl = ezr.Tbl([header] + rows)
    
    # We need to track which rows have been labeled to avoid re-labeling
    # and to satisfy the 50-label budget constraint.
    labeled_indices = {}

    def oracle_wrapper(row):
        # Find the index of this row in the original list
        idx = rows.index(row)
        if idx not in labeled_indices:
            true_row = label(idx)
            # Update the row in place so the table sees the real values
            for i in range(len(row)):
                row[i] = true_row[i]
            labeled_indices[idx] = row
        return row

    # The issue in the previous version was that acquire() expects the 
    # input TBL to have rows that it can sample from. 
    # We pass the table with all rows (masked) and the oracle wrapper.
    # ezr.acquire handles the logic of picking rows and calling the oracle.
    labeled_data = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # After acquiring, find the best row among all labeled ones.
    # A row is better if its ydist is lower.
    # We use the table's internal state which was updated by the oracle.
    best_row = min(labeled_data, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Mask the goals for the choose function
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    def label(i):
        return all_rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label)
    
    print(f"Best setup found at index: {best_idx}")
    print(f"Row data: {all_rows[best_idx]}")

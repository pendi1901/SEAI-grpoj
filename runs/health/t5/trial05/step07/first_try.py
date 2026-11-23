import ezr
import random

def choose(header, rows, label):
    """
    Find the best setup by using the acquire logic from ezr.
    We have a budget of 50 labels. We use the 'acquire' function
    which is designed to find the best rows in a multi-objective space.
    """
    # Create a table object to handle the data
    # We need to ensure the rows have the correct structure for ezr
    tbl = ezr.Tbl([header] + rows)
    
    # The 'acquire' function in ezr performs active learning to find
    # the best rows within a budget (the.Stop).
    # It returns the rows that were labeled.
    # We need to map the labeled rows back to their original indices.
    
    # We need to track which rows we have already labeled to return the index
    labeled_rows = []
    
    def oracle_wrapper(row):
        # Find the index of the row in the original list
        # Since rows might be identical, we look for the first match
        # that hasn't been labeled yet.
        for i, r in enumerate(rows):
            if r == row and i not in [idx for idx, _ in labeled_rows]:
                labeled_rows.append((i, label(row)))
                return labeled_rows[-1][1]
        return label(row)

    # Use the acquire function to explore the space
    # It will call our oracle_wrapper up to 50 times
    ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Now we have a set of labeled rows. Find the best one among them.
    # We create a temporary table of the labeled rows to use ydist
    labeled_data = [header] + [r for _, r in labeled_rows]
    best_tbl = ezr.Tbl(labeled_data)
    
    best_idx = -1
    best_ydist = 1e30
    
    for i, row in labeled_rows:
        d = ezr.ydist(best_tbl, row)
        if d < best_ydist:
            best_ydist = d
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    all_rows = list(data_iter)
    
    # The customer wants to find the best row.
    # We simulate the label function.
    def label(row):
        return row # In this dataset, the goals are already present
    
    # Mask the goals for the choose function
    masked_rows = []
    for row in all_rows:
        masked_row = ["?"] * 3 + row[3:]
        masked_rows.append(masked_row)
        
    best_index = choose(header, masked_rows, label)
    
    print(f"Analysis complete.")
    print(f"The best configuration found is at index {best_index}.")
    print(f"Row data: {all_rows[best_index]}")

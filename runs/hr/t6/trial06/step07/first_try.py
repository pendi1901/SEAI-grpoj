import ezr
import random

def choose(header, rows, label):
    """
    Finds the best row by using the 'acquire' strategy from ezr.
    We label up to 50 rows, then return the index of the best one found.
    """
    # Create a table object to manage the data
    tbl = ezr.Tbl([header] + rows)
    
    # We need to map the labeled rows back to their original indices.
    # Since label(i) returns the row with goals filled, we track them.
    labeled_rows = {}
    
    def oracle_wrapper(row):
        # Find the original index of this row to keep track
        # We search for the row in the original list
        for i, r in enumerate(rows):
            if r == row:
                labeled_row = label(i)
                labeled_rows[i] = labeled_row
                return labeled_row
        return row

    # Use ezr.acquire to select and label the most informative rows
    # This respects the budget (the.Stop=50)
    ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among those we labeled
    best_idx = -1
    best_ydist = 1e30
    
    for idx, row in labeled_rows.items():
        d = ezr.ydist(tbl, row)
        if d < best_ydist:
            best_ydist = d
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    file_path = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    # Create a local copy of rows with goals masked for the simulation
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    def label(i):
        return rows[i]
    
    best_idx = choose(header, masked_rows, label)
    
    print(f"Best employee arrangement found at index: {best_idx}")
    print("This row was identified using the active learning 'acquire' strategy.")
    print("It represents the optimal configuration based on the 50-interview budget.")

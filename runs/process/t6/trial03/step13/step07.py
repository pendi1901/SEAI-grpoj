import ezr

def choose(header, rows, label):
    """
    Find the best row by using the acquire logic from ezr.
    We label up to 50 rows and return the index of the best one found.
    """
    # Create a table object. We must provide rows that have valid data 
    # for columns, but since goals are '?', we must handle them carefully.
    # ezr.Tbl expects rows to match the header length.
    tbl = ezr.Tbl([header] + rows)
    
    # Track labeled rows to find the best one later
    labeled_results = []

    def tracked_label(row):
        # Find the original index of this row by comparing object identity
        # or content. Since rows are lists, we use index.
        idx = rows.index(row)
        true_row = label(idx)
        labeled_results.append((idx, true_row))
        return true_row

    # Use ezr.acquire to pick the best rows to label.
    # Note: acquire expects the rows in tbl to be the ones it can sample.
    ezr.acquire(tbl, cap=50, label=tracked_label)
    
    # Find the best row among those we labeled.
    # We use the full table context to calculate ydist.
    best_idx = -1
    best_ydist = 1e30
    
    for idx, row in labeled_results:
        d = ezr.ydist(tbl, row)
        if d < best_ydist:
            best_ydist = d
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    # Keep a copy of full data to act as the oracle
    full_data = [list(r) for r in data[1:]]
    
    # Prepare rows with '?' for goals as per instructions
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for r in full_data:
        new_row = list(r)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
    
    def label(i):
        return full_data[i]
    
    best_idx = choose(header, masked_rows, label)
    
    print(f"Optimization complete.")
    print(f"The best row found is at index: {best_idx}")
    goals = [full_data[best_idx][i] for i in goal_indices]
    print(f"Goal values for this row: {goals}")

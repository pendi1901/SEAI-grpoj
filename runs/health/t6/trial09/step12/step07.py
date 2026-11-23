import ezr

def choose(header, rows, label):
    """
    Find the best setup by using the acquire logic from ezr.
    We have a budget of 50 labels.
    """
    # We need to track the original indices because rows are modified
    # during the acquisition process.
    indexed_rows = []
    for i, row in enumerate(rows):
        indexed_rows.append({'idx': i, 'row': list(row)})

    # Create a table structure to manage the data.
    # We use the first row to initialize columns.
    data = [header] + [item['row'] for item in indexed_rows]
    tbl = ezr.Tbl(data)

    # We wrap the label function to map back to the original index.
    # ezr.acquire expects a function that takes a row and returns a row with goals filled.
    def oracle_wrapper(row):
        # Find the original index by matching the row content
        for item in indexed_rows:
            if item['row'] == row:
                revealed = label(item['idx'])
                # Update the row in place
                for i, val in enumerate(revealed):
                    row[i] = val
                return row
        return row

    # Use ezr.acquire to spend the budget of 50 labels.
    # This returns the rows that were labeled.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones using ydist.
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Find the original index of the best row.
    # We compare the row content to find the original index.
    for item in indexed_rows:
        if item['row'] == best_row:
            return item['idx']
            
    return 0

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Create a copy of rows with goals masked as '?'
    masked_rows = []
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
    
    # Define the label function for the harness
    def label_func(i):
        return all_rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Analysis complete. Best setup found at index: {best_idx}")
    goal_vals = [all_rows[best_idx][i] for i in goal_indices]
    print(f"Best row goals: {goal_vals}")
    exit(0)

import ezr
import step01

def choose(header, rows, label):
    """
    Find the best row by using the acquire logic from ezr.
    We label up to 50 rows and return the index of the best one found.
    """
    # Create a table structure to handle the data
    # We need to preserve the original indices to return the correct position
    indexed_rows = []
    for i, row in enumerate(rows):
        new_row = list(row)
        new_row.append(i)  # Keep track of original index
        indexed_rows.append(new_row)
    
    # Update header to include the index column as a skip
    new_header = header + ["idxX"]
    
    # Use ezr's acquire logic to pick rows to label
    # We define a wrapper for the oracle to handle our indexed rows
    def wrapped_label(row):
        idx = row[-1]
        true_goals = label(idx)
        # Update the row with true goals
        for i, name in enumerate(header):
            if name[-1] in "+-":
                row[i] = true_goals[i]
        return row

    tbl = ezr.Tbl([new_header] + indexed_rows)
    
    # Run the acquisition process
    # ezr.acquire returns the rows that were labeled
    labeled_rows = ezr.acquire(tbl, cap=50, label=wrapped_label)
    
    # Find the best row among the labeled ones
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    return int(best_row[-1])

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define the oracle that reveals the hidden goals
    def oracle(idx):
        return rows[idx]
    
    # Mask the goals in the rows provided to choose
    masked_rows = []
    for row in rows:
        masked_row = [row[i] if header[i][-1] not in "+-" else "?" 
                      for i in range(len(row))]
        masked_rows.append(masked_row)
        
    best_idx = choose(header, masked_rows, oracle)
    
    print(f"Optimization complete. Best row found at index: {best_idx}")
    print(f"Best row data: {rows[best_idx]}")

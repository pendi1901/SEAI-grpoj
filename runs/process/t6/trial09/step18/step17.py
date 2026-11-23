import ezr

def choose(header, rows, label):
    """
    Find the best setup for a high-stakes project.
    We use the acquire strategy from ezr. To avoid the TypeError 
    encountered previously, we ensure that the table is initialized 
    with the full header and that we only pass fully-labeled rows 
    to the acquire function.
    """
    # Create a table object.
    tbl = ezr.Tbl([header])
    
    # We need to track the original index of the rows.
    row_to_idx = {id(row): i for i, row in enumerate(rows)}
    
    # The acquire function expects a table that already has some data 
    # to define the column statistics (mu, sd).
    # We label the initial set (the.Start) to populate the table.
    labeled_data = []
    for i in range(min(len(rows), ezr.the.Start)):
        true_row = label(i)
        labeled_data.append(true_row)
        ezr.addRow(tbl, true_row)
        
    # Define an oracle that updates the table as it labels
    def oracle_wrapper(row):
        # Find the index of this row
        idx = row_to_idx[id(row)]
        true_row = label(idx)
        # Update the row in place
        for i in range(len(true_row)):
            row[i] = true_row[i]
        # Update the table's internal column statistics
        ezr.addCols(tbl, true_row)
        return row

    # Run the acquisition process.
    # We pass the rows with masked goals.
    final_labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among those labeled.
    best_row = min(final_labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    return row_to_idx[id(best_row)]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    full_data = list(ezr.csv(filename))
    header = full_data[0]
    full_rows = full_data[1:]
    
    # Prepare rows with masked goals
    rows = []
    for r in full_rows:
        new_row = r[:]
        for i, h in enumerate(header):
            if h[-1] in "+-":
                new_row[i] = "?"
        rows.append(new_row)
                
    # Define the oracle to reveal true values
    def label(idx):
        return full_rows[idx]
        
    # Run the optimization
    best_idx = choose(header, rows, label)
    
    # Print a summary for the customer
    print("High-Stakes Project Optimization Report:")
    print(f"Optimization complete using a budget of 50 labels.")
    print(f"The best configuration found is at index: {best_idx}")
    print(f"Goal values for this configuration: {full_rows[best_idx][9:]}")
    print("This setup was selected to minimize risk and maximize performance.")
    
    exit(0)

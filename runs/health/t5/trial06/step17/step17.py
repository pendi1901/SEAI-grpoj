import ezr
import random

def choose(header, rows, label):
    """
    Finds a setup that balances performance (low ydist) and efficiency (small size).
    We define 'small' as having a low N_estimators value.
    We use the acquire strategy to explore the space within a 50-label budget.
    """
    # Create a table structure to manage the data
    tbl = ezr.Tbl([header] + rows)
    
    # We define a custom objective: minimize ydist AND minimize N_estimators.
    # Since ydist is already a normalized distance to the ideal, we can 
    # add a penalty for high N_estimators (index 3).
    # N_estimators ranges from ~10 to 200.
    def combined_score(row):
        yd = ezr.ydist(tbl, row)
        # Normalize N_estimators to 0..1 range for the penalty
        n_est = row[3]
        penalty = (n_est - 10) / (200 - 10)
        return yd + (0.2 * penalty) # 0.2 weight for size penalty

    # Budget constraint
    ezr.the.Stop = 50
    
    # Track labeled rows to ensure we don't exceed 50
    labeled_data = {}

    def oracle_wrapper(row):
        # Find index by content
        for i, r in enumerate(rows):
            if r == row:
                if i not in labeled_data:
                    if len(labeled_data) >= 50:
                        return row
                    labeled_data[i] = label(i)
                
                true_vals = labeled_data[i]
                new_row = list(row)
                for col_idx, col in enumerate(header):
                    if col[-1] in "+-":
                        new_row[col_idx] = true_vals[col_idx]
                return new_row
        return row

    # Perform the acquisition
    # We use the acquire function to intelligently sample the space
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones based on our combined score
    best_row = min(labeled_rows, key=combined_score)
    
    # Return the index of the best row
    for i, r in enumerate(rows):
        if r == best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    
    if not data:
        print("No data found.")
        exit(1)
        
    header = data[0]
    rows = data[1:]
    
    # Define the label function for the harness
    def label_func(i):
        return rows[i]

    # Run the choice function
    best_idx = choose(header, rows, label_func)
    
    print(f"Search complete. The best setup found is at index {best_idx}.")
    print(f"Setup details: {rows[best_idx]}")
    print("This setup was selected for balancing high performance with a smaller footprint.")
    
    exit(0)

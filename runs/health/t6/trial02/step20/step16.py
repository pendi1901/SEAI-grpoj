import ezr
import step02
import step06

def justify(header, rows, row):
    """
    Estimates the performance of a 'big/deep' configuration and compares it
    to the population to explain why 'bigger' is not always 'better'.
    """
    # Create a table to use ezr's distance metrics
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goals for the target row using the nearest neighbor logic
    # This mimics the behavior of the configuration in the existing dataset
    best_neighbor = min(rows, key=lambda r: ezr.xdist(tbl, row, r))
    
    # Calculate ydist for the target row (using the estimated goals)
    # and for all rows in the dataset
    target_ydist = ezr.ydist(tbl, best_neighbor)
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Calculate p: fraction of rows that are worse (have higher ydist) than our target
    # A lower ydist is better, so we count how many rows have a higher ydist
    better_than_count = sum(1 for d in all_ydists if d > target_ydist)
    p = better_than_count / len(rows)
    
    reason = (f"Choosing the biggest, deepest setup is not always optimal because "
              f"this configuration is only better than {p:.2f} of all known setups, "
              f"suggesting that excessive complexity often leads to diminishing returns.")
    
    return p, reason

if __name__ == "__main__":
    # Load data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Define a "big/deep" configuration: high N_estimators, high Max_depth
    # Based on the header: N_estimators (idx 3), Max_depth (idx 7)
    # We create a hypothetical "big" row
    big_row = [0.0] * len(header)
    for i, h in enumerate(header):
        if h == "N_estimators": big_row[i] = 200.0
        elif h == "Max_depth": big_row[i] = 20.0
        elif h == "Min_sample_leaves": big_row[i] = 1.0
        elif h == "Min_impurity_decrease": big_row[i] = 0.0
        elif h == "criterion": big_row[i] = "squared_error"
        elif h[-1] in "+-": big_row[i] = "?"
        else: big_row[i] = 0.0
        
    p, reason = justify(header, rows, big_row)
    
    print(f"Justification Score (p): {p:.4f}")
    print(f"Reason: {reason}")

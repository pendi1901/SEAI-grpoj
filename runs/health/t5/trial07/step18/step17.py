import ezr
import random

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (low ydist) and is small.
    We define 'small' as having a low 'N_estimators' value.
    We use the acquire strategy to explore the space, but prioritize
    rows that are both accurate and have low N_estimators.
    """
    # Create a table object to manage column roles
    tbl = ezr.Tbl([header] + rows)
    
    # Identify the index for N_estimators to penalize large models
    n_est_idx = -1
    for i, name in enumerate(header):
        if name == "N_estimators":
            n_est_idx = i
            break
            
    # We need to track which rows we have already labeled
    # We use a dictionary to store the full row objects once labeled
    labeled_data = {}

    def oracle_wrapper(row):
        # Find the index of this row in the original rows list
        # We compare by identity or content
        for i, r in enumerate(rows):
            if r is row:
                if i not in labeled_data:
                    labeled_data[i] = label(i)
                return labeled_data[i]
        return row

    # We perform the acquisition using the standard acquire function.
    # To favor smaller models, we will evaluate the results of the 
    # acquisition process by applying a penalty to the ydist.
    
    # Run the acquisition process
    # Note: acquire() uses the table's internal ydist logic.
    # We will select the best row from the acquired set based on our custom criteria.
    best_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    def penalized_score(row):
        # Get the base ydist
        base_dist = ezr.ydist(tbl, row)
        # Normalize N_estimators to 0..1 range for penalty
        # Based on the data, N_estimators ranges roughly from 100 to 200
        size_penalty = (row[n_est_idx] - 100) / 100
        return base_dist + (0.1 * size_penalty)

    # Find the best row among those acquired
    best_row = min(best_rows, key=penalized_score)
    
    # Find the index of the best row
    for i, r in enumerate(rows):
        if r is best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Mask goals
    masked_rows = []
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(idx):
        return rows[idx]
    
    random.seed(1234567891)
    best_idx = choose(header, masked_rows, label)
    
    print("Optimization Analysis: Finding a high-performance, small-footprint configuration.")
    print(f"The best configuration found is at index {best_idx}.")
    print(f"Configuration details: {rows[best_idx]}")
    print("This setup balances predictive accuracy with a smaller model size for nightly execution.")

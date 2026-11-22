import ezr
import random

def choose(header, rows, label):
    """
    Finds a setup that is both high-performing (low ydist) and 'small' 
    (low N_estimators). We use a multi-objective approach to balance 
    performance and resource usage.
    """
    # Set the labeling budget
    ezr.the.Stop = 50
    
    # Create a table to manage the data
    tbl = ezr.Tbl([header] + rows)
    
    # We need to track labeled rows
    labeled_indices = {}
    
    def oracle(row):
        # Find the index of the row to label
        for i, r in enumerate(rows):
            if r is row:
                if i not in labeled_indices:
                    goals = label(i)
                    for col in tbl.y:
                        row[col.at] = goals[col.at]
                    labeled_indices[i] = row
                return row
        return row

    # Use the acquire strategy to find promising candidates
    # This focuses on areas of the search space that are likely to be optimal
    labeled = ezr.acquire(tbl, cap=50, label=oracle)
    
    # Define a custom score: 
    # We want low ydist (performance) and low N_estimators (cost).
    # N_estimators is at index 3.
    n_est_idx = 3
    
    # Normalize N_estimators to 0-1 range for comparison with ydist
    all_n = [r[n_est_idx] for r in rows if r[n_est_idx] != "?"]
    min_n, max_n = min(all_n), max(all_n)
    
    def score(row):
        yd = ezr.ydist(tbl, row)
        norm_n = (row[n_est_idx] - min_n) / (max_n - min_n + 1e-32)
        # Balance performance and size (50/50 weight)
        return (yd * 0.5) + (norm_n * 0.5)

    # Find the best row among the labeled ones based on our balanced score
    best_row = min(labeled, key=score)
    
    # Return the index of the best row
    for i, r in enumerate(rows):
        if r is best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals in the rows
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for col in ezr.Tbl([header]).y:
            new_row[col.at] = "?"
        masked_rows.append(new_row)
        
    def label(i):
        return data[i+1]
        
    best_idx = choose(header, masked_rows, label)
    
    print(f"Optimization complete. Best setup found at index: {best_idx}")
    print("Setup details:")
    for h, v in zip(header, rows[best_idx]):
        print(f"  {h}: {v}")

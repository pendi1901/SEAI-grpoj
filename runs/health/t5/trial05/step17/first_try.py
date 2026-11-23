import ezr
import random

def choose(header, rows, label):
    """
    Finds a setup that is both high-performing (low ydist) and small (low N_estimators).
    We use a multi-objective approach: we want to minimize ydist AND minimize N_estimators.
    """
    # Create a table to handle column roles
    tbl = ezr.Tbl([header] + rows)
    
    # We want to minimize ydist (performance) and N_estimators (cost).
    # We create a custom ranking function that balances these two.
    # N_estimators is at index 3.
    n_est_idx = header.index("N_estimators")
    
    # Normalize N_estimators to 0..1 to make it comparable to ydist
    def cost(row):
        val = row[n_est_idx]
        # Simple min-max normalization based on observed data
        return (val - 50) / (200 - 50)

    # We use the acquire logic to find candidates, but we bias the selection
    # towards rows that are both performant and small.
    # We label up to 50 rows.
    labeled = {}
    
    def oracle_wrapper(row):
        # Find original index
        for i, r in enumerate(rows):
            if r[3:] == row[3:]:
                if i not in labeled:
                    labeled[i] = label(r)
                return labeled[i]
        return label(row)

    # Use acquire to explore the space
    ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Evaluate the labeled rows based on a combined score:
    # Score = ydist + weight * cost
    best_idx = -1
    best_score = 1e30
    
    for i, row in labeled.items():
        # ydist is the performance metric
        perf = ezr.ydist(tbl, row)
        # cost is the size metric
        c = cost(row)
        # Combined score (equal weight)
        score = perf + c
        
        if score < best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    all_rows = list(data_iter)
    
    # Mask goals
    masked_rows = [["?"] * 3 + r[3:] for r in all_rows]
    
    def label(row):
        # Find original row by matching inputs
        for r in all_rows:
            if r[3:] == row[3:]:
                return r
        return row

    best_index = choose(header, masked_rows, label)
    
    print("--- Optimization Analysis: Performance vs. Size ---")
    print(f"The best configuration found for nightly runs is at index {best_index}.")
    print(f"Row data: {all_rows[best_index]}")
    print("This setup balances high predictive accuracy with a smaller model size.")

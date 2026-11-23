import ezr
import random

def choose(header, rows, label):
    """
    Finds a setup that is both high-performing (low ydist) and small (low N_estimators).
    We use a multi-objective approach: we want to minimize ydist AND minimize N_estimators.
    """
    # Create a table to handle column roles
    tbl = ezr.Tbl([header] + rows)
    
    # N_estimators is at index 3.
    n_est_idx = header.index("N_estimators")
    
    # We track labeled rows by their index in the original 'rows' list
    # to avoid issues with unhashable list types.
    labeled_data = {}
    
    def oracle_wrapper(row):
        # Find the index of the row in the provided rows list
        for i, r in enumerate(rows):
            # Compare inputs (columns 3 onwards)
            if r[3:] == row[3:]:
                if i not in labeled_data:
                    labeled_data[i] = label(r)
                return labeled_data[i]
        return label(row)

    # Use acquire to explore the space.
    # The acquire function will call our oracle_wrapper up to 50 times.
    ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Evaluate the labeled rows based on a combined score:
    # Score = ydist + normalized_cost
    # We normalize N_estimators to 0..1 based on the range [50, 200]
    best_idx = -1
    best_score = 1e30
    
    for i, row in labeled_data.items():
        # ydist is the performance metric (lower is better)
        perf = ezr.ydist(tbl, row)
        # cost is the size metric (lower is better)
        cost = (row[n_est_idx] - 50) / (200 - 50)
        # Combined score (equal weight)
        score = perf + cost
        
        if score < best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    all_rows = list(data_iter)
    
    # Mask goals for the choose function
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

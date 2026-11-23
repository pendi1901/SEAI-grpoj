import ezr
import random

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (low ydist) and is small (low N_estimators).
    We use the acquire strategy to explore the space, then select the best
    trade-off between performance and size.
    """
    # Create a table to handle metadata and normalization
    tbl = ezr.Tbl([header] + rows)
    
    # We need to track labeled rows to stay within the 50-label budget
    labeled_cache = {}

    def oracle_proxy(r):
        # Find the index of this row in the original list
        for i, orig in enumerate(rows):
            if r is orig:
                if i not in labeled_cache:
                    if len(labeled_cache) >= 50:
                        raise Exception("Budget exceeded")
                    labeled_cache[i] = label(i)
                # Return the row with goals filled in
                new_row = list(r)
                for j in range(len(labeled_cache[i])):
                    new_row[j] = labeled_cache[i][j]
                return new_row
        return r

    # Use the acquire strategy to intelligently sample the space
    # This focuses on areas that are likely to have good performance
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_proxy)
    
    # Now we have a set of labeled rows. We want to find one that is:
    # 1. High performance (low ydist)
    # 2. Small (low N_estimators)
    # We define a simple multi-objective score: ydist + (N_estimators / max_estimators)
    # This penalizes large setups.
    
    est_idx = header.index("N_estimators")
    all_ests = [r[est_idx] for r in labeled_rows]
    max_est = max(all_ests) if all_ests else 1.0
    
    def trade_off_score(r):
        perf = ezr.ydist(tbl, r)
        size = r[est_idx] / max_est
        return perf + (0.2 * size) # 0.2 weight on size to favor smaller models
    
    best_row = min(labeled_rows, key=trade_off_score)
    
    # Find the index of this best row in the original rows list
    for i, r in enumerate(rows):
        if r is best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    all_rows = list(data_iter)
    
    # Keep a copy of original goals to simulate the oracle
    original_goals = [row[:3] for row in all_rows]
    
    # Mask the rows for the choose function
    masked_rows = []
    for row in all_rows:
        masked_rows.append(["?" if i < 3 else val for i, val in enumerate(row)])
    
    def label_func(i):
        return original_goals[i]
    
    best_idx = choose(header, masked_rows, label_func)
    
    print("Customer Query: Find me a setup that forecasts well and is also small enough to run every night.")
    print(f"Analysis: Found an optimal trade-off at index {best_idx}.")
    print(f"Setup details: N_estimators={all_rows[best_idx][header.index('N_estimators')]}, "
          f"Goals (MRE-, ACC+, PRED40+): {all_rows[best_idx][:3]}")
    
    exit(0)

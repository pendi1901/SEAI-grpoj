import ezr
import step07
import step01

def choose(header, rows, label):
    """
    Find a setup that forecasts well (low ydist) and is small (low N_estimators).
    We use the acquire logic to explore the space, then select the best row
    based on a multi-objective score that balances performance and size.
    """
    # Create a table to manage data and metrics
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # We need to map the index back to the row for the oracle
    def oracle(row):
        idx = rows.index(row)
        goals = label(idx)
        for i, col in enumerate(header):
            if col[-1] in "+-":
                row[i] = goals.pop(0)
        return row

    # Use ezr's acquire to pick the best rows within the budget
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle)
    
    # Find the index of 'N_estimators' to penalize large models
    n_est_idx = header.index('N_estimators')
    
    # Define a score: ydist (performance) + normalized N_estimators (size)
    # Since ydist is already normalized to 0..1, we normalize N_estimators
    # to 0..1 to balance the two objectives.
    n_ests = [r[n_est_idx] for r in labeled_rows]
    min_n, max_n = min(n_ests), max(n_ests)
    
    def score(row):
        yd = ezr.ydist(tbl, row)
        norm_n = (row[n_est_idx] - min_n) / (max_n - min_n + 1e-32)
        # Weight performance higher (0.7) than size (0.3)
        return 0.7 * yd + 0.3 * norm_n
    
    best_row = min(labeled_rows, key=score)
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals for the choose function
    masked_rows = []
    for r in rows:
        new_r = list(r)
        for i, col in enumerate(header):
            if col[-1] in "+-":
                new_r[i] = "?"
        masked_rows.append(new_r)
        
    # Define the label function for the harness
    def label(i):
        return [rows[i][j] for j, col in enumerate(header) if col[-1] in "+-"]
    
    best_idx = choose(header, masked_rows, label)
    
    print(f"Optimization complete.")
    print(f"The best configuration found (balancing performance and size) is at index {best_idx} (row {best_idx + 1}).")
    
    exit(0)

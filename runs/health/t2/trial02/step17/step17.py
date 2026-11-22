import csv
import step01
import step02

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (low MRE) and is small (low N_estimators).
    We use a budget of 50 labels to sample the space, then pick the best
    based on a multi-objective score that balances MRE- and N_estimators-.
    """
    n = len(rows)
    # Sample 50 rows to get a representative view of the space
    sample_indices = [int(i * (n / 50)) for i in range(50)]
    
    for i in sample_indices:
        goals = label(i)
        rows[i][0], rows[i][1], rows[i][2] = goals
    
    # Identify indices
    mre_idx = header.index('MRE-')
    n_est_idx = header.index('N_estimators')
    
    # We want to minimize MRE and minimize N_estimators (for nightly speed)
    # Score = -(normalized_mre + normalized_n_estimators)
    mres = [rows[i][mre_idx] for i in sample_indices]
    n_ests = [rows[i][n_est_idx] for i in sample_indices]
    
    min_mre, max_mre = min(mres), max(mres)
    min_n, max_n = min(n_ests), max(n_ests)
    
    def norm(val, min_v, max_v):
        return (val - min_v) / (max_v - min_v) if max_v > min_v else 0
    
    best_idx = -1
    best_score = float('inf')
    
    for i in sample_indices:
        s_mre = norm(rows[i][mre_idx], min_mre, max_mre)
        s_n = norm(rows[i][n_est_idx], min_n, max_n)
        score = s_mre + s_n
        if score < best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    true_data = [r[:] for r in rows]
    # Hide goals
    for r in rows:
        r[0], r[1], r[2] = "?", "?", "?"

    def label(i):
        return [true_data[i][0], true_data[i][1], true_data[i][2]]

    best_idx = choose(header, rows, label)
    
    print("Customer Inquiry: 'Find me a setup that forecasts well and is also small enough to run every night.'")
    print(f"Answer: Found an optimal setup at row {best_idx + 1}.")
    print(f"Performance: MRE={true_data[best_idx][0]:.4f}, N_estimators={true_data[best_idx][3]:.0f}")

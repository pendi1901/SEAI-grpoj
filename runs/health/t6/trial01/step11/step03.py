import ezr
import step01

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they are significantly different.
    """
    # Use the stats functions from ezr to compare two lists of numbers
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Create table to identify goal columns
    tbl = ezr.Tbl([header] + rows)
    
    # Identify 'N_estimators' column index
    try:
        n_est_idx = header.index("N_estimators")
    except ValueError:
        print("Could not find N_estimators column.")
        exit(1)

    # Split into "big" (above median N_estimators) and "small" (below median)
    n_vals = [r[n_est_idx] for r in rows]
    median_n = sorted(n_vals)[len(n_vals) // 2]
    
    big_setups = [r for r in rows if r[n_est_idx] >= median_n]
    small_setups = [r for r in rows if r[n_est_idx] < median_n]
    
    # Calculate ydist for each group to measure "accuracy" (lower is better)
    big_scores = [ezr.ydist(tbl, r) for r in big_setups]
    small_scores = [ezr.ydist(tbl, r) for r in small_setups]
    
    # Certify if the difference is real
    is_same = certify(big_scores, small_scores)
    
    print(f"Comparing {len(big_setups)} big setups vs {len(small_setups)} small setups.")
    print(f"Mean ydist (Big): {sum(big_scores)/len(big_scores):.4f}")
    print(f"Mean ydist (Small): {sum(small_scores)/len(small_scores):.4f}")
    
    if is_same:
        print("Conclusion: The difference in accuracy is likely just noise.")
    else:
        print("Conclusion: The difference in accuracy is statistically significant.")

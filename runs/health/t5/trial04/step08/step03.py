import ezr

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    # Use ezr's stats module to compare the two distributions
    # same() checks for statistical difference using cliffs and ks tests
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]

    # Identify the 'N_estimators' column (index 3) as the proxy for "big" vs "small"
    # Identify the 'ACC+' column (index 1) as the performance metric
    n_est_idx = 3
    acc_idx = 1

    # Split data into two groups based on the median of N_estimators
    n_estimators = [row[n_est_idx] for row in rows]
    median_n = sorted(n_estimators)[len(n_estimators) // 2]

    small_setups = [row[acc_idx] for row in rows if row[n_est_idx] <= median_n]
    big_setups = [row[acc_idx] for row in rows if row[n_est_idx] > median_n]

    # Certify if the difference in accuracy is statistically significant
    is_same = certify(small_setups, big_setups)

    print("Analysis: Are big setups significantly more accurate than small ones?")
    if is_same:
        print("Result: The difference in accuracy is statistically insignificant (noise).")
    else:
        print("Result: The difference in accuracy is statistically significant.")
    
    print(f"Small setups (n={len(small_setups)}) mean accuracy: {sum(small_setups)/len(small_setups):.3f}")
    print(f"Big setups (n={len(big_setups)}) mean accuracy: {sum(big_setups)/len(big_setups):.3f}")

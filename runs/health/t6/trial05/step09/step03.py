import ezr
import step01

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable
    (same apart from noise), False if they are significantly different.
    Uses the statistical tests provided in ezr.
    """
    # Use the same logic as ezr.same, which checks cliffs and ks tests.
    # We sort the inputs as required by the statistical functions.
    xs_sorted = sorted(xs)
    ys_sorted = sorted(ys)
    return ezr.cliffs(xs_sorted, ys_sorted) and ezr.ks(xs_sorted, ys_sorted)

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Define "big" vs "small" based on N_estimators (index 3)
    # We use the median of N_estimators to split the data
    n_est_idx = 3
    n_estimators = [row[n_est_idx] for row in rows]
    median_n = sorted(n_estimators)[len(n_estimators) // 2]
    
    # We want to compare the accuracy (ACC+, index 1) of big vs small setups
    acc_idx = 1
    small_setups = [row[acc_idx] for row in rows if row[n_est_idx] <= median_n]
    big_setups = [row[acc_idx] for row in rows if row[n_est_idx] > median_n]
    
    # Run the certification
    is_same = certify(small_setups, big_setups)
    
    print(f"Comparing accuracy of {len(small_setups)} small setups vs {len(big_setups)} big setups.")
    print(f"Small setups mean ACC: {sum(small_setups)/len(small_setups):.4f}")
    print(f"Big setups mean ACC: {sum(big_setups)/len(big_setups):.4f}")
    
    if is_same:
        print("Result: The difference in accuracy is statistically insignificant (noise).")
    else:
        print("Result: The difference in accuracy is statistically significant (real).")

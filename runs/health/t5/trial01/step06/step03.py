import ezr

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    # We use the same logic as the stats layer in ezr.py
    # same() checks cliffs delta and KS test, which are robust for this purpose.
    return ezr.same(xs, ys)

def run_analysis():
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        return

    # Define "big" vs "small" based on N_estimators (index 3)
    # We split by the median of N_estimators
    n_est_idx = 3
    n_estimators = [row[n_est_idx] for row in rows]
    median = sorted(n_estimators)[len(n_estimators) // 2]
    
    # We use ACC+ (index 1) as the measure of accuracy
    acc_idx = 1
    small_setups = [row[acc_idx] for row in rows if row[n_est_idx] <= median]
    big_setups = [row[acc_idx] for row in rows if row[n_est_idx] > median]
    
    # Certify if they are the same
    is_same = certify(small_setups, big_setups)
    
    print("Analysis: Comparing accuracy (ACC+) of small vs big setups.")
    if is_same:
        print("Result: The difference in accuracy is statistically insignificant (noise).")
    else:
        print("Result: There is a statistically significant difference in accuracy.")
    
    print(f"Small setups mean: {sum(small_setups)/len(small_setups):.4f}")
    print(f"Big setups mean:   {sum(big_setups)/len(big_setups):.4f}")

if __name__ == "__main__":
    run_analysis()

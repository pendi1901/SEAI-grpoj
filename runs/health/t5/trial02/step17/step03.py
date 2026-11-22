import ezr
import random

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (same apart from noise), False otherwise.
    Uses the statistical tests provided in ezr.stats.
    """
    # Sort the lists as required by the statistical tests in ezr
    xs_sorted = sorted(xs)
    ys_sorted = sorted(ys)
    
    # Use the same function from ezr.stats
    # It checks cliffs, ks, and cohen's d
    return ezr.same(xs_sorted, ys_sorted)

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Create a table to identify goals and calculate ydist
    tbl = ezr.Tbl(data)
    
    # Define "big" vs "small" based on N_estimators (index 3)
    # We split by the median value of N_estimators
    n_est_idx = 3
    n_ests = [r[n_est_idx] for r in rows]
    median_n = sorted(n_ests)[len(n_ests) // 2]
    
    small_set = []
    big_set = []
    
    for row in rows:
        yd = ezr.ydist(tbl, row)
        if row[n_est_idx] <= median_n:
            small_set.append(yd)
        else:
            big_set.append(yd)
            
    # Certify if the difference in performance (ydist) is real
    is_same = certify(small_set, big_set)
    
    print("Statistical analysis of setup size vs performance:")
    if is_same:
        print("The difference between big and small setups is statistically insignificant.")
        print("Conclusion: The observed difference is likely just noise.")
    else:
        print("The difference between big and small setups is statistically significant.")
        print("Conclusion: The performance difference is real.")

import ezr
import random

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (same apart from noise), False otherwise.
    Uses the statistical tests provided in ezr.
    """
    # Sort inputs as required by the statistical tests in ezr
    xs_sorted = sorted(xs)
    ys_sorted = sorted(ys)
    
    # Use ezr.same which combines cliffs, ks, and cohen tests
    # eps=0.35 is a standard medium effect size for Cohen's d
    return ezr.same(xs_sorted, ys_sorted, eps=0.35)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(0)

    # Identify "big" vs "small" setups. 
    # 'N_estimators' is a numeric column representing setup size.
    # We find its index in the header.
    n_est_idx = header.index('N_estimators')
    
    # We use 'MRE-' as the accuracy metric (lower is better).
    mre_idx = header.index('MRE-')
    
    # Split data based on the median of N_estimators
    n_vals = [row[n_est_idx] for row in rows]
    median_n = sorted(n_vals)[len(n_vals) // 2]
    
    small_setups = [row[mre_idx] for row in rows if row[n_est_idx] <= median_n]
    big_setups = [row[mre_idx] for row in rows if row[n_est_idx] > median_n]
    
    # Certify if the difference in accuracy is statistically significant
    is_same = certify(small_setups, big_setups)
    
    print(f"Analysis of {len(rows)} records.")
    print(f"Comparing accuracy (MRE-) of small setups (N_estimators <= {median_n}) vs big setups.")
    
    if is_same:
        print("Result: The difference in accuracy is not statistically significant (it is likely noise).")
    else:
        print("Result: The difference in accuracy is statistically significant (it is real).")
    
    exit(0)

import ezr
import step01

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they differ significantly.
    """
    return ezr.same(xs, ys, eps=0.35)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Identify the column index for 'N_estimators' (a proxy for 'big' vs 'small' setup)
    # and 'ACC+' (the accuracy goal)
    n_est_idx = header.index("N_estimators")
    acc_idx = header.index("ACC+")
    
    # Split data into 'big' (above median N_estimators) and 'small' (below median)
    n_ests = [r[n_est_idx] for r in rows]
    median_n = sorted(n_ests)[len(n_ests) // 2]
    
    big_setups = [r[acc_idx] for r in rows if r[n_est_idx] >= median_n]
    small_setups = [r[acc_idx] for r in rows if r[n_est_idx] < median_n]
    
    # Compare accuracy distributions
    is_same = certify(big_setups, small_setups)
    
    print("--- Analysis: Big vs Small Setups ---")
    print(f"Big setups (N_estimators >= {median_n}): {len(big_setups)} rows")
    print(f"Small setups (N_estimators < {median_n}): {len(small_setups)} rows")
    
    if is_same:
        print("Result: The difference in accuracy is statistically insignificant (noise).")
    else:
        print("Result: There is a statistically significant difference in accuracy.")
        avg_big = sum(big_setups) / len(big_setups)
        avg_small = sum(small_setups) / len(small_setups)
        print(f"Average Accuracy - Big: {avg_big:.3f}, Small: {avg_small:.3f}")

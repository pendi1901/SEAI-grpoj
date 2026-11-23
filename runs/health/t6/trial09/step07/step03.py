import ezr
import step01

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    # Use ezr's same function which performs cliffs, ks, and cohen tests
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define "big" vs "small" based on N_estimators (index 3)
    # We split by the median of N_estimators
    n_est_idx = 3
    n_estimators = [r[n_est_idx] for r in rows]
    median = sorted(n_estimators)[len(n_estimators) // 2]
    
    # Get ydist for all rows to measure accuracy
    tbl = ezr.Tbl(data)
    
    big_setups = []
    small_setups = []
    
    for row in rows:
        yd = ezr.ydist(tbl, row)
        if row[n_est_idx] >= median:
            big_setups.append(yd)
        else:
            small_setups.append(yd)
            
    # Certify if the difference in accuracy is real
    is_same = certify(big_setups, small_setups)
    
    print(f"Analysis of {len(rows)} records.")
    print(f"Big setups (N_estimators >= {median}): {len(big_setups)} records, mean ydist={sum(big_setups)/len(big_setups):.4f}")
    print(f"Small setups (N_estimators < {median}): {len(small_setups)} records, mean ydist={sum(small_setups)/len(small_setups):.4f}")
    
    if is_same:
        print("Conclusion: The difference in accuracy is likely noise.")
    else:
        print("Conclusion: The difference in accuracy is statistically significant.")
        
    exit(0)

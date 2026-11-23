import csv

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically similar 
    (i.e., the difference is likely noise), False if they differ significantly.
    Uses a simple comparison of means relative to the standard deviation 
    (Cohen's d approach).
    """
    if not xs or not ys:
        return True
    
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    
    var_x = sum((x - mean_x) ** 2 for x in xs) / len(xs)
    var_y = sum((y - mean_y) ** 2 for y in ys) / len(ys)
    
    pooled_std = ((var_x + var_y) / 2) ** 0.5
    
    if pooled_std == 0:
        return mean_x == mean_y
    
    # Effect size (Cohen's d)
    d = abs(mean_x - mean_y) / pooled_std
    
    # If effect size is small (< 0.5), we consider it noise
    return d < 0.5

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define "big" vs "small" based on N_estimators (median split)
    n_est_idx = header.index('N_estimators')
    acc_idx = header.index('ACC+')
    
    n_ests = [r[n_est_idx] for r in rows]
    median_n = sorted(n_ests)[len(n_ests) // 2]
    
    small_setups = [r[acc_idx] for r in rows if r[n_est_idx] <= median_n]
    big_setups = [r[acc_idx] for r in rows if r[n_est_idx] > median_n]
    
    is_noise = certify(small_setups, big_setups)
    
    print("Analysis: Are 'big' setups significantly more accurate than 'small' ones?")
    if is_noise:
        print("Result: The observed difference is likely just noise.")
    else:
        print("Result: There is a statistically significant difference in accuracy.")
    
    print(f"Mean Accuracy (Small): {sum(small_setups)/len(small_setups):.4f}")
    print(f"Mean Accuracy (Big):   {sum(big_setups)/len(big_setups):.4f}")

import csv
import numpy as np
from scipy import stats
from step01 import remember

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is likely noise,
    False if they are statistically different (using Welch's t-test).
    """
    # Use Welch's t-test to compare two independent samples
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    # If p-value > 0.05, we fail to reject the null hypothesis (it's noise)
    return p_value > 0.05

def analyze_correlation(header, rows):
    """
    Checks if 'N_estimators' (a proxy for setup size) correlates with 'ACC+'
    to determine if larger setups are genuinely more accurate.
    """
    n_est_idx = header.index('N_estimators')
    acc_idx = header.index('ACC+')
    
    n_est = [row[n_est_idx] for row in rows]
    acc = [row[acc_idx] for row in rows]
    
    # Split into two groups: small (below median) and large (above median)
    median_n = np.median(n_est)
    small_acc = [acc[i] for i in range(len(n_est)) if n_est[i] <= median_n]
    large_acc = [acc[i] for i in range(len(n_est)) if n_est[i] > median_n]
    
    is_noise = certify(small_acc, large_acc)
    
    return is_noise, np.mean(small_acc), np.mean(large_acc)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
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

    is_noise, mean_small, mean_large = analyze_correlation(header, rows)
    
    print("Analysis: Are larger setups more accurate?")
    print(f"Mean Accuracy (Small Setups): {mean_small:.4f}")
    print(f"Mean Accuracy (Large Setups): {mean_large:.4f}")
    
    if is_noise:
        print("Conclusion: The observed difference is likely noise (statistically insignificant).")
    else:
        print("Conclusion: The difference is statistically significant; larger setups are genuinely more accurate.")

import csv
import numpy as np
from scipy import stats
from step01 import remember

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is likely noise,
    False if they are statistically significantly different.
    Uses Welch's t-test.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    # If p_value > 0.05, we fail to reject the null hypothesis (it's noise)
    return p_value > 0.05

def analyze_size_vs_accuracy(header, rows):
    """
    Compares accuracy (ACC+) of 'big' setups vs 'small' setups.
    'Big' is defined as N_estimators > median.
    """
    n_est_idx = header.index('N_estimators')
    acc_idx = header.index('ACC+')
    
    n_estimators = [float(row[n_est_idx]) for row in rows]
    median_n = np.median(n_estimators)
    
    big_accs = [float(row[acc_idx]) for row in rows if float(row[n_est_idx]) > median_n]
    small_accs = [float(row[acc_idx]) for row in rows if float(row[n_est_idx]) <= median_n]
    
    is_noise = certify(big_accs, small_accs)
    
    return is_noise, np.mean(big_accs), np.mean(small_accs)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
            
    is_noise, mean_big, mean_small = analyze_size_vs_accuracy(header, rows)
    
    print(f"Analysis of Setup Size vs Accuracy:")
    print(f"Mean ACC+ (Big setups): {mean_big:.4f}")
    print(f"Mean ACC+ (Small setups): {mean_small:.4f}")
    
    if is_noise:
        print("Conclusion: The observed difference is likely noise (not statistically significant).")
    else:
        print("Conclusion: The difference is statistically significant; big setups perform differently.")

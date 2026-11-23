import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is statistically 
    insignificant (noise), False if they are significantly different.
    Uses Welch's t-test to compare the means of two independent samples.
    """
    # If samples are too small, assume noise (True)
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    # Welch's t-test (equal_var=False)
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same)
    return p_value > 0.05

def load_data(filename):
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
    return header, rows

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    header, rows = load_data(filename)
    
    # Define "big" vs "small" based on N_estimators (index 3)
    # Median split to compare two groups
    n_est_idx = header.index('N_estimators')
    acc_idx = header.index('ACC+')
    
    n_ests = [r[n_est_idx] for r in rows]
    median_n = sum(n_ests) / len(n_ests)
    
    small_setups_acc = [r[acc_idx] for r in rows if r[n_est_idx] <= median_n]
    big_setups_acc = [r[acc_idx] for r in rows if r[n_est_idx] > median_n]
    
    is_noise = certify(small_setups_acc, big_setups_acc)
    
    print(f"Analysis of ACC+ for small vs big setups (N_estimators split at {median_n:.1f}):")
    if is_noise:
        print("Result: The observed difference is likely just noise (statistically insignificant).")
    else:
        print("Result: The difference is statistically significant; big setups perform differently.")

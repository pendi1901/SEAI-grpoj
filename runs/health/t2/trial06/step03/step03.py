import csv
from step01 import remember

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically similar 
    (i.e., the difference is likely noise), False if they differ significantly.
    Uses a simple mean comparison relative to the standard deviation.
    """
    if not xs or not ys:
        return True
    
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    
    # Calculate pooled standard deviation
    combined = xs + ys
    mean_all = sum(combined) / len(combined)
    var = sum((x - mean_all) ** 2 for x in combined) / len(combined)
    std = var ** 0.5
    
    if std == 0:
        return mean_x == mean_y
        
    # Cohen's d effect size: if difference is less than 0.5 std, treat as noise
    return abs(mean_x - mean_y) < (0.5 * std)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    # Define "big" vs "small" based on N_estimators (index 3)
    n_est_idx = header.index('N_estimators')
    acc_idx = header.index('ACC+')
    
    # Split data by median N_estimators
    n_ests = [r[n_est_idx] for r in rows]
    median_n = sorted(n_ests)[len(n_ests) // 2]
    
    small_setups = [r[acc_idx] for r in rows if r[n_est_idx] <= median_n]
    big_setups = [r[acc_idx] for r in rows if r[n_est_idx] > median_n]
    
    is_noise = certify(small_setups, big_setups)
    
    print("Analysis: Are big setups significantly more accurate than small ones?")
    if is_noise:
        print("Result: The observed difference is likely noise (no significant difference).")
    else:
        print("Result: There is a statistically significant difference in accuracy.")

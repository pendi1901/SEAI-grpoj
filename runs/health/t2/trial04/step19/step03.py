import csv
import math

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (no significant difference),
    False if they differ significantly. Uses a simple T-test approach.
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    mean1, mean2 = sum(xs) / n1, sum(ys) / n2
    var1 = sum((x - mean1)**2 for x in xs) / (n1 - 1)
    var2 = sum((y - mean2)**2 for y in ys) / (n2 - 1)
    
    # Standard error of the difference
    se = math.sqrt((var1 / n1) + (var2 / n2))
    if se == 0:
        return mean1 == mean2
    
    t_stat = abs(mean1 - mean2) / se
    # For a 95% confidence level, t-critical is approx 2.0
    return t_stat < 2.0

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)

    # Define "big" vs "small" based on N_estimators (median split)
    n_est_idx = header.index('N_estimators')
    acc_idx = header.index('ACC+')
    
    n_ests = [r[n_est_idx] for r in rows]
    median_n = sum(n_ests) / len(n_ests)
    
    big_setups = [r[acc_idx] for r in rows if r[n_est_idx] >= median_n]
    small_setups = [r[acc_idx] for r in rows if r[n_est_idx] < median_n]
    
    is_similar = certify(big_setups, small_setups)
    
    print("Analysis: Is the performance difference between big and small setups real?")
    if is_similar:
        print("Result: The difference is likely noise. Setup size does not significantly impact accuracy.")
    else:
        print("Result: The difference is statistically significant. Setup size impacts accuracy.")

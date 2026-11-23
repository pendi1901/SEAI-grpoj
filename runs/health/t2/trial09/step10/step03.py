import csv
import math

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (noise),
    False if they are significantly different. Uses a simple T-test approach.
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    mu1, mu2 = sum(xs) / n1, sum(ys) / n2
    var1 = sum((x - mu1) ** 2 for x in xs) / (n1 - 1)
    var2 = sum((y - mu2) ** 2 for y in ys) / (n2 - 1)
    
    # Pooled standard error
    se = math.sqrt((var1 / n1) + (var2 / n2))
    if se == 0:
        return mu1 == mu2
    
    t_stat = abs(mu1 - mu2) / se
    # Critical value for t-distribution (approx 2.0 for 95% confidence)
    return t_stat < 2.0

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

    # Define "big" vs "small" based on N_estimators (median split)
    n_est_idx = header.index('N_estimators')
    acc_idx = header.index('ACC+')
    
    n_ests = [r[n_est_idx] for r in rows]
    median_n = sorted(n_ests)[len(n_ests) // 2]
    
    small_setups = [r[acc_idx] for r in rows if r[n_est_idx] <= median_n]
    big_setups = [r[acc_idx] for r in rows if r[n_est_idx] > median_n]
    
    is_noise = certify(small_setups, big_setups)
    
    print(f"Analysis of ACC+ by setup size (N_estimators):")
    print(f"Small setups mean: {sum(small_setups)/len(small_setups):.4f}")
    print(f"Big setups mean:   {sum(big_setups)/len(big_setups):.4f}")
    
    if is_noise:
        print("Conclusion: The difference is likely just noise.")
    else:
        print("Conclusion: The difference is statistically significant.")

import csv
import math
from step01 import remember

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is likely noise,
    False if they are statistically different. Uses a simple T-test approach.
    """
    if not xs or not ys:
        return True
    
    n1, n2 = len(xs), len(ys)
    m1, m2 = sum(xs) / n1, sum(ys) / n2
    
    v1 = sum((x - m1) ** 2 for x in xs) / (n1 - 1) if n1 > 1 else 0
    v2 = sum((y - m2) ** 2 for y in ys) / (n2 - 1) if n2 > 1 else 0
    
    # Standard error of the difference
    se = math.sqrt((v1 / n1) + (v2 / n2))
    if se == 0:
        return m1 == m2
    
    t_stat = abs(m1 - m2) / se
    # Threshold for 95% confidence (approx 1.96 for large samples)
    return t_stat < 1.96

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

    # "Big setups" defined by N_estimators > median
    n_est_idx = header.index('N_estimators')
    acc_idx = header.index('ACC+')
    
    n_ests = [r[n_est_idx] for r in rows]
    median_n = sorted(n_ests)[len(n_ests) // 2]
    
    small = [r[acc_idx] for r in rows if r[n_est_idx] <= median_n]
    big = [r[acc_idx] for r in rows if r[n_est_idx] > median_n]
    
    is_noise = certify(small, big)
    
    print(f"Small setups mean ACC: {sum(small)/len(small):.4f}")
    print(f"Big setups mean ACC: {sum(big)/len(big):.4f}")
    if is_noise:
        print("Conclusion: The difference is likely noise.")
    else:
        print("Conclusion: The difference is statistically significant.")

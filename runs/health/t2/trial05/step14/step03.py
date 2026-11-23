import csv
import math

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is likely noise,
    False if they are statistically distinct. Uses a simple T-test approach.
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    m1, m2 = sum(xs) / n1, sum(ys) / n2
    v1 = sum((x - m1) ** 2 for x in xs) / (n1 - 1)
    v2 = sum((y - m2) ** 2 for y in ys) / (n2 - 1)
    
    # Standard error of the difference
    se = math.sqrt((v1 / n1) + (v2 / n2))
    if se == 0:
        return m1 == m2
    
    t_stat = abs(m1 - m2) / se
    # Threshold for 95% confidence (approx 2.0 for large samples)
    return t_stat < 2.0

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = [val if header[i] == 'criterion' else float(val) 
                                 for i, val in enumerate(row)]
                rows.append(processed_row)
        
        # "Big setups" defined by N_estimators > median
        n_est_idx = header.index('N_estimators')
        n_ests = [r[n_est_idx] for r in rows]
        median_n = sorted(n_ests)[len(n_ests) // 2]
        
        # Compare ACC+ (index 1) for big vs small setups
        acc_idx = 1
        big = [r[acc_idx] for r in rows if r[n_est_idx] > median_n]
        small = [r[acc_idx] for r in rows if r[n_est_idx] <= median_n]
        
        is_noise = certify(big, small)
        
        print(f"Analysis of ACC+ for big vs small setups:")
        print(f"Big setups mean: {sum(big)/len(big):.4f}")
        print(f"Small setups mean: {sum(small)/len(small):.4f}")
        if is_noise:
            print("Conclusion: The difference is likely noise.")
        else:
            print("Conclusion: The difference is statistically significant.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

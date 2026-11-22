import csv

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (noise), False if they differ significantly.
    Uses a simple A12 effect size test (non-parametric).
    """
    if not xs or not ys:
        return True
    
    def count_greater(list1, list2):
        count = 0
        for x in list1:
            for y in list2:
                if x > y:
                    count += 1
                elif x == y:
                    count += 0.5
        return count

    n, m = len(xs), len(ys)
    a12 = count_greater(xs, ys) / (n * m)
    
    # A12 threshold: 0.56 is a small effect size, 
    # 0.64 is medium, 0.71 is large.
    # If A12 is close to 0.5, they are likely the same (noise).
    return abs(a12 - 0.5) < 0.14

def analyze_correlation(header, rows):
    """
    Compares 'N_estimators' (size) against 'ACC+' (accuracy).
    Splits data into small and large setups and compares accuracy.
    """
    n_idx = header.index('N_estimators')
    acc_idx = header.index('ACC+')
    
    vals = [r[n_idx] for r in rows]
    median = sum(vals) / len(vals)
    
    small = [r[acc_idx] for r in rows if r[n_idx] <= median]
    large = [r[acc_idx] for r in rows if r[n_idx] > median]
    
    is_noise = certify(small, large)
    
    print(f"Analysis of setup size vs accuracy:")
    print(f"Small setups (N <= {median:.1f}) mean ACC: {sum(small)/len(small):.4f}")
    print(f"Large setups (N > {median:.1f}) mean ACC: {sum(large)/len(large):.4f}")
    
    if is_noise:
        print("Conclusion: The difference is likely just noise.")
    else:
        print("Conclusion: The difference is statistically significant.")
    return is_noise

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
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
            
    analyze_correlation(header, rows)

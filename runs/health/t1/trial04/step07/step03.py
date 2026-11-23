import csv

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is likely noise,
    False if they are statistically different. Uses a simple A12 effect size 
    check (Vargha-Delaney). A12 > 0.56 or < 0.44 suggests a real difference.
    """
    n_x = len(xs)
    n_y = len(ys)
    if n_x == 0 or n_y == 0:
        return True
    
    greater = 0
    equal = 0
    for x in xs:
        for y in ys:
            if x > y:
                greater += 1
            elif x == y:
                equal += 1
    
    a12 = (greater + 0.5 * equal) / (n_x * n_y)
    return 0.44 <= a12 <= 0.56

def analyze_correlation(header, rows):
    """
    Checks if 'N_estimators' (size) correlates with 'ACC+' (accuracy).
    Splits data into 'small' and 'big' based on median N_estimators.
    """
    n_idx = header.index('N_estimators')
    acc_idx = header.index('ACC+')
    
    vals = [r[n_idx] for r in rows]
    median = sorted(vals)[len(vals) // 2]
    
    small = [r[acc_idx] for r in rows if r[n_idx] <= median]
    big = [r[acc_idx] for r in rows if r[n_idx] > median]
    
    is_noise = certify(small, big)
    
    print(f"Analysis of Accuracy vs Setup Size (N_estimators):")
    print(f"Small setups (<= {median}): {len(small)} rows, Avg ACC: {sum(small)/len(small):.4f}")
    print(f"Big setups (> {median}): {len(big)} rows, Avg ACC: {sum(big)/len(big):.4f}")
    
    if is_noise:
        print("Conclusion: The difference is likely noise.")
    else:
        print("Conclusion: The difference is statistically significant.")
    return not is_noise

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
            
    analyze_correlation(header, rows)

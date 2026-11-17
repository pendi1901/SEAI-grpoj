import csv

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (noise), False if they differ significantly.
    Uses a simple A12 effect size test.
    """
    if not xs or not ys:
        return True
    
    # A12 test: probability that a random value from xs is greater than ys
    greater = 0
    equal = 0
    for x in xs:
        for y in ys:
            if x > y:
                greater += 1
            elif x == y:
                equal += 0.5
    
    a12 = (greater + equal) / (len(xs) * len(ys))
    
    # Threshold for "significant" difference (standard A12 threshold is 0.56)
    # If A12 is close to 0.5, they are likely the same (noise).
    return abs(a12 - 0.5) < 0.06

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append(row)

    # Identify N_estimators column (index 3) and MRE- column (index 0)
    # N_estimators is numeric (starts with upper case)
    n_est_idx = 3
    mre_idx = 0
    
    # Split data into "small" and "big" based on median N_estimators
    n_vals = [float(row[n_est_idx]) for row in rows]
    median_n = sorted(n_vals)[len(n_vals) // 2]
    
    small_setups = [float(row[mre_idx]) for row in rows if float(row[n_est_idx]) <= median_n]
    big_setups = [float(row[mre_idx]) for row in rows if float(row[n_est_idx]) > median_n]
    
    is_noise = certify(small_setups, big_setups)
    
    print("Analysis of N_estimators impact on MRE-:")
    if is_noise:
        print("Result: The difference between small and big setups is statistically insignificant (noise).")
    else:
        print("Result: The difference between small and big setups is real and significant.")
    
    avg_small = sum(small_setups) / len(small_setups)
    avg_big = sum(big_setups) / len(big_setups)
    print(f"Average MRE- (Small): {avg_small:.4f}")
    print(f"Average MRE- (Big):   {avg_big:.4f}")

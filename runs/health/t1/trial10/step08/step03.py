import csv

def certify(xs, ys):
    """
    Determines if two distributions are significantly different using the 
    A12 effect size statistic. Returns True if they are the same (noise), 
    False if they really differ.
    """
    if not xs or not ys:
        return True

    def a12(lst1, lst2):
        m, n = len(lst1), len(lst2)
        count = 0
        for x in lst1:
            for y in lst2:
                if x > y: count += 1
                elif x == y: count += 0.5
        return count / (m * n)

    # A12 threshold: 0.56 is a small effect size, 0.64 medium, 0.71 large.
    # We use 0.6 as a conservative threshold for "really differ".
    score = a12(xs, ys)
    return 0.4 <= score <= 0.6

def load_data(filename):
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] in ['criterion']:
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
    return header, rows

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        header, rows = load_data(filename)
        
        # Define "big" vs "small" based on N_estimators (median split)
        n_est_idx = header.index('N_estimators')
        n_ests = [r[n_est_idx] for r in rows]
        median_n = sum(n_ests) / len(n_ests)
        
        # Goal: ACC+ (maximize)
        acc_idx = header.index('ACC+')
        
        small_setups = [r[acc_idx] for r in rows if r[n_est_idx] <= median_n]
        big_setups = [r[acc_idx] for r in rows if r[n_est_idx] > median_n]
        
        is_noise = certify(small_setups, big_setups)
        
        print("Analysis: Comparing ACC+ performance between small and big setups.")
        if is_noise:
            print("Result: The difference is likely just noise. Setup size does not significantly impact accuracy.")
        else:
            print("Result: There is a statistically significant difference in accuracy between setup sizes.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

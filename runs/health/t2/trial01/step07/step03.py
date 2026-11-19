import csv
import math

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (noise),
    False if they are significantly different. Uses a simple A12 effect size
    check (Vargha-Delaney).
    """
    def a12(lst1, lst2):
        m, n = len(lst1), len(lst2)
        lst1, lst2 = sorted(lst1), sorted(lst2)
        r1 = 0
        for x in lst1:
            for y in lst2:
                if x > y: r1 += 1
                elif x == y: r1 += 0.5
        return abs(0.5 - (r1 / (m * n))) > 0.15

    # If the difference is small (A12 < 0.15), it's likely noise.
    return not a12(xs, ys)

def load_data(filename):
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed.append(float(val))
                else:
                    processed.append(val)
            rows.append(processed)
    return header, rows

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        header, rows = load_data(filename)
        
        # Define "big" vs "small" based on N_estimators (median split)
        n_est_idx = header.index('N_estimators')
        mre_idx = header.index('MRE-')
        
        n_ests = [r[n_est_idx] for r in rows]
        median_n = sum(n_ests) / len(n_ests)
        
        small_setups = [r[mre_idx] for r in rows if r[n_est_idx] <= median_n]
        big_setups = [r[mre_idx] for r in rows if r[n_est_idx] > median_n]
        
        is_noise = certify(small_setups, big_setups)
        
        print("Analysis: Is the performance difference between big and small setups real?")
        if is_noise:
            print("Answer: The difference is likely just noise.")
        else:
            print("Answer: The difference is statistically significant.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

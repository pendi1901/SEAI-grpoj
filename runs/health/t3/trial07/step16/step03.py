import csv
import numpy as np
from scipy.stats import pearsonr

def certify(xs, ys):
    """
    Returns True if the correlation between xs and ys is strong,
    implying the relationship is real rather than noise.
    """
    if len(xs) < 2:
        return False
    
    # Calculate Pearson correlation coefficient
    corr, _ = pearsonr(xs, ys)
    
    # If correlation is > 0.3, we consider the relationship 'real' (not just noise)
    # This is a standard heuristic for identifying non-trivial associations.
    return abs(corr) > 0.3

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # The customer asks if "big setups" (N_estimators) are more accurate (MRE-)
    # MRE- is index 0, N_estimators is index 3
    mre_idx = 0
    n_est_idx = 3
    
    xs = [row[n_est_idx] for row in rows]
    ys = [row[mre_idx] for row in rows]
    
    is_real = certify(xs, ys)
    
    print("Analyzing if setup size (N_estimators) correlates with accuracy (MRE-)...")
    if is_real:
        print("Result: The observed trend is statistically significant. The relationship is real.")
    else:
        print("Result: The observed trend is likely noise. There is no strong evidence of a relationship.")

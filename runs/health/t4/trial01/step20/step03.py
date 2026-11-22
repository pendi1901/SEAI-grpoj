import csv
import numpy as np
from scipy.stats import pearsonr
from step01 import remember

def certify(xs, ys):
    """
    Returns True if the correlation between two lists is high (suggesting 
    the relationship is real), False if it is likely noise.
    """
    if len(xs) < 2:
        return False
    corr, _ = pearsonr(xs, ys)
    # If correlation is > 0.3, we consider the trend significant/real
    return abs(corr) > 0.3

def analyze_correlation(header, rows):
    """
    Checks if 'N_estimators' (a proxy for setup size) correlates with 
    'ACC+' (a proxy for accuracy).
    """
    idx_acc = header.index('ACC+')
    idx_size = header.index('N_estimators')
    
    sizes = [row[idx_size] for row in rows]
    accuracies = [row[idx_acc] for row in rows]
    
    is_real = certify(sizes, accuracies)
    return is_real

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed.append(float(val))
                else:
                    processed.append(val)
            rows.append(processed)

    result = analyze_correlation(header, rows)
    
    print("Analysis of Setup Size vs Accuracy:")
    if result:
        print("The observation is real: there is a statistically significant correlation between setup size and accuracy.")
    else:
        print("The observation is likely noise: there is no significant correlation between setup size and accuracy.")

import csv
import numpy as np
from scipy.stats import ttest_ind
from step03 import certify as step03_certify

def certify(xs, ys):
    """
    Returns True if the two lists of numbers are statistically indistinguishable 
    (i.e., the choice of rule makes no real difference), False if they differ.
    Uses a t-test to compare the means of the two groups.
    """
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    # Perform an independent t-test
    t_stat, p_value = ttest_ind(xs, ys, equal_var=False)
    
    # If p-value > 0.05, we fail to reject the null hypothesis (no significant difference)
    return p_value > 0.05

def analyze_rules(header, rows):
    """
    Compares the performance of different 'criterion' settings.
    """
    idx_crit = header.index('criterion')
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    def get_score(row):
        return (1.0 - row[idx_mre]) + row[idx_acc] + row[idx_pred]

    # Group scores by criterion
    groups = {}
    for row in rows:
        crit = row[idx_crit]
        if crit not in groups:
            groups[crit] = []
        groups[crit].append(get_score(row))

    # Compare the two most common criteria: 'absolute_error' and 'squared_error'
    if 'absolute_error' in groups and 'squared_error' in groups:
        return certify(groups['absolute_error'], groups['squared_error'])
    return True

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
                    try:
                        processed.append(float(val))
                    except ValueError:
                        processed.append(0.0)
                else:
                    processed.append(val)
            rows.append(processed)

    is_same = analyze_rules(header, rows)
    
    print("Analysis of 'criterion' rule choice:")
    if is_same:
        print("The choice between rules makes no real difference. You can stop arguing about it.")
    else:
        print("The choice between rules results in statistically significant performance differences.")

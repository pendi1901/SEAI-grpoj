import csv
from scipy.stats import ttest_ind

def certify(xs, ys):
    """
    Returns True if the two sets of results are statistically indistinguishable 
    (p-value >= 0.05), implying the choice of rule makes no real difference.
    Returns False if they are statistically different (p-value < 0.05).
    """
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    # Perform an independent two-sample t-test
    _, p_value = ttest_ind(xs, ys, equal_var=False)
    
    # If p_value >= 0.05, we fail to reject the null hypothesis (no difference)
    return p_value >= 0.05

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # We test if the choice of 'criterion' (a built-in rule parameter) 
    # makes a difference in the primary goal (MRE-).
    # We compare 'absolute_error' vs 'squared_error'.
    crit_idx = header.index('criterion')
    mre_idx = header.index('MRE-')
    
    abs_err_results = [r[mre_idx] for r in rows if r[crit_idx] == 'absolute_error']
    sq_err_results = [r[mre_idx] for r in rows if r[crit_idx] == 'squared_error']
    
    is_same = certify(abs_err_results, sq_err_results)
    
    print("Analysis: Does the choice of 'criterion' rule make a real difference?")
    if is_same:
        print("Result: The choice makes no statistically significant difference. You can stop arguing.")
    else:
        print("Result: The choice leads to statistically significant differences. It matters.")

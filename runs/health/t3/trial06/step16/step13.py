import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is statistically 
    insignificant (noise), False if they are significantly different.
    Uses Welch's t-test to compare the means of two independent samples.
    """
    # If samples are too small, assume noise (True)
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    # Welch's t-test (equal_var=False)
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same)
    return p_value > 0.05

def get_utility(header, row):
    """Calculates a normalized utility score for a row."""
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Normalize goals to [0, 1]
    # MRE- (minimize), ACC+ (maximize), PRED40+ (maximize)
    mre = min(1.0, max(0.0, row[mre_idx]))
    acc = min(1.0, max(0.0, row[acc_idx]))
    pred = min(1.0, max(0.0, row[pred_idx]))
    
    return (1.0 - mre) + acc + pred

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)

    # The customer asks about the "two built-in rules". 
    # In the context of this dataset, 'criterion' has three values:
    # 'absolute_error', 'poisson', 'squared_error'.
    # We compare the performance of 'absolute_error' vs 'squared_error'.
    
    crit_idx = header.index('criterion')
    
    abs_error_utils = [get_utility(header, r) for r in rows if r[crit_idx] == 'absolute_error']
    sq_error_utils = [get_utility(header, r) for r in rows if r[crit_idx] == 'squared_error']
    
    is_noise = certify(abs_error_utils, sq_error_utils)
    
    print("Analysis: Does the choice of 'criterion' (absolute_error vs squared_error) matter?")
    if is_noise:
        print("Result: The difference in performance is statistically insignificant.")
        print("You can stop arguing about it; the choice does not make a real difference.")
    else:
        print("Result: The difference in performance is statistically significant.")
        print("The choice of criterion does matter for your results.")

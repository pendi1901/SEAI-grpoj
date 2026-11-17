import csv
import pandas as pd
import numpy as np
from scipy import stats
from step01 import remember

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is likely noise,
    False if they are statistically significantly different.
    Uses Welch's t-test.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    # If p_value > 0.05, we fail to reject the null hypothesis (it's likely noise)
    return p_value > 0.05

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if val.replace('.', '', 1).isdigit() or 
                             (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                             else val for val in row]
            data.append(processed_row)

    df = pd.DataFrame(data, columns=header)
    
    # Define "big" vs "small" based on N_estimators (a common proxy for setup size)
    median_estimators = df['N_estimators'].median()
    small_setups = df[df['N_estimators'] <= median_estimators]['MRE-']
    big_setups = df[df['N_estimators'] > median_estimators]['MRE-']
    
    is_noise = certify(small_setups.tolist(), big_setups.tolist())
    
    print("Analysis: Comparing MRE- (error) between small and big setups.")
    if is_noise:
        print("Result: The difference in accuracy is likely just noise.")
    else:
        print("Result: The difference in accuracy is statistically significant.")
        if big_setups.mean() < small_setups.mean():
            print("Conclusion: Big setups are indeed more accurate.")
        else:
            print("Conclusion: Small setups are more accurate.")

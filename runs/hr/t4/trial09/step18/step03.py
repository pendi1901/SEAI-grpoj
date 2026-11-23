import csv
import numpy as np
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two groups is statistically 
    insignificant (noise), False if they really differ (p < 0.05).
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_overtime(header, rows):
    """
    Compares 'YearsInCurrentRole+' for employees who work overtime vs those who don't.
    """
    ot_idx = header.index('overTime')
    role_idx = header.index('YearsInCurrentRole+')
    
    yes_ot = [row[role_idx] for row in rows if row[ot_idx] == 'Yes']
    no_ot = [row[role_idx] for row in rows if row[ot_idx] == 'No']
    
    is_noise = certify(yes_ot, no_ot)
    
    print(f"Average Years in Current Role (Overtime): {np.mean(yes_ot):.2f}")
    print(f"Average Years in Current Role (No Overtime): {np.mean(no_ot):.2f}")
    if is_noise:
        print("Conclusion: The observed difference is likely just noise.")
    else:
        print("Conclusion: There is a statistically significant difference.")
    return is_noise

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
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
    
    analyze_overtime(header, rows)

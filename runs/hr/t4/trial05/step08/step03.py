import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two groups is not statistically 
    significant (noise), False if they really differ.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same)
    return p_value > 0.05

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

    # Identify columns
    overtime_idx = header.index('overTime')
    tenure_idx = header.index('YearsInCurrentRole+')

    # Split data based on overtime
    yes_overtime = [r[tenure_idx] for r in rows if r[overtime_idx] == 'Yes']
    no_overtime = [r[tenure_idx] for r in rows if r[overtime_idx] == 'No']

    # Perform certification
    is_noise = certify(yes_overtime, no_overtime)

    print("Analysis: Do people who work overtime leave their role sooner?")
    if is_noise:
        print("Result: The observed difference is likely just noise (not statistically significant).")
    else:
        print("Result: There is a statistically significant difference in tenure between these groups.")

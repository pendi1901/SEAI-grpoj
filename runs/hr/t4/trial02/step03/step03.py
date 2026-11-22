import csv
from scipy import stats

def certify(xs, ys):
    """
    Performs a Welch's t-test to determine if the means of two groups
    are statistically different. Returns True if they are likely the same
    (p-value > 0.05), False if they are significantly different.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
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
    years_idx = header.index('YearsInCurrentRole+')

    # Split data based on overtime status
    yes_overtime = [row[years_idx] for row in rows if row[overtime_idx] == 'Yes']
    no_overtime = [row[years_idx] for row in rows if row[overtime_idx] == 'No']

    # Perform certification
    is_noise = certify(yes_overtime, no_overtime)

    print("Analysis: Do people who work overtime leave their role sooner?")
    if is_noise:
        print("Result: The difference is statistically insignificant (noise).")
    else:
        print("Result: There is a statistically significant difference.")
    
    print(f"Mean years in role (Overtime): {sum(yes_overtime)/len(yes_overtime):.2f}")
    print(f"Mean years in role (No Overtime): {sum(no_overtime)/len(no_overtime):.2f}")

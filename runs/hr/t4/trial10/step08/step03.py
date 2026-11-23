import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two groups is statistically 
    insignificant (p-value > 0.05), False if they really differ.
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

    # Split data based on overtime
    yes_overtime = [row[years_idx] for row in rows if row[overtime_idx] == 'Yes']
    no_overtime = [row[years_idx] for row in rows if row[overtime_idx] == 'No']

    # Perform statistical test
    is_noise = certify(yes_overtime, no_overtime)

    print("Analysis: Do people who work overtime leave their role sooner?")
    if is_noise:
        print("Result: The observed difference is likely just noise (p > 0.05).")
    else:
        print("Result: There is a statistically significant difference in tenure.")
        avg_yes = sum(yes_overtime) / len(yes_overtime)
        avg_no = sum(no_overtime) / len(no_overtime)
        print(f"Average years in role (Overtime): {avg_yes:.2f}")
        print(f"Average years in role (No Overtime): {avg_no:.2f}")

import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two groups is statistically 
    insignificant (p > 0.05), False if they really differ.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_overtime_impact(header, rows):
    """
    Compares 'YearsInCurrentRole+' for employees who work overtime vs those who don't.
    """
    overtime_idx = header.index('overTime')
    role_years_idx = header.index('YearsInCurrentRole+')
    
    overtime_yes = [row[role_years_idx] for row in rows if row[overtime_idx] == 'Yes']
    overtime_no = [row[role_years_idx] for row in rows if row[overtime_idx] == 'No']
    
    is_noise = certify(overtime_yes, overtime_no)
    
    return is_noise, overtime_yes, overtime_no

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

    is_noise, yes_group, no_group = analyze_overtime_impact(header, rows)
    
    print("Analysis: Do people who work overtime leave their role sooner?")
    if is_noise:
        print("Result: The observed difference is likely just noise (p > 0.05).")
    else:
        print("Result: There is a statistically significant difference in tenure.")
        avg_yes = sum(yes_group) / len(yes_group)
        avg_no = sum(no_group) / len(no_group)
        print(f"Average years in role (Overtime): {avg_yes:.2f}")
        print(f"Average years in role (No Overtime): {avg_no:.2f}")

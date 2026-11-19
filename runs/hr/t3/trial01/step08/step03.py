import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the two groups are statistically similar (p > 0.05),
    False if they are significantly different (p <= 0.05).
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_overtime_impact(header, rows):
    """
    Compares 'YearsInCurrentRole+' for employees who work overtime vs those who don't.
    """
    overtime_idx = header.index('overTime')
    role_years_idx = header.index('YearsInCurrentRole+')
    
    yes_overtime = [r[role_years_idx] for r in rows if r[overtime_idx] == 'Yes']
    no_overtime = [r[role_years_idx] for r in rows if r[overtime_idx] == 'No']
    
    is_same = certify(yes_overtime, no_overtime)
    
    avg_yes = sum(yes_overtime) / len(yes_overtime)
    avg_no = sum(no_overtime) / len(no_overtime)
    
    return is_same, avg_yes, avg_no

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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
            
    is_same, avg_yes, avg_no = analyze_overtime_impact(header, rows)
    
    print("Analysis: Does Overtime affect YearsInCurrentRole?")
    print(f"Average Years (Overtime): {avg_yes:.2f}")
    print(f"Average Years (No Overtime): {avg_no:.2f}")
    
    if is_same:
        print("Conclusion: The difference is statistically insignificant (noise).")
    else:
        print("Conclusion: The difference is statistically significant (real).")

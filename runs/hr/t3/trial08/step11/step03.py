import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the two groups are statistically similar (p > 0.05),
    False if they differ significantly (p <= 0.05).
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_overtime_impact(header, rows):
    """
    Compares 'YearsInCurrentRole+' for employees who work overtime vs those who don't.
    """
    overtime_idx = header.index('overTime')
    years_idx = header.index('YearsInCurrentRole+')
    
    overtime_group = [row[years_idx] for row in rows if row[overtime_idx] == 'Yes']
    no_overtime_group = [row[years_idx] for row in rows if row[overtime_idx] == 'No']
    
    is_same = certify(overtime_group, no_overtime_group)
    
    avg_ot = sum(overtime_group) / len(overtime_group)
    avg_no_ot = sum(no_overtime_group) / len(no_overtime_group)
    
    return is_same, avg_ot, avg_no_ot

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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    is_same, avg_ot, avg_no_ot = analyze_overtime_impact(header, rows)
    
    print("Analysis: Does Overtime affect YearsInCurrentRole?")
    print(f"Average years in role (Overtime): {avg_ot:.2f}")
    print(f"Average years in role (No Overtime): {avg_no_ot:.2f}")
    
    if is_same:
        print("Conclusion: The difference is not statistically significant. It is likely just noise.")
    else:
        print("Conclusion: There is a statistically significant difference. The observation is real.")

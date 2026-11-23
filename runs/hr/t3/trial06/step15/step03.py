import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (p > 0.05),
    False if they are significantly different (p <= 0.05).
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_overtime_impact(header, rows):
    """
    Splits data into 'Overtime' and 'No Overtime' groups based on 
    'YearsInCurrentRole+' and checks if the difference is significant.
    """
    idx_overtime = header.index('overTime')
    idx_years = header.index('YearsInCurrentRole+')
    
    overtime_group = [row[idx_years] for row in rows if row[idx_overtime] == 'Yes']
    no_overtime_group = [row[idx_years] for row in rows if row[idx_overtime] == 'No']
    
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    is_same, avg_ot, avg_no_ot = analyze_overtime_impact(header, rows)
    
    print("Analysis: Does Overtime impact tenure in current role?")
    print(f"Average years in role (Overtime): {avg_ot:.2f}")
    print(f"Average years in role (No Overtime): {avg_no_ot:.2f}")
    
    if is_same:
        print("Conclusion: The difference is not statistically significant. It is likely noise.")
    else:
        print("Conclusion: There is a statistically significant difference. The impact is real.")

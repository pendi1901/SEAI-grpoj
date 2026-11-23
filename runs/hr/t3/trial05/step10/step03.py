import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the two groups are statistically indistinguishable (noise),
    False if they significantly differ. Uses a t-test for independent samples.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    # If p_value > 0.05, we fail to reject the null hypothesis (they are the same)
    return p_value > 0.05

def analyze_overtime_impact(header, rows):
    """
    Splits data by 'overTime' status and compares 'YearsAtCompany+' 
    to see if overtime workers leave sooner.
    """
    idx_overtime = header.index('overTime')
    idx_years = header.index('YearsAtCompany+')
    
    no_overtime = [r[idx_years] for r in rows if r[idx_overtime] == 'No']
    yes_overtime = [r[idx_years] for r in rows if r[idx_overtime] == 'Yes']
    
    is_noise = certify(no_overtime, yes_overtime)
    
    avg_no = sum(no_overtime) / len(no_overtime)
    avg_yes = sum(yes_overtime) / len(yes_overtime)
    
    return is_noise, avg_no, avg_yes

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
            
    is_noise, avg_no, avg_yes = analyze_overtime_impact(header, rows)
    
    print("Analysis: Does Overtime impact 'YearsAtCompany+'?")
    print(f"Average tenure (No Overtime): {avg_no:.2f} years")
    print(f"Average tenure (Yes Overtime): {avg_yes:.2f} years")
    
    if is_noise:
        print("Conclusion: The difference is statistically insignificant (likely noise).")
    else:
        print("Conclusion: There is a statistically significant difference in tenure.")

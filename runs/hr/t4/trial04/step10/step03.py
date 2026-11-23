import csv
from scipy import stats

def certify(xs, ys):
    """
    Performs a Welch's t-test to determine if two samples are 
    statistically different. Returns True if they are likely from 
    the same distribution (p > 0.05), False otherwise.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_overtime_impact(header, rows):
    """
    Compares 'YearsInCurrentRole+' for employees who work overtime 
    vs those who do not.
    """
    ot_idx = header.index('overTime')
    role_idx = header.index('YearsInCurrentRole+')
    
    yes_ot = [row[role_idx] for row in rows if row[ot_idx] == 'Yes']
    no_ot = [row[role_idx] for row in rows if row[ot_idx] == 'No']
    
    is_noise = certify(yes_ot, no_ot)
    
    print(f"Average years in role (Overtime): {sum(yes_ot)/len(yes_ot):.2f}")
    print(f"Average years in role (No Overtime): {sum(no_ot)/len(no_ot):.2f}")
    
    if is_noise:
        print("Conclusion: The difference is likely just noise.")
    else:
        print("Conclusion: The difference is statistically significant.")
    
    return is_noise

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    analyze_overtime_impact(header, rows)

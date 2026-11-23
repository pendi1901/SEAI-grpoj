import csv
from scipy import stats

def certify(xs, ys):
    """
    Performs a Welch's t-test to determine if two groups (xs and ys)
    are statistically different. Returns True if they are not 
    significantly different (p > 0.05), False otherwise.
    """
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    
    # If p > 0.05, we fail to reject the null hypothesis (no real difference)
    return p_value > 0.05

def analyze_overtime_impact(header, rows):
    """
    Splits data by 'overTime' and compares 'YearsInCurrentRole+' 
    to see if overtime workers leave sooner.
    """
    ot_idx = header.index('overTime')
    years_idx = header.index('YearsInCurrentRole+')
    
    overtime_yes = [row[years_idx] for row in rows if row[ot_idx] == 'Yes']
    overtime_no = [row[years_idx] for row in rows if row[ot_idx] == 'No']
    
    is_noise = certify(overtime_yes, overtime_no)
    
    print("Analysis: Does Overtime impact YearsInCurrentRole?")
    print(f"Average years (Overtime): {sum(overtime_yes)/len(overtime_yes):.2f}")
    print(f"Average years (No Overtime): {sum(overtime_no)/len(overtime_no):.2f}")
    
    if is_noise:
        print("Result: The difference is statistically insignificant (likely noise).")
    else:
        print("Result: There is a statistically significant difference.")
    return is_noise

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
            
    analyze_overtime_impact(header, rows)

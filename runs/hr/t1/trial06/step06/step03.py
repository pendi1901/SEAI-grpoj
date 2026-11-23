import csv

def certify(xs, ys):
    """
    Performs a simple two-sample t-test (Welch's) to determine if two 
    distributions are significantly different. Returns True if they are 
    statistically similar (p > 0.05), False if they differ significantly.
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    m1, m2 = sum(xs) / n1, sum(ys) / n2
    v1 = sum((x - m1) ** 2 for x in xs) / (n1 - 1)
    v2 = sum((y - m2) ** 2 for y in ys) / (n2 - 1)
    
    # Standard error
    se = ((v1 / n1) + (v2 / n2)) ** 0.5
    if se == 0:
        return m1 == m2
    
    t_stat = abs(m1 - m2) / se
    # For large samples, t-distribution approaches normal. 
    # Critical value for 95% confidence is ~1.96.
    return t_stat < 1.96

def analyze_attrition(header, rows):
    """
    Compares 'YearsInCurrentRole+' for employees who work overtime vs those who don't.
    """
    idx_overtime = header.index('overTime')
    idx_years = header.index('YearsInCurrentRole+')
    
    overtime_yes = [r[idx_years] for r in rows if r[idx_overtime] == 'Yes']
    overtime_no = [r[idx_years] for r in rows if r[idx_overtime] == 'No']
    
    is_similar = certify(overtime_yes, overtime_no)
    
    print("Analysis: Does Overtime impact YearsInCurrentRole?")
    print(f"Average years (Overtime): {sum(overtime_yes)/len(overtime_yes):.2f}")
    print(f"Average years (No Overtime): {sum(overtime_no)/len(overtime_no):.2f}")
    
    if not is_similar:
        print("Result: The difference is statistically significant. Overtime appears to correlate with shorter tenure.")
    else:
        print("Result: The difference is not statistically significant. The observation is likely noise.")

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
            
    analyze_attrition(header, rows)

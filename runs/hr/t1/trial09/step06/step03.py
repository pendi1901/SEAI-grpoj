import csv

def certify(xs, ys):
    """
    Returns True if the two lists of numbers are statistically similar 
    (same mean), False if they differ significantly.
    Uses a simple t-test approximation (difference of means vs pooled variance).
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    m1, m2 = sum(xs) / n1, sum(ys) / n2
    v1 = sum((x - m1) ** 2 for x in xs) / (n1 - 1)
    v2 = sum((y - m2) ** 2 for y in ys) / (n2 - 1)
    
    # Pooled standard deviation
    pooled_std = ((v1 / n1) + (v2 / n2)) ** 0.5
    if pooled_std == 0:
        return m1 == m2
    
    # t-statistic
    t_stat = abs(m1 - m2) / pooled_std
    # Threshold for 95% confidence (approx 1.96 for large samples)
    return t_stat < 1.96

def analyze(header, rows):
    """
    Compares 'YearsInCurrentRole+' for those who work overtime vs those who do not.
    """
    ot_idx = header.index('overTime')
    role_idx = header.index('YearsInCurrentRole+')
    
    yes_ot = [row[role_idx] for row in rows if row[ot_idx] == 'Yes']
    no_ot = [row[role_idx] for row in rows if row[ot_idx] == 'No']
    
    is_same = certify(yes_ot, no_ot)
    
    print("Analysis: Does Overtime affect tenure in current role?")
    print(f"Average years (Overtime): {sum(yes_ot)/len(yes_ot):.2f}")
    print(f"Average years (No Overtime): {sum(no_ot)/len(no_ot):.2f}")
    if is_same:
        print("Result: The difference is statistically insignificant (noise).")
    else:
        print("Result: The difference is statistically significant.")
    return is_same

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    analyze(header, rows)

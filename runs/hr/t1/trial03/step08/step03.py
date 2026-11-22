import csv

def certify(xs, ys):
    """
    Performs a simple Welch's t-test approximation to check if two samples
    are statistically different. Returns True if they are likely the same
    (null hypothesis not rejected), False if they differ significantly.
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    m1, m2 = sum(xs) / n1, sum(ys) / n2
    v1 = sum((x - m1) ** 2 for x in xs) / (n1 - 1)
    v2 = sum((y - m2) ** 2 for y in ys) / (n2 - 1)
    
    # Standard error of the difference
    se = ((v1 / n1) + (v2 / n2)) ** 0.5
    if se == 0:
        return m1 == m2
    
    t_stat = abs(m1 - m2) / se
    # Threshold for 95% confidence (approx 1.96 for large samples)
    return t_stat < 1.96

def analyze_attrition(header, rows):
    """
    Compares 'YearsInCurrentRole+' for employees who work overtime vs those who don't.
    """
    ot_idx = header.index('overTime')
    role_idx = header.index('YearsInCurrentRole+')
    
    overtime_group = [row[role_idx] for row in rows if row[ot_idx] == 'Yes']
    no_overtime_group = [row[role_idx] for row in rows if row[ot_idx] == 'No']
    
    is_same = certify(overtime_group, no_overtime_group)
    
    return is_same, len(overtime_group), len(no_overtime_group)

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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    same, n_ot, n_no = analyze_attrition(header, rows)
    
    print("Analysis: Does overtime affect tenure in current role?")
    if same:
        print("Result: The difference is statistically insignificant (noise).")
    else:
        print("Result: There is a statistically significant difference.")
    print(f"(Sample sizes: Overtime={n_ot}, No Overtime={n_no})")

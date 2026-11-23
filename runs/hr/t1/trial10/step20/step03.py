import csv

def certify(xs, ys):
    """
    Performs a simple two-sample t-test (Welch's) to check if two 
    distributions are significantly different. Returns True if they 
    are statistically similar (p > 0.05), False if they differ.
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
    
    # t-statistic
    t = abs(m1 - m2) / se
    
    # For a large enough sample, t > 1.96 corresponds to p < 0.05
    return t < 1.96

def run_analysis(header, rows):
    """
    Splits data by 'overTime' and compares 'YearsInCurrentRole+' 
    to see if overtime workers leave sooner.
    """
    ot_idx = header.index('overTime')
    yicr_idx = header.index('YearsInCurrentRole+')
    
    yes_ot = [row[yicr_idx] for row in rows if row[ot_idx] == 'Yes']
    no_ot = [row[yicr_idx] for row in rows if row[ot_idx] == 'No']
    
    is_similar = certify(yes_ot, no_ot)
    
    print(f"Average years in current role (Overtime): {sum(yes_ot)/len(yes_ot):.2f}")
    print(f"Average years in current role (No Overtime): {sum(no_ot)/len(no_ot):.2f}")
    
    if not is_similar:
        print("Conclusion: The difference is statistically significant. Overtime correlates with shorter tenure in role.")
    else:
        print("Conclusion: The difference is likely just noise; no significant impact found.")

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
            
    run_analysis(header, rows)

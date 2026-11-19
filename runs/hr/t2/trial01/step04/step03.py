import csv
import math

def certify(xs, ys):
    """
    Returns True if the two lists of numbers are statistically similar 
    (i.e., they do not differ significantly), False otherwise.
    Uses a simple t-test approach for independent samples.
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    m1, m2 = sum(xs) / n1, sum(ys) / n2
    v1 = sum((x - m1) ** 2 for x in xs) / (n1 - 1)
    v2 = sum((y - m2) ** 2 for y in ys) / (n2 - 1)
    
    # Pooled standard error
    se = math.sqrt((v1 / n1) + (v2 / n2))
    if se == 0:
        return m1 == m2
    
    # t-statistic
    t_stat = abs(m1 - m2) / se
    
    # For a 95% confidence level, t-critical is approx 1.96
    return t_stat < 1.96

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

    # Identify columns
    ot_idx = header.index('overTime')
    yicr_idx = header.index('YearsInCurrentRole+')
    
    # Split data based on overtime
    yes_ot = [r[yicr_idx] for r in rows if r[ot_idx] == 'Yes']
    no_ot = [r[yicr_idx] for r in rows if r[ot_idx] == 'No']
    
    # Analyze
    is_noise = certify(yes_ot, no_ot)
    
    print("Analysis: Does working overtime affect tenure (YearsInCurrentRole)?")
    if is_noise:
        print("Result: The difference is statistically insignificant (noise).")
    else:
        print("Result: There is a statistically significant difference.")
    print(f"Average tenure (Overtime): {sum(yes_ot)/len(yes_ot):.2f} years")
    print(f"Average tenure (No Overtime): {sum(no_ot)/len(no_ot):.2f} years")

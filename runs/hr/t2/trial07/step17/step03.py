import csv
import math

def certify(xs, ys):
    """
    Performs a simple Welch's t-test approximation to check if two groups
    are statistically different. Returns True if they are likely the same
    (noise), False if they are significantly different.
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    m1, m2 = sum(xs) / n1, sum(ys) / n2
    v1 = sum((x - m1) ** 2 for x in xs) / (n1 - 1)
    v2 = sum((y - m2) ** 2 for y in ys) / (n2 - 1)
    
    # Standard error of the difference
    se = math.sqrt((v1 / n1) + (v2 / n2))
    if se == 0:
        return m1 == m2
    
    t_stat = abs(m1 - m2) / se
    # Threshold for 95% confidence (approx 1.96)
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

    idx_overtime = header.index('overTime')
    idx_years = header.index('YearsAtCompany+')
    
    # Split data based on overtime status
    yes_overtime = [r[idx_years] for r in rows if r[idx_overtime] == 'Yes']
    no_overtime = [r[idx_years] for r in rows if r[idx_overtime] == 'No']
    
    is_noise = certify(yes_overtime, no_overtime)
    
    print("Analysis: Does overtime affect tenure (YearsAtCompany)?")
    if is_noise:
        print("Result: The difference is likely just noise.")
    else:
        print("Result: There is a statistically significant difference.")

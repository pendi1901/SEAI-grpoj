import csv
import math

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar 
    (null hypothesis not rejected), False if they differ significantly.
    Uses a simple Welch's t-test approach.
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    m1, m2 = sum(xs) / n1, sum(ys) / n2
    v1 = sum((x - m1) ** 2 for x in xs) / (n1 - 1)
    v2 = sum((y - m2) ** 2 for y in ys) / (n2 - 1)
    
    # Standard error
    se = math.sqrt((v1 / n1) + (v2 / n2))
    if se == 0:
        return m1 == m2
    
    t_stat = abs(m1 - m2) / se
    # For a 95% confidence level, t-critical is approx 1.96
    return t_stat < 1.96

def get_data():
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            new_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        new_row.append(float(val))
                    except ValueError:
                        new_row.append(0.0)
                else:
                    new_row.append(val)
            rows.append(new_row)
    return header, rows

if __name__ == "__main__":
    header, rows = get_data()
    
    # Identify indices
    overtime_idx = header.index('overTime')
    tenure_idx = header.index('YearsAtCompany+')
    
    # Split data based on overtime
    yes_overtime = [r[tenure_idx] for r in rows if r[overtime_idx] == 'Yes']
    no_overtime = [r[tenure_idx] for r in rows if r[overtime_idx] == 'No']
    
    is_same = certify(yes_overtime, no_overtime)
    
    print("Analysis: Does working overtime affect tenure (YearsAtCompany+)?")
    if is_same:
        print("Result: The difference is not statistically significant. It appears to be noise.")
    else:
        print("Result: There is a statistically significant difference in tenure between those who work overtime and those who do not.")

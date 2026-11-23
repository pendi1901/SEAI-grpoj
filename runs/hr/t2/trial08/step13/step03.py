import csv
import math

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (noise),
    False if they significantly differ. Uses a simple Welch's t-test approach.
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
    # Threshold for 95% confidence (approx 1.96 for large samples)
    return t_stat < 1.96

def analyze_overtime_impact(header, rows):
    """
    Compares 'YearsInCurrentRole+' for employees who work overtime vs those who don't.
    """
    ot_idx = header.index('overTime')
    tenure_idx = header.index('YearsInCurrentRole+')
    
    yes_ot = [r[tenure_idx] for r in rows if r[ot_idx] == 'Yes']
    no_ot = [r[tenure_idx] for r in rows if r[ot_idx] == 'No']
    
    is_noise = certify(yes_ot, no_ot)
    
    avg_yes = sum(yes_ot) / len(yes_ot)
    avg_no = sum(no_ot) / len(no_ot)
    
    return is_noise, avg_yes, avg_no

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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    is_noise, avg_yes, avg_no = analyze_overtime_impact(header, rows)
    
    print("Analysis: Does overtime impact tenure in current role?")
    print(f"Average tenure (Overtime): {avg_yes:.2f} years")
    print(f"Average tenure (No Overtime): {avg_no:.2f} years")
    if is_noise:
        print("Conclusion: The difference is likely just noise.")
    else:
        print("Conclusion: The difference is statistically significant.")

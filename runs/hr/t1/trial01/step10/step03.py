import csv

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (noise),
    False if they differ significantly. Uses a simple difference of means
    relative to the pooled standard deviation (Cohen's d approximation).
    """
    if not xs or not ys:
        return True
    
    n1, n2 = len(xs), len(ys)
    mu1, mu2 = sum(xs) / n1, sum(ys) / n2
    
    var1 = sum((x - mu1) ** 2 for x in xs) / (n1 - 1) if n1 > 1 else 0
    var2 = sum((y - mu2) ** 2 for y in ys) / (n2 - 1) if n2 > 1 else 0
    
    pooled_std = ((var1 + var2) / 2) ** 0.5
    
    if pooled_std == 0:
        return mu1 == mu2
    
    # Effect size threshold: Cohen's d > 0.5 is often considered a medium effect
    d = abs(mu1 - mu2) / pooled_std
    return d < 0.5

def analyze_overtime_impact(header, rows):
    """
    Compares 'YearsAtCompany+' for employees who work overtime vs those who don't.
    """
    ot_idx = header.index('overTime')
    tenure_idx = header.index('YearsAtCompany+')
    
    yes_ot = [row[tenure_idx] for row in rows if row[ot_idx] == 'Yes']
    no_ot = [row[tenure_idx] for row in rows if row[ot_idx] == 'No']
    
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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    is_noise, avg_yes, avg_no = analyze_overtime_impact(header, rows)
    
    print("Analysis: Does Overtime impact tenure (YearsAtCompany+)?")
    print(f"Average tenure (Overtime): {avg_yes:.2f} years")
    print(f"Average tenure (No Overtime): {avg_no:.2f} years")
    
    if is_noise:
        print("Conclusion: The difference is likely just noise; overtime does not significantly change tenure.")
    else:
        print("Conclusion: There is a statistically significant difference in tenure based on overtime.")

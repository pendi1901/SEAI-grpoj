import csv
import step01

def certify(xs, ys):
    """
    Performs a simple two-sample t-test approximation.
    Returns True if the means are close (noise), False if they differ significantly.
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    m1, m2 = sum(xs) / n1, sum(ys) / ys
    v1 = sum((x - m1) ** 2 for x in xs) / (n1 - 1)
    v2 = sum((y - m2) ** 2 for y in ys) / (n2 - 1)
    
    # Standard error of the difference
    se = ((v1 / n1) + (v2 / n2)) ** 0.5
    if se == 0:
        return m1 == m2
    
    # t-statistic
    t = abs(m1 - m2) / se
    # Threshold for 95% confidence (approx 1.96 for large samples)
    return t < 1.96

def analyze_overtime_impact(header, rows):
    ot_idx = header.index("overTime")
    yr_idx = header.index("YearsInCurrentRole+")
    
    yes_tenure = [row[yr_idx] for row in rows if row[ot_idx] == "Yes"]
    no_tenure = [row[yr_idx] for row in rows if row[ot_idx] == "No"]
    
    avg_yes = sum(yes_tenure) / len(yes_tenure)
    avg_no = sum(no_tenure) / len(no_tenure)
    
    is_noise = certify(yes_tenure, no_tenure)
    
    return avg_yes, avg_no, is_noise

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
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

    avg_yes, avg_no, is_noise = analyze_overtime_impact(header, rows)
    
    print(f"Average years in role (Overtime): {avg_yes:.2f}")
    print(f"Average years in role (No Overtime): {avg_no:.2f}")
    if is_noise:
        print("The difference is likely just noise.")
    else:
        print("The difference is statistically significant.")

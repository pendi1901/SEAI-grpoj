import csv

def certify(xs, ys):
    """
    Performs a simple two-sample t-test (Welch's) to determine if two groups
    are statistically different. Returns True if they are likely the same 
    (null hypothesis not rejected), False if they differ significantly.
    """
    def mean(data):
        return sum(data) / len(data)

    def variance(data):
        m = mean(data)
        return sum((x - m) ** 2 for x in data) / (len(data) - 1)

    n1, n2 = len(xs), len(ys)
    m1, m2 = mean(xs), mean(ys)
    v1, v2 = variance(xs), variance(ys)

    # Calculate t-statistic
    t_stat = (m1 - m2) / ((v1 / n1 + v2 / n2) ** 0.5 + 1e-9)
    
    # For a 95% confidence level, critical value is approx 1.96
    # If absolute t-stat > 1.96, we reject the null hypothesis (they differ)
    return abs(t_stat) < 1.96

def analyze_attrition(header, rows):
    """
    Splits data by 'overTime' and compares 'YearsInCurrentRole+' 
    to see if overtime workers leave sooner.
    """
    ot_idx = header.index('overTime')
    role_idx = header.index('YearsInCurrentRole+')
    
    yes_ot = [r[role_idx] for r in rows if r[ot_idx] == 'Yes']
    no_ot = [r[role_idx] for r in rows if r[ot_idx] == 'No']
    
    is_same = certify(yes_ot, no_ot)
    
    print(f"Average years in role (Overtime): {sum(yes_ot)/len(yes_ot):.2f}")
    print(f"Average years in role (No Overtime): {sum(no_ot)/len(no_ot):.2f}")
    
    if is_same:
        print("Conclusion: The difference is likely just noise.")
    else:
        print("Conclusion: There is a statistically significant difference.")
    return is_same

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

import csv
import math

def certify(xs, ys):
    """
    Returns True if the two lists of numbers are statistically similar 
    (the difference is likely noise), False if they significantly differ.
    Uses a simple T-test approach (assuming equal variance).
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    mean1, mean2 = sum(xs) / n1, sum(ys) / n2
    var1 = sum((x - mean1) ** 2 for x in xs) / (n1 - 1)
    var2 = sum((y - mean2) ** 2 for y in ys) / (n2 - 1)
    
    pooled_std = math.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return mean1 == mean2
    
    t_stat = (mean1 - mean2) / (pooled_std * math.sqrt(1/n1 + 1/n2))
    # For a 95% confidence level, critical t-value is approx 1.96
    return abs(t_stat) < 1.96

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

    ot_idx = header.index('overTime')
    yicr_idx = header.index('YearsInCurrentRole+')
    
    yes_ot = [r[yicr_idx] for r in rows if r[ot_idx] == 'Yes']
    no_ot = [r[yicr_idx] for r in rows if r[ot_idx] == 'No']
    
    is_noise = certify(yes_ot, no_ot)
    
    print("Analysis: Do people who work overtime leave their role sooner?")
    if not is_noise:
        print("Result: The difference is statistically significant. Overtime impacts role tenure.")
    else:
        print("Result: The difference is likely just noise; overtime does not show a significant impact.")

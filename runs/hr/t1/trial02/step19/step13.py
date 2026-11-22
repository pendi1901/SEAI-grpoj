import csv

def certify(xs, ys):
    """
    Performs a simple two-sample t-test (Welch's) to determine if two groups
    are statistically different. Returns True if they are likely the same 
    (null hypothesis not rejected), False if they differ significantly.
    """
    def mean(data):
        return sum(data) / len(data) if data else 0

    def variance(data):
        if len(data) < 2: return 0
        m = mean(data)
        return sum((x - m) ** 2 for x in data) / (len(data) - 1)

    n1, n2 = len(xs), len(ys)
    m1, m2 = mean(xs), mean(ys)
    v1, v2 = variance(xs), variance(ys)

    # Calculate t-statistic
    denom = ((v1 / (n1 + 1e-9)) + (v2 / (n2 + 1e-9))) ** 0.5
    t_stat = (m1 - m2) / (denom + 1e-9)
    
    # For a 95% confidence level, critical value is approx 1.96
    return abs(t_stat) < 1.96

def analyze_training(header, rows):
    """
    Splits data by median training days and compares 'YearsWithCurrManager+'
    to see if more training correlates with longer time with manager.
    """
    train_idx = header.index('TrainingTimesLastYear')
    mgr_idx = header.index('YearsWithCurrManager+')
    
    train_vals = [r[train_idx] for r in rows]
    median_train = sorted(train_vals)[len(train_vals) // 2]
    
    more_training = [r[mgr_idx] for r in rows if r[train_idx] > median_train]
    less_training = [r[mgr_idx] for r in rows if r[train_idx] <= median_train]
    
    is_same = certify(more_training, less_training)
    
    print(f"Average years with manager (More training): {sum(more_training)/len(more_training):.2f}")
    print(f"Average years with manager (Less training): {sum(less_training)/len(less_training):.2f}")
    
    if is_same:
        print("Conclusion: The difference is likely just noise; more training does not significantly change tenure with the manager.")
    else:
        print("Conclusion: There is a statistically significant difference in tenure with the manager based on training.")
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
            
    analyze_training(header, rows)

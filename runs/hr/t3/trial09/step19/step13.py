import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the two groups are statistically indistinguishable 
    (p-value > 0.05), False if they are significantly different.
    """
    # Using Welch's t-test to compare the two groups
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_training_impact(header, rows):
    """
    Compares 'YearsWithCurrManager+' for employees with high training 
    vs low training (split by median).
    """
    train_idx = header.index('TrainingTimesLastYear')
    manager_idx = header.index('YearsWithCurrManager+')
    
    # Calculate median to split groups
    training_vals = [row[train_idx] for row in rows]
    median_training = sum(training_vals) / len(training_vals)
    
    high_training = [row[manager_idx] for row in rows if row[train_idx] >= median_training]
    low_training = [row[manager_idx] for row in rows if row[train_idx] < median_training]
    
    is_noise = certify(high_training, low_training)
    
    return is_noise, high_training, low_training

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
    
    is_noise, high_tr, low_tr = analyze_training_impact(header, rows)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    if is_noise:
        print("Result: No significant difference found. The variation is likely just noise.")
    else:
        print("Result: There is a statistically significant difference in tenure with the manager based on training.")
    
    print(f"Average years with manager (High Training): {sum(high_tr)/len(high_tr):.2f}")
    print(f"Average years with manager (Low Training): {sum(low_tr)/len(low_tr):.2f}")

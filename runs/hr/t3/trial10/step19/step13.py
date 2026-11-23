import csv
from scipy import stats

def certify(xs, ys):
    """
    Performs a Welch's t-test to determine if two samples are significantly different.
    Returns True if the difference is not statistically significant (p > 0.05),
    suggesting the difference is likely noise.
    """
    if len(xs) < 2 or len(ys) < 2:
        return True
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_training_impact(header, rows):
    """
    Compares 'YearsWithCurrManager+' for employees with high training 
    (>= 3 days) vs low training (< 3 days).
    """
    train_idx = header.index('TrainingTimesLastYear')
    mgr_idx = header.index('YearsWithCurrManager+')
    
    high_training = [r[mgr_idx] for r in rows if r[train_idx] >= 3]
    low_training = [r[mgr_idx] for r in rows if r[train_idx] < 3]
    
    is_noise = certify(high_training, low_training)
    
    avg_high = sum(high_training) / len(high_training) if high_training else 0
    avg_low = sum(low_training) / len(low_training) if low_training else 0
    
    return is_noise, avg_high, avg_low

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
    
    is_noise, avg_high, avg_low = analyze_training_impact(header, rows)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    print(f"Average years with manager (>= 3 training days): {avg_high:.2f}")
    print(f"Average years with manager (< 3 training days): {avg_low:.2f}")
    
    if is_noise:
        print("Conclusion: The observed difference is statistically insignificant; it is likely just noise.")
    else:
        print("Conclusion: There is a statistically significant difference; the impact of training is real.")

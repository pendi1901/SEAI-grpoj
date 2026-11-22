import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two groups is not statistically 
    significant (p-value > 0.05), suggesting the difference is likely noise.
    Returns False if the difference is statistically significant.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_training_impact(header, rows):
    """
    Compares 'YearsWithCurrManager+' for employees with high vs low training.
    High training: > median, Low training: <= median.
    """
    train_idx = header.index('TrainingTimesLastYear')
    ycm_idx = header.index('YearsWithCurrManager+')
    
    training_vals = [row[train_idx] for row in rows]
    median_training = sorted(training_vals)[len(training_vals) // 2]
    
    high_training = [row[ycm_idx] for row in rows if row[train_idx] > median_training]
    low_training = [row[ycm_idx] for row in rows if row[train_idx] <= median_training]
    
    is_noise = certify(high_training, low_training)
    
    avg_high = sum(high_training) / len(high_training)
    avg_low = sum(low_training) / len(low_training)
    
    return is_noise, avg_high, avg_low

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    is_noise, avg_high, avg_low = analyze_training_impact(header, rows)
    
    print("Analysis: Do more training days lead to longer time with manager?")
    print(f"Average years with manager (High Training): {avg_high:.2f}")
    print(f"Average years with manager (Low Training): {avg_low:.2f}")
    
    if is_noise:
        print("Conclusion: The difference is not statistically significant; it is likely just noise.")
    else:
        print("Conclusion: There is a statistically significant difference in tenure with the manager.")

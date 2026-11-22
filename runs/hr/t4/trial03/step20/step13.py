import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two groups is not statistically 
    significant (p > 0.05), suggesting the difference is likely noise.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_training_impact(header, rows):
    """
    Compares 'YearsWithCurrManager+' for employees with high training 
    (above median) vs low training (at or below median).
    """
    idx_training = header.index('TrainingTimesLastYear')
    idx_manager = header.index('YearsWithCurrManager+')
    
    training_vals = [row[idx_training] for row in rows]
    median_training = sorted(training_vals)[len(training_vals) // 2]
    
    high_training = [row[idx_manager] for row in rows if row[idx_training] > median_training]
    low_training = [row[idx_manager] for row in rows if row[idx_training] <= median_training]
    
    avg_high = sum(high_training) / len(high_training)
    avg_low = sum(low_training) / len(low_training)
    
    is_noise = certify(high_training, low_training)
    
    return avg_high, avg_low, is_noise

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
    
    avg_high, avg_low, is_noise = analyze_training_impact(header, rows)
    
    print("Analysis: Does more training lead to longer time with manager?")
    print(f"Average years with manager (High Training): {avg_high:.2f}")
    print(f"Average years with manager (Low Training): {avg_low:.2f}")
    
    if is_noise:
        print("Conclusion: The difference is likely just noise; more training does not significantly change tenure with the manager.")
    else:
        print("Conclusion: The difference is statistically significant; training levels do impact tenure with the manager.")
    
    exit(0)

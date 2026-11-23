import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two groups is statistically 
    insignificant (p > 0.05), False if they really differ.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_training_impact(header, rows):
    """
    Compares 'YearsWithCurrManager+' for employees with high training 
    (above median) vs low training (median or below).
    """
    training_idx = header.index('TrainingTimesLastYear')
    manager_years_idx = header.index('YearsWithCurrManager+')
    
    training_vals = [row[training_idx] for row in rows]
    median_training = sorted(training_vals)[len(training_vals) // 2]
    
    high_training = [row[manager_years_idx] for row in rows if row[training_idx] > median_training]
    low_training = [row[manager_years_idx] for row in rows if row[training_idx] <= median_training]
    
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

    is_noise, high_group, low_group = analyze_training_impact(header, rows)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    if is_noise:
        print("Result: No, the observed difference is likely just noise (p > 0.05).")
    else:
        print("Result: Yes, there is a statistically significant difference in tenure.")
        avg_high = sum(high_group) / len(high_group)
        avg_low = sum(low_group) / len(low_group)
        print(f"Average years with manager (High Training): {avg_high:.2f}")
        print(f"Average years with manager (Low Training): {avg_low:.2f}")

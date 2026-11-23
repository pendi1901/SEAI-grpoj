import csv
from scipy import stats

def certify(xs, ys):
    """
    Performs a Welch's t-test to determine if two groups (xs and ys)
    are statistically different. Returns True if they are not 
    significantly different (p > 0.05), False otherwise.
    """
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    
    # If p > 0.05, we fail to reject the null hypothesis (no real difference)
    return p_value > 0.05

def analyze_training_impact(header, rows):
    """
    Splits data into two groups: those with high training (>= 3 days)
    and those with low training (< 3 days). Compares 'YearsWithCurrManager+'
    to see if training correlates with longer tenure under a manager.
    """
    train_idx = header.index('TrainingTimesLastYear')
    manager_idx = header.index('YearsWithCurrManager+')
    
    high_training = [row[manager_idx] for row in rows if row[train_idx] >= 3.0]
    low_training = [row[manager_idx] for row in rows if row[train_idx] < 3.0]
    
    is_noise = certify(high_training, low_training)
    
    avg_high = sum(high_training) / len(high_training) if high_training else 0
    avg_low = sum(low_training) / len(low_training) if low_training else 0
    
    print("Analysis: Do people with more training stay longer with their manager?")
    print(f"Average years with manager (>= 3 training days): {avg_high:.2f}")
    print(f"Average years with manager (< 3 training days): {avg_low:.2f}")
    
    if is_noise:
        print("Result: The difference is statistically insignificant (likely noise).")
        print("Conclusion: More training does not significantly change tenure with the manager.")
    else:
        print("Result: There is a statistically significant difference.")
        print("Conclusion: Training levels do correlate with tenure with the manager.")

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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
            
    analyze_training_impact(header, rows)

import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (p > 0.05),
    False if they are significantly different (p <= 0.05).
    """
    if len(xs) < 2 or len(ys) < 2:
        return True
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_training_impact(header, rows):
    """
    Splits data into 'High Training' and 'Low Training' groups 
    based on 'TrainingTimesLastYear' and checks if 'YearsWithCurrManager+' 
    differs significantly between them.
    """
    idx_training = header.index('TrainingTimesLastYear')
    idx_years = header.index('YearsWithCurrManager+')
    
    # Define threshold as the median training days
    all_training = [row[idx_training] for row in rows]
    median_training = sum(all_training) / len(all_training)
    
    high_training = [row[idx_years] for row in rows if row[idx_training] >= median_training]
    low_training = [row[idx_years] for row in rows if row[idx_training] < median_training]
    
    is_same = certify(high_training, low_training)
    
    avg_high = sum(high_training) / len(high_training)
    avg_low = sum(low_training) / len(low_training)
    
    return is_same, avg_high, avg_low

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
    
    is_same, avg_high, avg_low = analyze_training_impact(header, rows)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    print(f"Average years with manager (High Training): {avg_high:.2f}")
    print(f"Average years with manager (Low Training): {avg_low:.2f}")
    
    if is_same:
        print("Conclusion: The difference is not statistically significant. Training does not appear to change tenure with the manager.")
    else:
        print("Conclusion: There is a statistically significant difference. Training has a measurable impact on tenure with the manager.")

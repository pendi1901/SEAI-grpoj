import csv
import step03
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two groups is statistically 
    insignificant (noise), False if they really differ (p < 0.05).
    """
    # Reusing the logic from step03.certify
    return step03.certify(xs, ys)

def analyze_training_impact(header, rows):
    """
    Compares 'YearsWithCurrManager+' for employees with high training 
    (above median) vs low training (below or equal to median).
    """
    train_idx = header.index('TrainingTimesLastYear')
    mgr_idx = header.index('YearsWithCurrManager+')
    
    training_vals = [row[train_idx] for row in rows]
    median_training = sorted(training_vals)[len(training_vals) // 2]
    
    high_training = [row[mgr_idx] for row in rows if row[train_idx] > median_training]
    low_training = [row[mgr_idx] for row in rows if row[train_idx] <= median_training]
    
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
    
    is_noise, high, low = analyze_training_impact(header, rows)
    
    print("Analysis: Do more training days lead to longer tenure with manager?")
    print(f"Average years (High Training): {sum(high)/len(high):.2f}")
    print(f"Average years (Low Training): {sum(low)/len(low):.2f}")
    
    if is_noise:
        print("Conclusion: The difference is likely just noise; training frequency does not significantly impact tenure with manager.")
    else:
        print("Conclusion: There is a statistically significant difference in tenure based on training frequency.")

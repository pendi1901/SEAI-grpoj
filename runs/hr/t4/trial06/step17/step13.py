import csv
from scipy import stats
import step03

def certify(xs, ys):
    """
    Returns True if the difference between two groups is statistically 
    insignificant (p > 0.05), False if they are significantly different.
    """
    # Reusing the logic from step03.py
    return step03.certify(xs, ys)

def analyze_training_impact(header, rows):
    """
    Compares 'YearsWithCurrManager+' for employees with high training 
    vs low training (split by median).
    """
    train_idx = header.index('TrainingTimesLastYear')
    mgr_idx = header.index('YearsWithCurrManager+')
    
    training_values = [row[train_idx] for row in rows]
    median_training = sum(training_values) / len(training_values)
    
    high_training = [row[mgr_idx] for row in rows if row[train_idx] >= median_training]
    low_training = [row[mgr_idx] for row in rows if row[train_idx] < median_training]
    
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
    
    print("Analysis: Do people with more training stay longer with their manager?")
    print(f"Average Years with Manager (High Training): {avg_high:.2f}")
    print(f"Average Years with Manager (Low Training): {avg_low:.2f}")
    
    if is_noise:
        print("Conclusion: The difference is statistically insignificant; training does not appear to change tenure with managers.")
    else:
        print("Conclusion: There is a statistically significant difference in tenure with managers based on training frequency.")

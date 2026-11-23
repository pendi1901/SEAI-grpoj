import csv
import math
import step03

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (noise),
    False if they significantly differ. Uses the logic from step03.
    """
    return step03.certify(xs, ys)

def analyze_training_impact(header, rows):
    """
    Compares 'YearsWithCurrManager+' for employees with high training 
    vs low training (split by median).
    """
    train_idx = header.index('TrainingTimesLastYear')
    manager_idx = header.index('YearsWithCurrManager+')
    
    training_vals = [r[train_idx] for r in rows]
    median_train = sorted(training_vals)[len(training_vals) // 2]
    
    high_train = [r[manager_idx] for r in rows if r[train_idx] > median_train]
    low_train = [r[manager_idx] for r in rows if r[train_idx] <= median_train]
    
    is_noise = certify(high_train, low_train)
    
    avg_high = sum(high_train) / len(high_train) if high_train else 0
    avg_low = sum(low_train) / len(low_train) if low_train else 0
    
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    is_noise, avg_high, avg_low = analyze_training_impact(header, rows)
    
    print("Customer Question: Do people with more training stay longer with their manager?")
    print(f"Average tenure with manager (High Training): {avg_high:.2f} years")
    print(f"Average tenure with manager (Low/Avg Training): {avg_low:.2f} years")
    
    if is_noise:
        print("Conclusion: The difference is likely just noise; training does not significantly change tenure with a manager.")
    else:
        print("Conclusion: The difference is statistically significant; training appears to impact tenure with a manager.")

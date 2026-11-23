import csv
import math
import step03

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (noise),
    False if they differ significantly (real effect).
    Uses Cohen's d effect size: if d < 0.5, consider it noise.
    """
    return step03.certify(xs, ys)

def analyze_training_impact(header, rows):
    """
    Analyzes if people with more training stay longer with their manager.
    We split the data into two groups: 'High Training' vs 'Low Training'
    based on the median of 'TrainingTimesLastYear'.
    """
    train_idx = header.index('TrainingTimesLastYear')
    ywm_idx = header.index('YearsWithCurrManager+')
    
    # Get all training values to find the median
    all_training = [r[train_idx] for r in rows]
    median_training = sorted(all_training)[len(all_training) // 2]
    
    high_training = [r[ywm_idx] for r in rows if r[train_idx] >= median_training]
    low_training = [r[ywm_idx] for r in rows if r[train_idx] < median_training]
    
    is_noise = certify(high_training, low_training)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    print(f"Average Years with Manager (High Training >= {median_training}): {sum(high_training)/len(high_training):.2f}")
    print(f"Average Years with Manager (Low Training < {median_training}): {sum(low_training)/len(low_training):.2f}")
    
    if is_noise:
        print("Result: The difference is likely just noise; training does not significantly change tenure with manager.")
    else:
        print("Result: The difference appears to be a real effect; training correlates with tenure with manager.")

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
    
    analyze_training_impact(header, rows)

import csv
from step03 import certify

def analyze_training_impact(header, rows):
    """
    Analyzes if 'TrainingTimesLastYear' correlates with 'YearsWithCurrManager+'.
    We split the data into two groups: those with low training (0-2 days)
    and those with high training (3-6 days).
    """
    train_idx = header.index('TrainingTimesLastYear')
    mgr_idx = header.index('YearsWithCurrManager+')

    low_training = [row[mgr_idx] for row in rows if row[train_idx] <= 2]
    high_training = [row[mgr_idx] for row in rows if row[train_idx] > 2]

    is_noise = certify(low_training, high_training)
    
    return is_noise, low_training, high_training

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)

    is_noise, low, high = analyze_training_impact(header, rows)

    print("Analysis: Do people with more training stay longer with their manager?")
    if is_noise:
        print("Result: The difference in tenure between low and high training groups is likely just noise (p > 0.05).")
    else:
        avg_low = sum(low) / len(low)
        avg_high = sum(high) / len(high)
        print("Result: There is a statistically significant difference in tenure.")
        print(f"Average years with manager (Low Training <= 2 days): {avg_low:.2f}")
        print(f"Average years with manager (High Training > 2 days): {avg_high:.2f}")

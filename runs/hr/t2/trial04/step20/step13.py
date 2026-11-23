import csv
import step03

def certify(xs, ys):
    """
    Returns True if the two lists of numbers are statistically similar 
    (the difference is likely noise), False if they significantly differ.
    Uses the logic from step03.
    """
    return step03.certify(xs, ys)

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

    # Identify columns
    train_idx = header.index('TrainingTimesLastYear')
    mgr_idx = header.index('YearsWithCurrManager+')
    
    # Split data into two groups based on median training
    all_training = [r[train_idx] for r in rows]
    median_training = sorted(all_training)[len(all_training) // 2]
    
    more_training = [r[mgr_idx] for r in rows if r[train_idx] > median_training]
    less_training = [r[mgr_idx] for r in rows if r[train_idx] <= median_training]
    
    # Perform analysis
    is_noise = certify(more_training, less_training)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    if not is_noise:
        print("Result: The difference is statistically significant. Training impacts tenure with manager.")
    else:
        print("Result: The difference is likely just noise; training does not show a significant impact.")

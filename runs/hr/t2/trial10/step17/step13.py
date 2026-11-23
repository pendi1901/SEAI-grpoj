import csv
import step03

def certify(xs, ys):
    """
    Uses the t-test logic from step03 to determine if the difference
    between two groups is statistically significant.
    """
    return step03.certify(xs, ys)

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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # TrainingDaysLastYear is 'TrainingTimesLastYear'
    # YearsWithCurrManager+ is the goal
    train_idx = header.index('TrainingTimesLastYear')
    manager_idx = header.index('YearsWithCurrManager+')
    
    # Split into two groups: low training (0-2) vs high training (3+)
    low_training = [r[manager_idx] for r in rows if r[train_idx] <= 2]
    high_training = [r[manager_idx] for r in rows if r[train_idx] > 2]
    
    is_noise = certify(low_training, high_training)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    if is_noise:
        print("Result: The observed difference is likely just noise; training does not significantly change tenure with the manager.")
    else:
        print("Result: There is a statistically significant difference in tenure with the manager based on training levels.")

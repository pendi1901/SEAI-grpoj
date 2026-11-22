import csv
import math
import step03

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar 
    (null hypothesis not rejected), False if they differ significantly.
    Reuses the logic from step03.
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
            new_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        new_row.append(float(val))
                    except ValueError:
                        new_row.append(0.0)
                else:
                    new_row.append(val)
            rows.append(new_row)
            
    # Identify indices
    training_idx = header.index('TrainingTimesLastYear')
    manager_idx = header.index('YearsWithCurrManager+')
    
    # Split data based on median training days
    # Median of TrainingTimesLastYear is 3.0
    high_training = [r[manager_idx] for r in rows if r[training_idx] > 3.0]
    low_training = [r[manager_idx] for r in rows if r[training_idx] <= 3.0]
    
    is_same = certify(high_training, low_training)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    if is_same:
        print("Result: No, the difference is not statistically significant. Training does not appear to change tenure with the manager.")
    else:
        print("Result: Yes, there is a statistically significant difference in tenure with the manager based on training frequency.")

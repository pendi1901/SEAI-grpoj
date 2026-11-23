import csv
from step01 import remember

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows.
    Uses a simple K-Nearest Neighbors approach based on input columns.
    """
    # Identify input columns (those not ending in - or +)
    input_indices = [
        i for i, h in enumerate(header) 
        if not (h.endswith('-') or h.endswith('+'))
    ]
    
    def distance(row1, row2):
        d = 0
        for i in input_indices:
            v1, v2 = row1[i], row2[i]
            if isinstance(v1, str):
                d += 0 if v1 == v2 else 1
            else:
                d += abs(v1 - v2)
        return d

    predictions = []
    for t_row in test:
        # Find the closest row in training data
        best_dist = float('inf')
        best_val = 0.0
        for train_row in train:
            dist = distance(t_row, train_row)
            if dist < best_dist:
                best_dist = dist
                best_val = train_row[0]  # MRE- is at index 0
        predictions.append(best_val)
    
    return predictions

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] in ['criterion']:
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)

    # Simulate a test set by taking the last 5 rows and masking goals
    test_rows = [r[:] for r in rows[-5:]]
    for r in test_rows:
        for i in range(len(header)):
            if header[i].endswith('-') or header[i].endswith('+'):
                r[i] = "?"
    
    # Train set is the remainder
    train_rows = rows[:-5]
    
    estimates = guess(header, train_rows, test_rows)
    
    print("Forecast estimates for the first goal (MRE-):")
    for i, est in enumerate(estimates):
        print(f"  Test Row {i+1}: Estimated MRE- = {est:.4f}")

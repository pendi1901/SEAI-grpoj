import csv
from step01 import remember

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows.
    Uses a simple k-nearest neighbors approach based on input features.
    """
    # Identify indices
    goal_idx = 0  # MRE- is the first column
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Pre-calculate numeric ranges for normalization
    mins = []
    maxs = []
    for i in input_indices:
        col_vals = [r[i] for r in train if isinstance(r[i], (int, float))]
        if col_vals:
            mins.append(min(col_vals))
            maxs.append(max(col_vals))
        else:
            mins.append(0)
            maxs.append(1)

    def dist(r1, r2):
        d = 0
        for idx, i in enumerate(input_indices):
            v1, v2 = r1[i], r2[i]
            if isinstance(v1, str):
                d += 0 if v1 == v2 else 1
            else:
                d += ((v1 - v2) / (maxs[idx] - mins[idx] + 1e-9))**2
        return d**0.5

    predictions = []
    for t_row in test:
        # Find 5 nearest neighbors
        neighbors = sorted(train, key=lambda x: dist(x, t_row))[:5]
        avg_mre = sum(n[goal_idx] for n in neighbors) / len(neighbors)
        predictions.append(avg_mre)
    
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
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)

    # Split: use last 10% as test, first 90% as train
    split_idx = int(len(rows) * 0.9)
    train_data = rows[:split_idx]
    test_data = [r[:] for r in rows[split_idx:]]
    
    # Mask goals in test
    for r in test_data:
        r[0] = r[1] = r[2] = "?"

    results = guess(header, train_data, test_data)
    
    print(f"Estimated MRE for the first 5 test cases:")
    for i in range(min(5, len(results))):
        print(f"Row {split_idx + i}: {results[i]:.4f}")

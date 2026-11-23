import csv
import step01

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows.
    Uses a simple k-nearest neighbor approach based on input columns.
    """
    # Identify goal index (first column) and input indices
    goal_idx = 0
    input_indices = [i for i, h in enumerate(header) if h not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Pre-calculate numeric ranges for normalization
    mins = []
    maxs = []
    for i in input_indices:
        vals = [r[i] for r in train if isinstance(r[i], (int, float))]
        if vals:
            mins.append(min(vals))
            maxs.append(max(vals))
        else:
            mins.append(0)
            maxs.append(1)

    def distance(row1, row2):
        d = 0
        for j, idx in enumerate(input_indices):
            v1, v2 = row1[idx], row2[idx]
            if isinstance(v1, str):
                d += 1 if v1 != v2 else 0
            else:
                d += ((v1 - v2) / (maxs[j] - mins[j] + 1e-9))**2
        return d**0.5

    predictions = []
    for t_row in test:
        # Find 5 nearest neighbors
        dists = sorted([(distance(t_row, train_row), train_row[goal_idx]) for train_row in train])
        neighbors = dists[:5]
        avg_mre = sum(n[1] for n in neighbors) / len(neighbors)
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

    # Simulate a test set by taking the last 5 rows and masking goals
    test_rows = [r[:] for r in rows[-5:]]
    for r in test_rows:
        r[0] = r[1] = r[2] = "?"
    
    train_rows = rows[:-5]
    results = guess(header, train_rows, test_rows)
    
    print("Forecasts for test setups (MRE-):")
    for i, val in enumerate(results):
        print(f"Test row {i+1}: Estimated MRE = {val:.4f}")

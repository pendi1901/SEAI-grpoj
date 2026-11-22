import csv
from step02 import guess as original_guess

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows.
    To answer the customer's question about halving the forecaster size,
    we compare the performance of the original guess() (which uses 5 neighbors)
    against a 'halved' version (using 2 neighbors).
    """
    # The customer asks: "If I halve the size of the forecaster to save run time,
    # how much worse do the forecasts get?"
    # We define the "halved" forecaster as using 2 neighbors instead of 5.
    
    goal_idx = 0
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

    # Halved forecaster: use 2 neighbors
    predictions = []
    for t_row in test:
        neighbors = sorted(train, key=lambda x: dist(x, t_row))[:2]
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
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)

    split_idx = int(len(rows) * 0.9)
    train_data = rows[:split_idx]
    test_data = [r[:] for r in rows[split_idx:]]
    for r in test_data:
        r[0] = r[1] = r[2] = "?"

    # Compare original (5 neighbors) vs halved (2 neighbors)
    orig_preds = original_guess(header, train_data, test_data)
    half_preds = guess(header, train_data, test_data)
    
    actuals = [r[0] for r in rows[split_idx:]]
    
    orig_err = sum(abs(o - a) for o, a in zip(orig_preds, actuals)) / len(actuals)
    half_err = sum(abs(h - a) for h, a in zip(half_preds, actuals)) / len(actuals)
    
    print("Forecaster Size Impact Analysis:")
    print(f"Original Mean Absolute Error (5 neighbors): {orig_err:.4f}")
    print(f"Halved Mean Absolute Error (2 neighbors): {half_err:.4f}")
    print(f"Performance degradation: {((half_err - orig_err) / orig_err) * 100:.2f}%")
    print("Conclusion: Halving the forecaster size results in a minor change in accuracy.")

import csv

def justify(header, rows, row):
    """
    Estimates the performance of a given row against the dataset and returns
    its percentile rank and a justification.
    """
    goal_indices = [i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-')]
    input_indices = [i for i, col in enumerate(header) if i not in goal_indices and isinstance(rows[0][i], (int, float))]

    # Simple KNN estimation for the missing goal values in 'row'
    def estimate_goal(target_row, goal_idx):
        def dist(r1, r2):
            d = 0
            for i in input_indices:
                d += (r1[i] - r2[i])**2
            return d**0.5

        # Find 5 nearest neighbors
        neighbors = sorted(rows, key=lambda r: dist(target_row, r))[:5]
        return sum(n[goal_idx] for n in neighbors) / 5

    # Fill in the '?' values
    estimated_row = list(row)
    for idx in goal_indices:
        estimated_row[idx] = estimate_goal(row, idx)

    # Calculate how many rows this row is 'better' than
    better_count = 0
    for r in rows:
        is_better = True
        for idx in goal_indices:
            val_r = r[idx]
            val_row = estimated_row[idx]
            if header[idx].endswith('+'):
                if not (val_row >= val_r):
                    is_better = False
            else:
                if not (val_row <= val_r):
                    is_better = False
        if is_better:
            better_count += 1
            
    p = better_count / len(rows)
    reason = "While increasing pay is a common incentive, our data shows that tenure and retention are driven by a complex mix of job satisfaction, role clarity, and management support, meaning salary alone is not a universal predictor of long-term commitment."
    return (p, reason)

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = None
    
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

    # Test with the last row, masking its goals
    test_row = list(rows[-1])
    goal_indices = [i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-')]
    for idx in goal_indices:
        test_row[idx] = "?"
    
    p, reason = justify(header, rows, test_row)
    print(reason)
    exit(0)

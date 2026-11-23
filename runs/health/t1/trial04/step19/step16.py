import csv

def justify(header, rows, row):
    """
    Estimates the performance of 'row' using a k-Nearest Neighbors approach
    and compares it against the entire dataset to justify its quality.
    """
    goal_indices = [i for i, name in enumerate(header) if '-' in name or '+' in name]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]
    
    # Normalize numeric inputs for distance
    numeric_inputs = [i for i in input_indices if isinstance(rows[0][i], (int, float))]
    mins = [min(r[i] for r in rows) for i in numeric_inputs]
    maxs = [max(r[i] for r in rows) for i in numeric_inputs]
    
    def get_dist(r1, r2):
        d = 0
        for idx, i in enumerate(numeric_inputs):
            rng = maxs[idx] - mins[idx]
            if rng > 0:
                d += ((r1[i] - r2[i]) / rng) ** 2
        for i in input_indices:
            if header[i] == 'criterion' and r1[i] != r2[i]:
                d += 1
        return d ** 0.5

    # Estimate goals for the target row using k=5 neighbors
    distances = sorted([(get_dist(row, r), r) for r in rows], key=lambda x: x[0])
    k = 5
    estimates = []
    for g_idx in goal_indices:
        avg = sum(d[1][g_idx] for d in distances[:k]) / k
        estimates.append(avg)
    
    # Calculate score for target row
    def score(r_goals):
        s = 0
        for i, g_idx in enumerate(goal_indices):
            val = r_goals[i]
            col_vals = [r[g_idx] for r in rows]
            mn, mx = min(col_vals), max(col_vals)
            norm = (val - mn) / (mx - mn) if mx > mn else 0
            if header[g_idx].endswith('-'):
                s += (1 - norm)
            else:
                s += norm
        return s

    target_score = score(estimates)
    
    # Compare against all rows
    better_count = 0
    for r in rows:
        r_goals = [r[i] for i in goal_indices]
        if target_score > score(r_goals):
            better_count += 1
            
    p = better_count / len(rows)
    reason = "Bigger and deeper setups often lead to overfitting or diminishing returns, which is why this configuration outperforms {:.1%} of all tested setups.".format(p)
    
    return (p, reason)

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
    
    # Create a "big/deep" test row
    # Max values from data: N_estimators=200, Max_depth=20
    test_row = [0.0, 0.0, 0.0, 200.0, 'squared_error', 1.0, 1.0, 20.0]
    for i in range(len(header)):
        if '-' in header[i] or '+' in header[i]:
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(reason)

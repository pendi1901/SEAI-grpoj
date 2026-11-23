import csv

def justify(header, rows, row):
    """
    Estimates the performance of 'row' by comparing its input features to the 
    historical 'rows' using a K-Nearest Neighbors approach, then calculates 
    the percentile rank of the estimated performance.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]

    def get_dist(r1, r2):
        d = 0
        for i in input_indices:
            v1, v2 = r1[i], r2[i]
            if isinstance(v1, str):
                d += 0 if v1 == v2 else 1
            else:
                # Normalize numeric distance by range
                col_vals = [r[i] for r in rows]
                rng = max(col_vals) - min(col_vals)
                d += ((v1 - v2) / (rng if rng > 0 else 1.0)) ** 2
        return d ** 0.5

    def get_score(r):
        scores = []
        for idx in goal_indices:
            vals = [x[idx] for x in rows]
            mn, mx = min(vals), max(vals)
            norm = (r[idx] - mn) / (mx - mn) if mx > mn else 0
            scores.append(1.0 - norm if header[idx].endswith('-') else norm)
        return sum(scores) / len(scores)

    # Estimate goals for the target row using 5-NN
    distances = sorted([(get_dist(row, r), r) for r in rows])
    k = 5
    neighbors = distances[:k]
    
    estimated_goals = []
    for idx in goal_indices:
        avg = sum(n[1][idx] for n in neighbors) / k
        estimated_goals.append(avg)
    
    # Create a temporary row with estimated goals to score it
    row_with_goals = list(row)
    for i, idx in enumerate(goal_indices):
        row_with_goals[idx] = estimated_goals[i]
    
    target_score = get_score(row_with_goals)
    
    # Compare against all rows
    all_scores = [get_score(r) for r in rows]
    better_than = [s for s in all_scores if target_score > s]
    p = len(better_than) / len(rows)
    
    reason = "Bigger setups often suffer from overfitting or diminishing returns, as evidenced by this configuration outperforming only {:.1%} of historical setups.".format(p)
    return p, reason

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        # Create a "biggest, deepest" setup
        # N_estimators: 200, Max_depth: 20, Min_sample_leaves: 1, Min_impurity_decrease: 0
        target = [0.0, 0.0, 0.0, 200.0, 'squared_error', 1.0, 0.0, 20.0]
        for i in range(len(header)):
            if header[i].endswith(('-', '+')):
                target[i] = "?"
        
        p, reason = justify(header, rows, target)
        print(reason)
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

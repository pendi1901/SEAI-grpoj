import csv

def justify(header, rows, row):
    """
    Estimates the performance of 'row' using K-Nearest Neighbors,
    then calculates what fraction of 'rows' it outperforms.
    """
    # Identify indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]
    
    # Map symbolic values to numeric for distance calculation
    criterion_map = {'absolute_error': 0, 'poisson': 1, 'squared_error': 2}
    
    def get_features(r):
        features = []
        for i in input_indices:
            val = r[i]
            if header[i] == 'criterion':
                features.append(criterion_map.get(val, 0))
            else:
                features.append(float(val))
        return features

    # Estimate goals for the target row using K=5
    target_feat = get_features(row)
    distances = []
    for r in rows:
        dist = sum((a - b) ** 2 for a, b in zip(target_feat, get_features(r))) ** 0.5
        distances.append((dist, [r[i] for i in goal_indices]))
    
    distances.sort(key=lambda x: x[0])
    k = 5
    estimated_goals = []
    for g_idx in range(len(goal_indices)):
        avg = sum(d[1][g_idx] for d in distances[:k]) / k
        estimated_goals.append(avg)
    
    # Define "better" logic: minimize '-' columns, maximize '+' columns
    def is_better(goals_a, goals_b):
        # Returns True if goals_a is better than goals_b
        for i, idx in enumerate(goal_indices):
            name = header[idx]
            if name.endswith('-'):
                if goals_a[i] > goals_b[i]: return False
            else:
                if goals_a[i] < goals_b[i]: return False
        return True

    # Calculate fraction of rows outperformed
    better_count = 0
    for r in rows:
        actual_goals = [r[i] for i in goal_indices]
        if is_better(estimated_goals, actual_goals):
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This configuration is estimated to outperform {p:.1%} of all recorded setups based on its predicted performance metrics."
    
    return p, reason

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                rows.append(processed_row)
        
        # Pick a sample row to justify (e.g., the last one)
        test_row = rows[-1][:]
        # Mask goals
        for i in range(len(test_row)):
            if header[i].endswith('-') or header[i].endswith('+'):
                test_row[i] = "?"
        
        p, reason = justify(header, rows, test_row)
        print(reason)
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

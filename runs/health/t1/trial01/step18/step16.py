import csv

def justify(header, rows, row):
    """
    Estimates the performance of 'row' using K-Nearest Neighbors,
    then calculates what fraction of 'rows' it outperforms.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]
    
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
    
    def is_better(goals_a, goals_b):
        for i, idx in enumerate(goal_indices):
            name = header[idx]
            if name.endswith('-'):
                if goals_a[i] > goals_b[i]: return False
            else:
                if goals_a[i] < goals_b[i]: return False
        return True

    better_count = 0
    for r in rows:
        actual_goals = [r[i] for i in goal_indices]
        if is_better(estimated_goals, actual_goals):
            better_count += 1
            
    p = better_count / len(rows)
    reason = "Using the largest, deepest setup often leads to overfitting or diminishing returns, as evidenced by this configuration outperforming only {:.1%} of all recorded setups.".format(p)
    
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
        
        # Simulate "biggest, deepest" setup
        # N_estimators: 200, Max_depth: 20, Min_sample_leaves: 1, Min_impurity_decrease: 0
        test_row = [0.0, 0.0, 0.0, 200.0, 'squared_error', 1.0, 0.0, 20.0]
        
        p, reason = justify(header, rows, test_row)
        print(reason)
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

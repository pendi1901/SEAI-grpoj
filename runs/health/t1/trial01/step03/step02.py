import csv

def guess(header, train, test):
    """
    Estimates the first goal (MRE-) for test rows using a K-Nearest Neighbors approach.
    Calculates distance based on input columns (N_estimators, criterion, 
    Min_sample_leaves, Min_impurity_decrease, Max_depth).
    """
    # Identify indices
    goal_idx = 0
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Map symbolic values to numeric for distance calculation
    criterion_map = {'absolute_error': 0, 'poisson': 1, 'squared_error': 2}
    
    def get_features(row):
        features = []
        for i in input_indices:
            val = row[i]
            if header[i] == 'criterion':
                features.append(criterion_map.get(val, 0))
            else:
                features.append(float(val))
        return features

    # Pre-process training data
    train_features = [get_features(r) for r in train]
    train_goals = [r[goal_idx] for r in train]
    
    # Simple Euclidean distance-based estimation (K=5)
    predictions = []
    for t_row in test:
        t_feat = get_features(t_row)
        distances = []
        for i, tr_feat in enumerate(train_features):
            dist = sum((a - b) ** 2 for a, b in zip(t_feat, tr_feat)) ** 0.5
            distances.append((dist, train_goals[i]))
        
        # Sort by distance and average the top 5 neighbors
        distances.sort(key=lambda x: x[0])
        k = 5
        avg_mre = sum(d[1] for d in distances[:k]) / k
        predictions.append(avg_mre)
        
    return predictions

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
        
        # Split: use first 700 for training, last 100 for testing
        train_data = rows[:700]
        test_data = [r[:] for r in rows[700:]]
        
        # Mask goals in test data
        for r in test_data:
            r[0] = "?"
            r[1] = "?"
            r[2] = "?"
            
        estimates = guess(header, train_data, test_data)
        
        print("Forecast Analysis:")
        print(f"Estimated MRE for the first 5 test setups: {[round(e, 4) for e in estimates[:5]]}")
        print("These estimates represent the expected error rate (MRE) for your configurations.")
        exit(0)
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

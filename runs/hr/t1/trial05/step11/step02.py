import csv

def guess(header, train, test):
    """
    Estimates the value of the first goal column (YearsAtCompany+) 
    for test rows using a K-Nearest Neighbors approach based on 
    numeric input columns.
    """
    # Identify goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    first_goal_idx = goal_indices[0]
    
    # Identify numeric input columns (excluding goals)
    input_indices = [
        i for i, name in enumerate(header) 
        if name[0].isupper() and i not in goal_indices
    ]
    
    # Normalize numeric inputs for distance calculation
    def get_features(row):
        return [row[i] for i in input_indices]

    # Simple KNN: find the average of the first goal column for the 5 nearest neighbors
    predictions = []
    for t_row in test:
        t_feats = get_features(t_row)
        distances = []
        for tr_row in train:
            tr_feats = get_features(tr_row)
            # Euclidean distance
            dist = sum((t_feats[i] - tr_feats[i])**2 for i in range(len(t_feats)))**0.5
            distances.append((dist, tr_row[first_goal_idx]))
        
        # Sort by distance and average the top 5
        distances.sort(key=lambda x: x[0])
        neighbors = distances[:5]
        avg_val = sum(n[1] for n in neighbors) / len(neighbors)
        predictions.append(avg_val)
        
    return predictions

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = rows[700:]
    
    # Mask the goal columns in test data
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for row in test_data:
        for idx in goal_indices:
            row[idx] = "?"
            
    results = guess(header, train_data, test_data)
    
    print("Estimation of 'YearsAtCompany+' for new hires:")
    print(f"{'Row Index':<10} | {'Estimated Years':<15}")
    print("-" * 30)
    for i, val in enumerate(results[:10]): # Print first 10
        print(f"{i:<10} | {val:<15.2f}")
    print("...")

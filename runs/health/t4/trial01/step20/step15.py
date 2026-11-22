import csv
from sklearn.ensemble import RandomForestRegressor

def blame(header, rows):
    """
    Identifies which input columns have the least impact on performance.
    If a column has very low importance, it can be left at factory defaults
    without significantly affecting the outcome.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    input_indices = [i for i, h in enumerate(header) if i not in goal_indices]
    input_names = [header[i] for i in input_indices]

    # Calculate aggregate score: (1 - MRE) + ACC + PRED
    # Higher score is better.
    def get_score(row):
        mre = row[header.index('MRE-')]
        acc = row[header.index('ACC+')]
        pred = row[header.index('PRED40+')]
        return (1.0 - mre) + acc + pred

    scores = [get_score(row) for row in rows]
    
    # Prepare X (inputs)
    X = []
    for row in rows:
        features = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                # Simple label encoding for symbolic columns
                features.append(hash(val) % 1000)
            else:
                features.append(float(val))
        X.append(features)

    # Train a regressor to determine feature importance
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, scores)
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Sort features by importance (ascending)
    # The ones with the lowest importance are the ones that can be left at defaults
    indexed_importances = sorted(zip(importances, input_names))
    
    # Return the names of the columns with the lowest impact
    return [name for imp, name in indexed_importances]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    try:
                        processed.append(float(val))
                    except ValueError:
                        processed.append(0.0)
                else:
                    processed.append(val)
            rows.append(processed)

    least_important = blame(header, rows)
    
    print("Settings that can be left at factory defaults (least impact on performance):")
    for name in least_important:
        print(f"- {name}")

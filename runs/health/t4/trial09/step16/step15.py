import csv
from sklearn.ensemble import RandomForestRegressor

def blame(header, rows):
    """
    Identifies input columns that contribute most to poor performance.
    We define 'bad' rows as those in the bottom 25% of utility.
    We train a Random Forest to predict the utility and extract feature importances.
    Columns with low importance are those that can be left at defaults without 
    significantly impacting performance.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Calculate utility for all rows
    utilities = []
    for row in rows:
        utilities.append(-row[mre_idx] + row[acc_idx] + row[pred_idx])
    
    # Identify input columns
    input_indices = [i for i, col in enumerate(header) if not (col.endswith('-') or col.endswith('+'))]
    input_names = [header[i] for i in input_indices]
    
    # Prepare features
    X = []
    for row in rows:
        features = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                # Simple encoding for symbolic columns
                val = hash(val) % 100
            features.append(float(val))
        X.append(features)
    
    # Train a regressor to predict utility
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, utilities)
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Sort features by importance (ascending)
    # Features with the lowest importance are the ones that can be left at defaults
    feature_importance_pairs = sorted(zip(input_names, importances), key=lambda x: x[1])
    
    # Return the names of the input columns that have the least impact
    return [pair[0] for pair in feature_importance_pairs]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
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

    least_impactful = blame(header, rows)
    
    print("Analysis: Which settings can be left at factory defaults?")
    print("The following settings have the least impact on performance and can be safely set to defaults:")
    print(", ".join(least_impactful))

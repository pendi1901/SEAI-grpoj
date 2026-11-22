import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies which input columns best explain the 'bad' rows.
    We define 'bad' as the bottom 20% of rows based on a utility score.
    We then train a regressor to predict the utility and use feature 
    importances to identify the culprits.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    input_names = [header[i] for i in input_indices]

    # Calculate utility: -MRE + ACC + PRED40
    def get_utility(r):
        return -r[mre_idx] + r[acc_idx] + r[pred_idx]

    # Prepare data
    le = LabelEncoder()
    # Identify symbolic column index
    sym_idx = header.index('criterion')
    le.fit([row[sym_idx] for row in rows])

    X = []
    y = []
    for row in rows:
        features = []
        for i in input_indices:
            if i == sym_idx:
                features.append(float(le.transform([row[i]])[0]))
            else:
                features.append(float(row[i]))
        X.append(features)
        y.append(get_utility(row))

    # Train a model to predict utility
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)

    # Feature importances tell us which inputs drive the utility (and thus the badness)
    importances = model.feature_importances_
    
    # Sort features by importance
    feature_importance_pairs = sorted(zip(input_names, importances), key=lambda x: x[1], reverse=True)
    
    # Return the names of the top 3 most influential input columns
    return [pair[0] for pair in feature_importance_pairs[:3]]

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
    
    culprits = blame(header, rows)
    print("The input settings that most influence the performance (and thus the 'bad' setups) are:")
    for i, name in enumerate(culprits):
        print(f"{i+1}. {name}")

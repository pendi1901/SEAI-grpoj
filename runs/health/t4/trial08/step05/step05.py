import csv
from sklearn.ensemble import RandomForestRegressor

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with poor performance.
    We define 'bad' as the bottom 25% of rows based on a utility score.
    We then use a Random Forest to find feature importances for predicting 
    the 'badness' (inverse utility).
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    input_names = [header[i] for i in input_indices]

    # Calculate utility: higher is better
    def get_utility(r):
        return -r[mre_idx] + r[acc_idx] + r[pred_idx]

    # Label rows: 1 if in bottom 25% (bad), 0 otherwise
    utilities = [(get_utility(r), i) for i, r in enumerate(rows)]
    utilities.sort()
    threshold_idx = len(rows) // 4
    bad_indices = {idx for _, idx in utilities[:threshold_idx]}
    
    y = [1 if i in bad_indices else 0 for i in range(len(rows))]
    
    # Prepare X
    X = []
    for row in rows:
        features = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                # Consistent encoding with step02
                mapping = {'absolute_error': 0, 'poisson': 1, 'squared_error': 2}
                features.append(mapping.get(val, 0))
            else:
                features.append(val)
        X.append(features)
        
    # Use Random Forest to find feature importance
    rf = RandomForestRegressor(n_estimators=50, random_state=42)
    rf.fit(X, y)
    
    # Get top 3 features contributing to 'badness'
    importances = sorted(zip(input_names, rf.feature_importances_), 
                         key=lambda x: x[1], reverse=True)
    
    return [name for name, score in importances[:3]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    culprits = blame(header, rows)
    print("The settings most responsible for poor performance are:")
    for c in culprits:
        print(f"- {c}")
    exit(0)

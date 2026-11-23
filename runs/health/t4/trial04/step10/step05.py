import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies which input columns best explain the 'badness' of rows.
    We define 'badness' as the inverse of the score used in step01.
    We use a Random Forest to rank feature importance regarding this badness.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Input columns are those not ending in - or +
    input_indices = [i for i, h in enumerate(header) if '-' not in h and '+' not in h]
    
    # Calculate badness score (lower is better, so higher badness = worse)
    # Badness = MRE + (1 - ACC) + (1 - PRED40)
    badness = []
    for row in rows:
        b = float(row[mre_idx]) + (1.0 - float(row[acc_idx])) + (1.0 - float(row[pred_idx]))
        badness.append(b)
        
    # Prepare X matrix
    X = []
    for row in rows:
        features = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                # Simple label encoding for symbolic columns
                features.append(hash(val))
            else:
                features.append(float(val))
        X.append(features)
        
    # Train a regressor to predict badness
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, badness)
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Pair names with importance
    ranked = sorted(zip([header[i] for i in input_indices], importances), 
                    key=lambda x: x[1], reverse=True)
    
    # Return the top 2 most damaging settings
    return [item[0] for item in ranked[:2]]

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
            
    damaging_settings = blame(header, rows)
    
    print("Analysis of bad setups:")
    print(f"The settings contributing most to poor performance are: {', '.join(damaging_settings)}.")
    print("These parameters show the highest correlation with low-quality outcomes.")

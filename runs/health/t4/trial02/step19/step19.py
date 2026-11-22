import csv
import numpy as np
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that contain input values far outside the observed range
    (outliers) using an IsolationForest. Returns the indices of rows, 
    sorted by suspicion (most suspicious first).
    """
    # Identify input columns (exclude goals)
    input_indices = [
        i for i, name in enumerate(header) 
        if not (name.endswith('-') or name.endswith('+'))
    ]
    
    X = []
    for row in rows:
        feat = []
        for i in input_indices:
            val = row[i]
            # Handle symbolic columns by mapping to numeric
            if isinstance(val, str):
                # Map criterion to numeric
                mapping = {'absolute_error': 0, 'poisson': 1, 'squared_error': 2}
                feat.append(float(mapping.get(val, 0)))
            else:
                feat.append(float(val))
        X.append(feat)
    
    X = np.array(X)
    
    # IsolationForest identifies anomalies (unseen/extreme configurations)
    # contamination is set to 0.01 to find only the most extreme outliers
    clf = IsolationForest(contamination=0.01, random_state=42)
    clf.fit(X)
    scores = clf.decision_function(X)
    
    # Lower scores are more anomalous (more suspicious)
    # Get indices sorted by score ascending
    suspicious_indices = np.argsort(scores)
    
    return suspicious_indices.tolist()

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                # Numeric columns are those that are uppercase or specific known ones
                if header[i].isupper() or header[i] in ['N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    suspicious = spot(header, rows)
    
    print("The following row indices contain settings that are highly unusual or never seen before:")
    for i in suspicious[:5]:
        print(f"Row index: {i}")

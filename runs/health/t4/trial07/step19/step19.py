import csv
import numpy as np
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that contain input values that are 'wrong' (anomalous) 
    compared to the rest of the dataset. Uses Isolation Forest to detect 
    outliers in the input space.
    """
    # Identify input columns (exclude goals)
    goal_names = {'MRE-', 'ACC+', 'PRED40+'}
    input_indices = [i for i, name in enumerate(header) if name not in goal_names]
    
    # Prepare data for anomaly detection
    X = []
    for row in rows:
        processed = []
        for i in input_indices:
            val = row[i]
            # Handle '?' as a missing value, treat as a distinct category or mean
            if val == '?':
                processed.append(-1.0)
            elif isinstance(val, str):
                # Simple hash for symbolic columns
                processed.append(float(hash(val) % 1000))
            else:
                processed.append(float(val))
        X.append(processed)
    
    # Isolation Forest is effective for detecting anomalies in high-dimensional data
    # contamination=0.05 assumes roughly 5% of the data might be 'wrong' or extreme
    clf = IsolationForest(contamination=0.05, random_state=42)
    clf.fit(X)
    scores = clf.decision_function(X)
    
    # Lower scores indicate more anomalous (suspicious) rows
    # Sort indices by score ascending (most suspicious first)
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
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    suspicious = spot(header, rows)
    
    print("Analysis complete: Identified rows containing potentially erroneous or extreme input values.")
    print(f"The 5 most suspicious row indices are: {suspicious[:5]}")
    print("These rows contain configurations that deviate significantly from your historical data.")

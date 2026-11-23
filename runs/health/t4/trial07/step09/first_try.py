import csv
import numpy as np
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that look like failed runs (outliers) using an Isolation Forest.
    Failed runs often exhibit anomalous input combinations that lead to poor 
    performance or inconsistent behavior.
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
            if isinstance(val, str):
                # Simple hash for symbolic columns
                processed.append(float(hash(val) % 1000))
            else:
                processed.append(float(val))
        X.append(processed)
    
    # Isolation Forest is effective for detecting anomalies in high-dimensional data
    # contamination='auto' lets the model decide the threshold
    clf = IsolationForest(contamination=0.05, random_state=42)
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
    
    print("Analysis complete: Identified rows that appear to be failed runs.")
    print(f"Top 10 most suspicious row indices: {suspicious[:10]}")
    print("These rows contain input combinations that deviate significantly from the norm.")

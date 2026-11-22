import csv
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that look like failed runs (outliers) using IsolationForest.
    Returns the indices of the rows, most suspicious (most anomalous) first.
    """
    # Prepare input data for anomaly detection
    # We only use input columns (not goals) to find "weird" configurations
    input_indices = [i for i, h in enumerate(header) if h not in ['MRE-', 'ACC+', 'PRED40+']]
    
    X = []
    for row in rows:
        x_row = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                # Simple encoding for symbolic columns
                x_row.append(hash(val))
            else:
                x_row.append(float(val))
        X.append(x_row)
    
    # IsolationForest is effective for detecting outliers in high-dimensional data
    # We must fit the model before calling decision_function
    clf = IsolationForest(contamination=0.05, random_state=42)
    clf.fit(X)
    scores = clf.decision_function(X)
    
    # decision_function returns lower scores for more anomalous samples
    # We want to return indices sorted by suspicion (lowest score first)
    indexed_scores = list(enumerate(scores))
    indexed_scores.sort(key=lambda x: x[1])
    
    return [i for i, score in indexed_scores]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)
            
    suspicious_indices = spot(header, rows)
    
    print(f"Found {len(suspicious_indices)} rows that appear to be failed or anomalous runs.")
    print("The 10 most suspicious row indices are:")
    print(suspicious_indices[:10])

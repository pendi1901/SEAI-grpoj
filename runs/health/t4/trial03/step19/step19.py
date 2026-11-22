import csv
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that contain input values that are 'wrong' or anomalous
    compared to the rest of the dataset. Returns the indices of the rows,
    most suspicious (most anomalous) first.
    """
    # Identify input columns (exclude goals: MRE-, ACC+, PRED40+)
    input_indices = [i for i, h in enumerate(header) if h not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Prepare input data for anomaly detection
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
    
    # IsolationForest is effective for detecting outliers in high-dimensional data.
    # We use a small contamination factor to find the most extreme anomalies.
    clf = IsolationForest(contamination=0.01, random_state=42)
    clf.fit(X)
    
    # decision_function returns lower scores for more anomalous samples.
    scores = clf.decision_function(X)
    
    # Sort indices by suspicion (lowest score first)
    indexed_scores = list(enumerate(scores))
    indexed_scores.sort(key=lambda x: x[1])
    
    return [i for i, score in indexed_scores if score < 0]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns to float, keep symbolic as is
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)
            
    suspicious_indices = spot(header, rows)
    
    if not suspicious_indices:
        print("No suspicious or out-of-range configurations detected.")
    else:
        print(f"Detected {len(suspicious_indices)} configurations that are far outside the norm.")
        print("The most suspicious row indices are:")
        print(suspicious_indices[:10])

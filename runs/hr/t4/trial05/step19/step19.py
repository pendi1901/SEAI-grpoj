import csv
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed' (outliers)
    using an Isolation Forest. Returns the indices of the most suspicious 
    rows, sorted by suspicion level (most suspicious first).
    """
    # Prepare data: encode symbolic columns to numeric
    encoded_rows = []
    for row in rows:
        new_row = []
        for i, val in enumerate(row):
            if isinstance(val, str):
                # Simple hash-based encoding for symbolic columns
                new_row.append(float(hash(val) % 1000))
            else:
                new_row.append(float(val))
        encoded_rows.append(new_row)

    # Isolation Forest is effective for anomaly detection.
    # We set contamination to a small value to find the most extreme outliers.
    clf = IsolationForest(contamination=0.01, random_state=42)
    
    # decision_function returns the anomaly score (lower is more abnormal)
    decision_scores = clf.fit(encoded_rows).decision_function(encoded_rows)
    
    # Get indices of rows identified as outliers (score < 0)
    # Sort by decision_scores (most negative = most suspicious)
    suspicious_indices = [i for i, score in enumerate(decision_scores) if score < 0]
    suspicious_indices.sort(key=lambda i: decision_scores[i])
    
    return suspicious_indices

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
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
    
    print("Analysis: Identifying employees who are unlike anyone we have employed.")
    print(f"We have identified {len(suspicious)} records that are statistically anomalous.")
    print("Estimates for these records cannot be trusted as they deviate significantly from historical norms.")
    if suspicious:
        print(f"The most suspicious record is at index {suspicious[0]}.")
    
    exit(0)

import csv
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that look 'wrong' (outliers) using an Isolation Forest.
    Returns the indices of the most suspicious rows, sorted by suspicion level.
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

    # Isolation Forest is effective for anomaly detection
    # contamination='auto' lets the model decide the proportion of outliers
    clf = IsolationForest(contamination=0.05, random_state=42)
    
    # decision_function returns the anomaly score (lower is more abnormal)
    scores = clf.fit_predict(encoded_rows)
    decision_scores = clf.decision_function(encoded_rows)
    
    # Get indices of rows identified as outliers (-1)
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
    
    print(f"Analysis complete. Identified {len(suspicious)} potentially erroneous records.")
    print("Top 5 most suspicious row indices:")
    for idx in suspicious[:5]:
        print(f" - Row {idx}")

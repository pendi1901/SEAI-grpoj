import csv
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

def flow(header, row, seen):
    """
    Detects if the current row is an outlier compared to the 'seen' history.
    We use an Isolation Forest to determine if the new row deviates from 
    the distribution of the previously seen data.
    """
    if len(seen) < 20:
        return False

    # Combine seen rows and current row into a temporary dataset
    all_rows = seen + [row]
    
    # Encode data for Isolation Forest
    X = []
    for r in all_rows:
        encoded_row = []
        for i, val in enumerate(r):
            if isinstance(val, (int, float)):
                encoded_row.append(float(val))
            else:
                # Simple hash or index-based encoding for symbolic data
                encoded_row.append(float(hash(val) % 1000))
        X.append(encoded_row)
    
    # Use Isolation Forest to detect if the last row is an anomaly
    # We train on the 'seen' data and predict for the new row
    clf = IsolationForest(n_estimators=50, contamination=0.05, random_state=42)
    clf.fit(X[:-1])
    
    # If the score is negative, it's considered an anomaly
    score = clf.decision_function([X[-1]])
    return score[0] < 0

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
    
    seen = []
    anomalies = 0
    for row in rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
    
    print(f"Analysis complete.")
    print(f"Total employees processed: {len(rows)}")
    print(f"Number of times the team composition appeared to shift (anomalies detected): {anomalies}")
    print("Logic: Used Isolation Forest to flag rows that deviate significantly from historical trends.")

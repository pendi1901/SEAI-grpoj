import csv
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

def spot(header, rows):
    """
    Identifies suspicious rows using an Isolation Forest.
    Rows with lower anomaly scores are considered more suspicious.
    """
    # Prepare data for Isolation Forest
    X = []
    encoders = {}
    
    for row in rows:
        processed_row = []
        for i, val in enumerate(row):
            if isinstance(val, str):
                if i not in encoders:
                    le = LabelEncoder()
                    le.fit([str(r[i]) for r in rows])
                    encoders[i] = le
                processed_row.append(encoders[i].transform([str(val)])[0])
            else:
                processed_row.append(val)
        X.append(processed_row)
    
    # Isolation Forest detects anomalies
    # contamination is set to a small value to find outliers
    clf = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    scores = clf.fit_predict(X)
    anomaly_scores = clf.decision_function(X)
    
    # Get indices of rows sorted by suspicion (lowest score = most suspicious)
    suspicious_indices = sorted(range(len(anomaly_scores)), key=lambda i: anomaly_scores[i])
    
    # Return only the rows identified as anomalies (-1)
    return [i for i in suspicious_indices if scores[i] == -1]

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
    
    print("Suspicious rows identified (most suspicious first):")
    for i, idx in enumerate(suspicious[:10]):
        print(f"{i+1}. Row index {idx} (Anomaly score rank)")
    
    if not suspicious:
        print("No suspicious records found.")
    else:
        print(f"\nTotal suspicious records identified: {len(suspicious)}")

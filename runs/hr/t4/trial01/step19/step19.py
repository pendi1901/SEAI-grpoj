import csv
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed' (anomalies)
    using an Isolation Forest. Returns indices of suspicious rows,
    most suspicious first.
    """
    # Identify goal columns to exclude from anomaly detection
    goal_indices = [i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-')]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Prepare data for Isolation Forest
    X = []
    encoders = {}
    
    for row in rows:
        processed_row = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                if i not in encoders:
                    le = LabelEncoder()
                    # Fit on all rows to ensure consistent encoding
                    le.fit([str(r[i]) for r in rows])
                    encoders[i] = le
                processed_row.append(encoders[i].transform([str(val)])[0])
            else:
                processed_row.append(val)
        X.append(processed_row)
    
    # Isolation Forest detects anomalies
    # Contamination is set to 0.05 to identify the most distinct 5% of records
    clf = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    clf.fit(X)
    
    # decision_function returns the anomaly score (lower = more anomalous)
    scores = clf.decision_function(X)
    
    # Get indices of rows sorted by suspicion (lowest score = most suspicious)
    suspicious_indices = sorted(range(len(scores)), key=lambda i: scores[i])
    
    # Return the indices of the rows identified as anomalies (score < 0)
    return [i for i in suspicious_indices if scores[i] < 0]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    suspicious = spot(header, rows)
    
    print("Analysis: Identifying records that are unlike existing employees.")
    if not suspicious:
        print("No suspicious records found.")
    else:
        print(f"Found {len(suspicious)} records that are statistically unlike the current workforce.")
        print("The estimates for these specific employees cannot be fully trusted.")
        print("Top 5 most suspicious row indices:")
        for idx in suspicious[:5]:
            print(f"- Row index {idx}")

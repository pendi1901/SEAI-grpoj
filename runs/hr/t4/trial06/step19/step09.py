import csv
import pandas as pd
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that look 'wrong' (outliers) using an Isolation Forest.
    Returns the indices of the most suspicious rows, sorted by suspicion level.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Prepare data: convert all to numeric for anomaly detection
    # We use factorize for symbolic columns to keep them in the model
    df_numeric = df.copy()
    for col in header:
        if not col[0].isupper():
            df_numeric[col] = pd.factorize(df[col])[0]
            
    # Isolation Forest is effective for detecting anomalies in high-dimensional data
    # contamination='auto' lets the model decide the threshold
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    
    # Fit the model before calling decision_function
    model.fit(df_numeric)
    
    # decision_function returns the anomaly score (lower is more abnormal)
    scores = model.decision_function(df_numeric)
    
    # Get indices sorted by score (most negative = most suspicious)
    suspicious_indices = sorted(range(len(scores)), key=lambda i: scores[i])
    
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
    
    print("Analysis: Identifying potentially erroneous data entries.")
    print("The following row indices are the most suspicious (most likely to contain typos):")
    for i in range(min(10, len(suspicious))):
        print(f"Row {suspicious[i]} (Suspicion Rank {i+1})")
    
    print("\nThese rows were identified using an Isolation Forest anomaly detection model.")

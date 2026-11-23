import csv
import pandas as pd
from sklearn.ensemble import IsolationForest

def flow(header, row, seen):
    """
    Detects if the current row is an anomaly compared to the 'seen' distribution.
    Returns True if the row is an outlier (the team no longer looks normal),
    False otherwise.
    """
    if len(seen) < 30:
        return False

    # Convert seen rows and current row to DataFrame
    df_seen = pd.DataFrame(seen, columns=header)
    df_row = pd.DataFrame([row], columns=header)
    
    # Prepare data: factorize symbolic columns for anomaly detection
    df_combined = pd.concat([df_seen, df_row], axis=0)
    df_numeric = df_combined.copy()
    for col in header:
        if not col[0].isupper():
            df_numeric[col] = pd.factorize(df_combined[col])[0]
            
    # Use Isolation Forest to detect if the new row is an outlier
    # We fit on 'seen' and predict on the new row
    model = IsolationForest(n_estimators=50, contamination=0.05, random_state=42)
    model.fit(df_numeric.iloc[:-1])
    
    # decision_function < 0 indicates an anomaly
    score = model.decision_function(df_numeric.iloc[[-1]])
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

    print("Team Normality Analysis:")
    print(f"Total records processed: {len(rows)}")
    print(f"Number of times the team composition deviated from the norm: {anomalies}")
    print("The system flags a row as a deviation when it is identified as an outlier by an Isolation Forest model.")

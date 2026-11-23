import csv
import pandas as pd
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed' (outliers).
    Uses an Isolation Forest to detect rows that deviate significantly from
    the distribution of the existing staff. Returns indices of the most
    suspicious rows, sorted by suspicion level (most suspicious first).
    """
    # Convert rows to DataFrame for processing
    df = pd.DataFrame(rows, columns=header)
    
    # Prepare data: convert symbolic columns to numeric for the model
    df_numeric = df.copy()
    for col in header:
        if not col[0].isupper():
            # Factorize handles symbolic data by mapping to unique integers
            df_numeric[col] = pd.factorize(df[col])[0]
            
    # Isolation Forest is ideal for detecting anomalies (unusual hires)
    # contamination='auto' allows the model to determine the threshold
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(df_numeric)
    
    # decision_function returns the anomaly score (lower is more abnormal)
    scores = model.decision_function(df_numeric)
    
    # Get indices sorted by score (most negative = most suspicious/unlike others)
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
    
    print("Analysis: Identifying hires unlike anyone we have employed.")
    print("The following row indices represent the most 'unusual' profiles in our data,")
    print("where our performance estimates are least likely to be reliable:")
    for i in range(min(10, len(suspicious))):
        print(f"Row {suspicious[i]} (Suspicion Rank {i+1})")
    
    print("\nThese rows were identified using an Isolation Forest anomaly detection model.")

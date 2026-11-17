import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are outliers using Isolation Forest.
    Returns the indices of the most suspicious rows, sorted by 
    anomaly score (most suspicious first).
    """
    # Convert rows to a DataFrame
    df = pd.DataFrame(rows, columns=header)
    
    # Convert numeric columns to float, handle potential non-numeric data
    for col in header:
        if col[0].isupper():
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Fill NaNs if any (though problem implies clean numeric data)
    df = df.fillna(0)
    
    # Isolation Forest to detect anomalies
    # contamination='auto' lets the model decide the threshold
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    
    # Get anomaly scores (lower is more anomalous)
    scores = model.decision_function(df)
    
    # Get indices sorted by score (ascending, so lowest scores first)
    suspicious_indices = np.argsort(scores)
    
    return suspicious_indices.tolist()

if __name__ == "__main__":
    filename = 'pom3a.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    
    suspicious = spot(header, rows)
    
    print("Customer Inquiry: Which records look mistyped or made up?")
    print(f"Analysis: Identified {len(suspicious)} suspicious records.")
    print("The 5 most suspicious row indices are:")
    for idx in suspicious[:5]:
        print(f"- Row {idx}")
    
    print("\nThese rows were flagged as outliers based on their input/goal distributions.")

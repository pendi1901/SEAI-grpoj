import pandas as pd
import numpy as np
import csv
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are outliers in the input space using IsolationForest.
    Returns the indices of the most suspicious rows, sorted by anomaly score.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns and input columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Preprocess: Convert symbolic inputs to numeric using one-hot encoding
    # We only care about inputs for detecting "mistyped" or "made up" records
    df_inputs = pd.get_dummies(df[inputs])
    
    # Isolation Forest is effective for detecting anomalies in high-dimensional data
    # contamination is set to a small value assuming most data is valid
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    
    # Fit the model and get anomaly scores
    # scores: -1 for outliers, 1 for inliers
    # decision_function: lower values are more anomalous
    scores = model.decision_function(df_inputs)
    
    # Get indices of rows sorted by anomaly score (most negative first)
    suspicious_indices = np.argsort(scores)
    
    return suspicious_indices.tolist()

if __name__ == "__main__":
    filename = 'pom3a.train.csv'
    
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
    
    print("--- Anomaly Detection Report ---")
    print(f"Detected {len(suspicious[:10])} potentially mistyped or anomalous records.")
    print("The following row indices are the most suspicious (most anomalous first):")
    print(suspicious[:10])
    print("\nThese records deviate significantly from the patterns observed in the rest of the dataset.")
    
    exit(0)

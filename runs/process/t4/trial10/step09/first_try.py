import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are outliers using Isolation Forest.
    Returns the indices of rows, sorted by suspicion (highest anomaly score first).
    """
    df = pd.DataFrame(rows, columns=header)
    
    # IsolationForest works well for detecting anomalies in multi-dimensional data
    # We use all columns as they all contribute to the definition of a "valid" record
    model = IsolationForest(contamination=0.05, random_state=42)
    
    # Fit the model and get anomaly scores (lower is more anomalous)
    # decision_function returns the anomaly score of the input samples
    scores = model.decision_function(df)
    
    # Get indices sorted by score (ascending, so most negative/anomalous first)
    suspicious_indices = np.argsort(scores)
    
    return suspicious_indices.tolist()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to float
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        indices = spot(header, rows)
        
        print("Anomaly Detection Report:")
        print(f"Identified {len(indices)} potentially mistyped or outlier records.")
        print("The 5 most suspicious rows (by index) are:")
        for idx in indices[:5]:
            print(f"Row {idx} (Anomaly Score Rank: {indices.index(idx) + 1})")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

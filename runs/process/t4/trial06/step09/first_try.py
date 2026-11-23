import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are outliers (potentially mistyped or made up)
    using an Isolation Forest algorithm.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input columns (non-goal columns)
    input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    
    # Use Isolation Forest to detect anomalies
    # contamination is set to a small value (e.g., 0.05) assuming few errors
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    
    # Fit on input columns
    X = df[input_cols]
    
    # decision_function returns the anomaly score (lower is more abnormal)
    scores = model.decision_function(X)
    
    # Get indices of rows sorted by anomaly score (most suspicious first)
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
                processed_row = [float(val) for val in row]
                rows.append(processed_row)
        
        suspicious = spot(header, rows)
        
        print("Analysis complete. The following rows appear to be outliers or mistyped:")
        print(f"Top 10 most suspicious row indices: {suspicious[:10]}")
        print("These rows deviate significantly from the patterns observed in the rest of the dataset.")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

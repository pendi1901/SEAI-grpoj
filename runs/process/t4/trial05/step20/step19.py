import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are outliers in the input space using IsolationForest.
    Returns the indices of the most suspicious rows, sorted by anomaly score.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input columns (those not ending in - or +)
    inputs = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    
    # Use IsolationForest to detect anomalies
    # contamination='auto' lets the model decide the threshold
    model = IsolationForest(contamination=0.05, random_state=42)
    
    # Fit on input columns
    X = df[inputs]
    # decision_function returns lower values for more anomalous points
    scores = model.fit(X).decision_function(X)
    
    # Sort indices by score (ascending: most suspicious first)
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
                # Convert numeric columns to floats
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious = spot(header, rows)
        
        print("Customer Inquiry: Identifying setups unlike anything we have run.")
        print(f"Analysis complete. Found {len(suspicious)} setups that deviate from historical norms.")
        print("The 5 most suspicious row indices are:")
        print(suspicious[:5])
        print("\nThese rows represent configurations that are statistically novel or anomalous.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

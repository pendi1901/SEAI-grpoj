import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are outliers using the Isolation Forest algorithm.
    Returns the indices of the rows, sorted by suspicion level (highest first).
    """
    df = pd.DataFrame(rows, columns=header)
    
    # IsolationForest works well for detecting anomalies in numeric data.
    # We use the contamination parameter to estimate the proportion of outliers.
    # A value of 0.05 is a reasonable heuristic for "mistyped or made up" data.
    model = IsolationForest(contamination=0.05, random_state=42)
    
    # Fit the model and get anomaly scores (lower scores are more anomalous)
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
                # Convert numeric columns to floats
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious = spot(header, rows)
        
        print("Customer Inquiry: Identifying potentially mistyped or invalid records.")
        print(f"Analysis: Found {len(suspicious)} suspicious records.")
        print("Top 10 most suspicious row indices:")
        print(suspicious[:10])
        print("\nThese records deviate significantly from the patterns observed in the rest of the dataset.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are outliers (unseen or unusual configurations)
    using the Isolation Forest algorithm.
    Returns the indices of the rows, sorted by suspicion (most suspicious first).
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns and input columns
    # We only care about inputs because the customer is asking about 
    # the "setup" (the configuration), not the outcomes.
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Prepare numeric input data
    # We convert to numeric, coercing errors to NaN to handle potential bad data
    X = df[inputs].apply(pd.to_numeric, errors='coerce')
    
    # Fill NaNs with the median to allow the model to run
    X = X.fillna(X.median())
    
    # IsolationForest returns -1 for outliers and 1 for inliers.
    # The decision_function returns the anomaly score (lower is more anomalous).
    # We use a small contamination factor to find the most extreme cases.
    clf = IsolationForest(contamination=0.02, random_state=42)
    clf.fit(X)
    
    # Get anomaly scores (lower = more suspicious)
    scores = clf.decision_function(X)
    
    # Get indices of rows sorted by score (ascending, so lowest scores first)
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
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious = spot(header, rows)
        
        print("Anomaly Detection Report:")
        print(f"I have analyzed the {len(rows)} setups in your history.")
        print("The following row indices represent configurations that are highly unusual")
        print("or unlike anything we have run before:")
        print(suspicious[:5])
        print("\nThese setups are statistically distinct from your standard operating procedures.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

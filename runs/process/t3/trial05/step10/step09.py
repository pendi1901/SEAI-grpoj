import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are outliers in the input space using Isolation Forest.
    Returns the indices of the rows, sorted by their anomaly score (most suspicious first).
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input columns (those not ending in - or +)
    input_cols = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    
    # Use Isolation Forest to detect anomalies
    # contamination='auto' lets the model decide the threshold
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    
    # Fit the model on input columns
    # decision_function returns the anomaly score (lower is more abnormal)
    scores = model.fit(df[input_cols]).decision_function(df[input_cols])
    
    # Get indices of rows sorted by anomaly score (ascending, so lowest scores first)
    # The lower the score, the more "suspicious" the row is.
    suspicious_indices = np.argsort(scores)
    
    # Filter to only include rows that were actually flagged as anomalies (score < 0)
    # and return them as a list of ints
    flagged = [int(i) for i in suspicious_indices if scores[i] < 0]
    
    return flagged

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
        
        print(f"Customer Inquiry: Which records look mistyped or made up?")
        print(f"Analysis: Found {len(suspicious)} suspicious records.")
        if suspicious:
            print("The most suspicious row indices (most anomalous first) are:")
            print(suspicious[:10])
            print("...")
        else:
            print("No significant outliers detected.")
            
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

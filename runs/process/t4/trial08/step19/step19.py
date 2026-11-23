import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are outliers (unseen/anomalous configurations)
    using an Isolation Forest algorithm on input columns.
    Returns the indices of rows, most suspicious first.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input columns (those not ending in - or +)
    inputs = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    
    # Isolation Forest detects anomalies in the input space
    # contamination=0.05 assumes roughly 5% of data might be "unlike anything seen"
    clf = IsolationForest(contamination=0.05, random_state=42)
    clf.fit(df[inputs])
    
    # decision_function returns anomaly scores; lower scores are more anomalous
    scores = clf.decision_function(df[inputs])
    
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
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print("Customer Inquiry: Tell me when I am asking about something you have never seen.")
        print("Analysis: We identified records that deviate significantly from historical patterns.")
        print(f"The most suspicious row indices (most unlike previous runs) are: {suspicious_indices[:10]}")
        print("Conclusion: These configurations are outliers. Proceed with caution as they represent setups we have not encountered before.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

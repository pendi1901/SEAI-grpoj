import csv
import pandas as pd
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are outliers using Isolation Forest.
    Returns the indices of the rows, sorted by suspicion (highest anomaly score first).
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Isolation Forest works on numeric data.
    df_numeric = df.copy()
    for col in df_numeric.columns:
        # If column is symbolic, convert to numeric codes
        if df_numeric[col].dtype == 'object':
            df_numeric[col] = pd.factorize(df_numeric[col])[0]
        else:
            # Replace "?" with mean for anomaly detection
            mask = df_numeric[col] == "?"
            if mask.any():
                mean_val = df_numeric.loc[~mask, col].mean()
                df_numeric.loc[mask, col] = mean_val
                df_numeric[col] = df_numeric[col].astype(float)

    # Fit Isolation Forest
    clf = IsolationForest(contamination=0.05, random_state=42)
    clf.fit(df_numeric)
    scores = clf.decision_function(df_numeric)
    
    # Lower scores are more anomalous. 
    # We return indices sorted by score ascending (most suspicious first).
    indices = sorted(range(len(scores)), key=lambda i: scores[i])
    
    return indices

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
        
        print("Customer Inquiry: Which records look mistyped or made up?")
        print(f"Analysis: Found {len(suspicious_indices)} potentially anomalous records.")
        print("The 10 most suspicious row indices are:")
        print(suspicious_indices[:10])
        print("\nThese rows deviate significantly from the patterns observed in the rest of the dataset.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

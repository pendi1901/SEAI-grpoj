import csv
import pandas as pd
from sklearn.ensemble import IsolationForest

def spot(header, rows):
    """
    Identifies rows that are outliers (potentially mistyped or made up)
    using the Isolation Forest algorithm.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # We only consider numeric columns for anomaly detection
    numeric_cols = [c for c in header if c in df.select_dtypes(include=['number']).columns]
    data = df[numeric_cols]
    
    # Isolation Forest is effective at detecting anomalies in high-dimensional data
    # contamination='auto' lets the model decide the proportion of outliers
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    
    # Fit the model and get anomaly scores
    # -1 indicates an outlier, 1 indicates an inlier
    model.fit(data)
    scores = model.decision_function(data)
    
    # Get indices of rows sorted by suspicion (lowest score = most suspicious)
    suspicious_indices = sorted(range(len(scores)), key=lambda i: scores[i])
    
    return suspicious_indices

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
        
        outliers = spot(header, rows)
        
        print("Customer Inquiry: Which records look mistyped or made up?")
        print("-" * 60)
        print("Analysis: The following rows are statistically anomalous and may contain errors:")
        for i, idx in enumerate(outliers[:10]):
            print(f"{i+1}. Row index {idx} (Suspicion score rank: {i+1})")
        
        print("\nThese rows deviate significantly from the patterns observed in the rest of the dataset.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

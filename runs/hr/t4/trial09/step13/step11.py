import csv
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

def remember(header, rows):
    """
    Finds the 5% of employees most similar to the first employee in the dataset
    (the reference employee) based on input features.
    """
    # Identify input columns (those not ending in + or -)
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('+') or name.endswith('-'))]
    
    # Prepare feature matrix
    X = []
    encoders = {}
    for i in input_indices:
        if not header[i][0].isupper():
            le = LabelEncoder()
            le.fit([str(row[i]) for row in rows])
            encoders[i] = le

    for row in rows:
        features = []
        for i in input_indices:
            if i in encoders:
                features.append(encoders[i].transform([str(row[i])])[0])
            else:
                features.append(float(row[i]))
        X.append(features)
    
    # Use NearestNeighbors to find similarity to the first row
    n_neighbors = max(1, int(len(rows) * 0.05))
    nn = NearestNeighbors(n_neighbors=n_neighbors + 1)
    nn.fit(X)
    
    # Find neighbors of the first row (index 0)
    distances, indices = nn.kneighbors([X[0]])
    
    # Return indices of neighbors (excluding the reference row itself)
    return [idx for idx in indices[0] if idx != 0][:n_neighbors]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
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
    
    best_indices = remember(header, rows)
    
    goal_idx = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')][0]
    
    print(f"Reference Employee (Row 0) Tenure: {rows[0][goal_idx]}")
    print("Most similar employees and their tenure:")
    print(f"{'Index':<10} | {'Tenure (YearsAtCompany+)':<25}")
    print("-" * 40)
    for idx in best_indices:
        print(f"{idx:<10} | {rows[idx][goal_idx]:<25}")

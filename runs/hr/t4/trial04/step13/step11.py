import csv
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

def remember(header, rows):
    """
    Finds the 5% of employees most similar to the first employee (rows[0]).
    Similarity is calculated using Euclidean distance on encoded features.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Exclude goal columns for similarity calculation
    input_cols = [c for c in header if not (c.endswith('+') or c.endswith('-'))]
    X = df[input_cols].copy()
    
    # Encode symbolic columns and ensure numeric are float
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
        else:
            X[col] = X[col].astype(float).fillna(0)
            
    # Find nearest neighbors to the first row
    # We look for n_neighbors + 1 because the first neighbor is the row itself
    n_neighbors = max(1, len(rows) // 20)
    nn = NearestNeighbors(n_neighbors=n_neighbors + 1)
    nn.fit(X)
    
    # Query for the first row
    distances, indices = nn.kneighbors([X.iloc[0]])
    
    # Return the indices of the neighbors (excluding the first one which is the row itself)
    return indices[0][1:].tolist()

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns (Upper case start) to float
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    indices = remember(header, rows)
    
    goal_col = next(c for c in header if c.endswith('+') or c.endswith('-'))
    goal_idx = header.index(goal_col)
    
    print(f"Employees most similar to the first record (Row 0):")
    print(f"{'Index':<10} | {'YearsAtCompany+'}")
    print("-" * 30)
    for idx in indices:
        print(f"{idx:<10} | {rows[idx][goal_idx]}")

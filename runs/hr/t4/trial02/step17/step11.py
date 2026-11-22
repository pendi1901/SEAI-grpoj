import csv
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

def remember(header, rows):
    """
    Finds the 5% of employees most similar to the last employee in the dataset.
    Similarity is calculated using Euclidean distance on encoded features.
    """
    # Prepare dataframe
    df = pd.DataFrame(rows, columns=header)
    
    # Select input features (exclude goals)
    features = [c for c in header if not (c.endswith('+') or c.endswith('-'))]
    
    # Encode symbolic columns to numeric for distance calculation
    df_encoded = df.copy()
    for col in header:
        if df_encoded[col].dtype == 'object':
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            
    # Use the last row as the target
    target = df_encoded.iloc[[-1]][features]
    data = df_encoded[features]
    
    # Find nearest neighbors
    n_neighbors = max(1, int(len(rows) * 0.05))
    # We ask for n_neighbors + 1 because the target row is included in the dataset
    nn = NearestNeighbors(n_neighbors=n_neighbors + 1)
    nn.fit(data)
    
    # Get indices
    distances, indices = nn.kneighbors(target)
    
    # Filter out the target row itself (the last one)
    result_indices = [i for i in indices[0] if i != len(rows) - 1]
    
    return result_indices[:n_neighbors]

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
    
    indices = remember(header, rows)
    
    years_idx = header.index('YearsAtCompany+')
    print("Employees most similar to the last record:")
    print(f"{'Index':<10} | {'YearsAtCompany+'}")
    print("-" * 30)
    for idx in indices:
        print(f"{idx:<10} | {rows[idx][years_idx]}")

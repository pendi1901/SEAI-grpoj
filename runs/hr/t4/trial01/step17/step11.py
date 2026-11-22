import csv
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

def remember(header, rows):
    """
    Finds the 5% of employees most similar to the last employee in the dataset.
    Similarity is calculated using Euclidean distance on encoded features.
    """
    # Identify goal column to exclude from similarity calculation
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    
    # Prepare data for similarity (exclude goal)
    X = []
    encoders = {}
    for i in range(len(header)):
        if i == goal_idx:
            continue
        col_data = [row[i] for row in rows]
        if isinstance(col_data[0], str):
            le = LabelEncoder()
            le.fit(col_data)
            encoders[i] = le
            X.append(le.transform(col_data))
        else:
            X.append(col_data)
    
    # Transpose to get (n_samples, n_features)
    X = list(zip(*X))
    
    # Use the last row as the reference
    target = X[-1]
    
    # Find nearest neighbors
    n_neighbors = max(1, len(rows) // 20)
    nn = NearestNeighbors(n_neighbors=n_neighbors + 1)
    nn.fit(X)
    
    # Get indices of nearest neighbors (excluding the target itself)
    distances, indices = nn.kneighbors([target])
    
    # Return indices excluding the last row (the target itself)
    result = [i for i in indices[0] if i != len(rows) - 1]
    return result[:n_neighbors]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    indices = remember(header, rows)
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    
    print(f"Employees most similar to the last record (Index {len(rows)-1}):")
    print(f"{'Index':<10} | {'YearsAtCompany+':<15}")
    print("-" * 30)
    for idx in indices:
        print(f"{idx:<10} | {rows[idx][goal_idx]:<15}")

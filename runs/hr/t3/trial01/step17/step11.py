import csv
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

def remember(header, rows):
    """
    Finds the 5% of employees most similar to the first employee (index 0)
    based on input features, and returns their indices.
    """
    # Identify goal columns (ending in + or -)
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Encode symbolic columns for distance calculation
    encoders = {}
    for i in input_indices:
        if not header[i][0].isupper():
            le = LabelEncoder()
            le.fit([str(r[i]) for r in rows])
            encoders[i] = le

    def transform(row):
        features = []
        for i in input_indices:
            val = row[i]
            if i in encoders:
                features.append(float(encoders[i].transform([str(val)])[0]))
            else:
                features.append(float(val))
        return features

    # Prepare feature matrix
    X = [transform(row) for row in rows]
    
    # Find nearest neighbors to the first row (index 0)
    # We want 5% of the total rows
    n_neighbors = max(1, int(len(rows) * 0.05))
    
    # Use NearestNeighbors to find the most similar rows
    nn = NearestNeighbors(n_neighbors=n_neighbors + 1)
    nn.fit(X)
    
    distances, indices = nn.kneighbors([X[0]])
    
    # Return the indices of the neighbors (excluding the query row itself if it's the first)
    result_indices = [idx for idx in indices[0] if idx != 0]
    
    # Ensure we return exactly the requested amount
    return result_indices[:n_neighbors]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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
    print(f"Employees most similar to the first record (Index 0):")
    print(f"{'Index':<10} | {'YearsAtCompany+'}")
    print("-" * 30)
    for idx in indices:
        print(f"{idx:<10} | {rows[idx][years_idx]}")
    
    print("\nLogic: Used K-Nearest Neighbors on input features to find the most similar staff members.")

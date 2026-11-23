import csv
from sklearn.neighbors import NearestNeighbors
import numpy as np

def remember(header, rows):
    """
    Finds the 5% of rows most similar to the 'current' setup (the last row).
    Similarity is calculated using Euclidean distance on normalized input features.
    """
    # Identify input columns (all except goals)
    input_indices = [i for i, col in enumerate(header) if not (col.endswith('-') or col.endswith('+'))]
    
    def prepare_features(data_rows):
        X = []
        for row in data_rows:
            features = []
            for i in input_indices:
                val = row[i]
                # Encode symbolic columns
                if isinstance(val, str):
                    val = hash(val) % 100
                features.append(float(val))
            X.append(features)
        return np.array(X)

    X = prepare_features(rows)
    
    # The 'current' setup is the last row
    current_setup = X[-1].reshape(1, -1)
    
    # Find nearest neighbors
    n_neighbors = max(1, int(len(rows) * 0.05))
    # We look for n_neighbors + 1 because the last row is itself
    nn = NearestNeighbors(n_neighbors=n_neighbors + 1)
    nn.fit(X)
    
    distances, indices = nn.kneighbors(current_setup)
    
    # Return indices excluding the last row (the current setup itself)
    result = [idx for idx in indices[0] if idx != len(rows) - 1]
    return result[:n_neighbors]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    best_indices = remember(header, rows)
    
    print("Analysis: Setups most similar to the current configuration.")
    print(f"Found {len(best_indices)} similar setups.")
    print("Index | MRE-   | ACC+   | PRED40+")
    print("-" * 35)
    for idx in best_indices:
        r = rows[idx]
        print(f"{idx:<5} | {r[0]:.4f} | {r[1]:.4f} | {r[2]:.4f}")

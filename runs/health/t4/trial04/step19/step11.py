import csv
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
import numpy as np

def remember(header, rows):
    """
    Identifies the rows most similar to the 'current' setup (the first row).
    Uses K-Nearest Neighbors on input features to find the most similar configurations.
    """
    # Input columns are those not ending in - or +
    input_indices = [i for i, h in enumerate(header) if '-' not in h and '+' not in h]
    
    # Prepare feature matrix
    X = []
    for row in rows:
        features = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                # Simple encoding for symbolic columns
                features.append(hash(val))
            else:
                features.append(float(val))
        X.append(features)
    
    X = np.array(X)
    
    # The 'current' setup is the first row
    current_setup = X[0].reshape(1, -1)
    
    # Find 5% of rows (800 * 0.05 = 40)
    n_neighbors = max(1, int(len(rows) * 0.05))
    
    # Use KNN to find the most similar rows
    nn = NearestNeighbors(n_neighbors=n_neighbors + 1)
    nn.fit(X)
    distances, indices = nn.kneighbors(current_setup)
    
    # Return indices (excluding the first one, which is the current setup itself)
    return indices[0][1:].tolist()

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
            rows.append(processed_row)

    best_indices = remember(header, rows)
    
    print("Analysis complete. Found setups most similar to the current one:")
    
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    for idx in best_indices:
        row = rows[idx]
        score = (1.0 - float(row[mre_idx])) + float(row[acc_idx]) + float(row[pred_idx])
        print(f"Row {idx}: Score={score:.4f}, MRE={row[mre_idx]:.4f}, ACC={row[acc_idx]:.4f}, PRED40={row[pred_idx]:.4f}")

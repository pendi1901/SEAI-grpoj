import csv
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

def remember(header, rows):
    """
    Finds the 5% of employees most similar to the first employee in the dataset.
    Similarity is based on input features (excluding goal columns).
    """
    # Identify goal columns to exclude from similarity calculation
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Prepare data for KNN
    X = []
    encoders = {}
    for row in rows:
        processed_row = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                if i not in encoders:
                    encoders[i] = LabelEncoder()
                    encoders[i].fit([str(r[i]) for r in rows])
                processed_row.append(float(encoders[i].transform([str(val)])[0]))
            else:
                processed_row.append(float(val))
        X.append(processed_row)
    
    # Find neighbors of the first row
    n_neighbors = max(1, len(rows) // 20)
    knn = NearestNeighbors(n_neighbors=n_neighbors + 1)
    knn.fit(X)
    
    # Get indices of the most similar rows (excluding the first row itself)
    distances, indices = knn.kneighbors([X[0]])
    similar_indices = [idx for idx in indices[0] if idx != 0]
    
    return similar_indices[:n_neighbors]

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
    print(f"The 5% of employees most similar to the first employee (Row 0):")
    print(f"{'Index':<10} | {'YearsAtCompany+'}")
    print("-" * 30)
    for i in indices:
        print(f"{i:<10} | {rows[i][years_idx]}")

import csv

def remember(header, rows):
    """
    Finds the 5% of employees most similar to the first employee (index 0).
    Similarity is calculated using Euclidean distance on numeric features.
    """
    # Identify numeric columns (excluding goals)
    goal_names = [name for name in header if name.endswith('+') or name.endswith('-')]
    feature_indices = [
        i for i, name in enumerate(header) 
        if name[0].isupper() and name not in goal_names
    ]
    
    # Normalize numeric features to handle different scales
    data_matrix = []
    for row in rows:
        data_matrix.append([row[i] for i in feature_indices])
    
    # Simple min-max normalization
    mins = [min(col) for col in zip(*data_matrix)]
    maxs = [max(col) for col in zip(*data_matrix)]
    
    def normalize(row_vals):
        return [(val - mins[i]) / (maxs[i] - mins[i] + 1e-9) for i, val in enumerate(row_vals)]
    
    target = normalize(data_matrix[0])
    
    # Calculate distance to target
    distances = []
    for i in range(1, len(rows)):
        current = normalize(data_matrix[i])
        dist = sum((a - b) ** 2 for a, b in zip(target, current)) ** 0.5
        distances.append((dist, i))
    
    # Sort by distance (ascending)
    distances.sort(key=lambda x: x[0])
    
    # Return top 5%
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in distances[:limit]]

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
    
    idx_tenure = header.index('YearsAtCompany+')
    print("Employees most similar to the first record and their tenure:")
    for idx in best_indices:
        tenure = rows[idx][idx_tenure]
        print(f"- Row {idx}: {tenure} years at company")

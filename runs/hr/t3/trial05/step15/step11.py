import csv
from math import sqrt

def remember(header, rows):
    """
    Finds the 5% of employees most similar to the first employee in the dataset.
    Similarity is calculated using Euclidean distance on normalized numeric features.
    """
    # Target is the first employee
    target = rows[0]
    
    # Identify numeric columns (excluding goals)
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper() and i not in goal_indices]
    
    # Normalize numeric columns to calculate distance
    mins = [min(row[i] for row in rows) for i in numeric_indices]
    maxs = [max(row[i] for row in rows) for i in numeric_indices]
    ranges = [maxs[i] - mins[i] if maxs[i] != mins[i] else 1 for i in range(len(numeric_indices))]
    
    def get_distance(row_a, row_b):
        dist = 0
        for idx, col_idx in enumerate(numeric_indices):
            val_a = (row_a[col_idx] - mins[idx]) / ranges[idx]
            val_b = (row_b[col_idx] - mins[idx]) / ranges[idx]
            dist += (val_a - val_b) ** 2
        return sqrt(dist)

    # Calculate distances for all rows
    distances = []
    for i, row in enumerate(rows):
        if i == 0: continue # Skip self
        distances.append((get_distance(target, row), i))
    
    # Sort by distance ascending
    distances.sort(key=lambda x: x[0])
    
    # Return top 5% (800 rows * 0.05 = 40 rows)
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
    print(f"{'Index':<10} | {'YearsAtCompany':<15}")
    print("-" * 30)
    for idx in best_indices:
        print(f"{idx:<10} | {rows[idx][idx_tenure]:<15}")

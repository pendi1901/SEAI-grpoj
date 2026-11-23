import csv
import math

def remember(header, rows):
    """
    Finds the 5% of employees most similar to the first employee in the dataset.
    Similarity is calculated using Euclidean distance on normalized numeric features.
    """
    # Identify numeric columns (excluding goals)
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper() and i not in goal_indices]
    
    # Normalize numeric columns
    data_matrix = []
    for row in rows:
        data_matrix.append([float(row[i]) for i in numeric_indices])
    
    mins = [min(col) for col in zip(*data_matrix)]
    maxs = [max(col) for col in zip(*data_matrix)]
    
    def normalize(row_data):
        norm = []
        for i, val in enumerate(row_data):
            denom = (maxs[i] - mins[i])
            norm.append((val - mins[i]) / denom if denom != 0 else 0)
        return norm

    norm_rows = [normalize(r) for r in data_matrix]
    
    # Target is the first row
    target = norm_rows[0]
    
    # Calculate distances
    distances = []
    for i in range(1, len(norm_rows)):
        dist = math.sqrt(sum((target[j] - norm_rows[i][j])**2 for j in range(len(target))))
        distances.append((dist, i))
    
    # Sort by distance (ascending)
    distances.sort(key=lambda x: x[0])
    
    # Return top 5% (max 40 rows for 800 total)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in distances[:limit]]

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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    best_indices = remember(header, rows)
    
    years_idx = header.index('YearsAtCompany+')
    print(f"Employees most similar to the first record (Index 0):")
    print(f"{'Index':<10} | {'YearsAtCompany+'}")
    print("-" * 30)
    for idx in best_indices:
        print(f"{idx:<10} | {rows[idx][years_idx]}")

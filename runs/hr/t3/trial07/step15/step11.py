import csv
from math import sqrt

def remember(header, rows):
    """
    Finds the 5% of employees most similar to the first employee (index 0)
    based on Euclidean distance of normalized numeric features.
    """
    # Identify numeric columns for similarity calculation
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper()]
    
    # Normalize numeric columns
    normalized_rows = []
    for row in rows:
        norm_row = []
        for i in numeric_indices:
            # Simple min-max normalization based on column data
            col_vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
            min_v, max_v = min(col_vals), max(col_vals)
            val = (row[i] - min_v) / (max_v - min_v + 1e-9)
            norm_row.append(val)
        normalized_rows.append(norm_row)
    
    # Calculate Euclidean distance from the first employee (index 0)
    target = normalized_rows[0]
    distances = []
    for i in range(1, len(rows)):
        dist = sqrt(sum((target[j] - normalized_rows[i][j])**2 for j in range(len(target))))
        distances.append((i, dist))
    
    # Sort by distance (ascending)
    distances.sort(key=lambda x: x[1])
    
    # Return top 5% (40 rows out of 800)
    limit = max(1, len(rows) // 20)
    return [d[0] for d in distances[:limit]]

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

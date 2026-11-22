import csv
import math

def remember(header, rows):
    """
    Finds the 5% of rows most similar to the last row in the dataset.
    Similarity is calculated using Euclidean distance on numeric input columns.
    """
    # Identify numeric input columns (excluding goals)
    input_indices = [
        i for i, h in enumerate(header) 
        if h[0].isupper() and not (h.endswith('+') or h.endswith('-'))
    ]
    
    # Target row is the last one
    target = rows[-1]
    
    # Calculate distances to all other rows
    distances = []
    for i in range(len(rows) - 1):
        dist = 0
        for idx in input_indices:
            # Simple normalization: assume range 0-100 for distance calculation
            # or just raw difference if values are comparable
            dist += (target[idx] - rows[i][idx]) ** 2
        distances.append((math.sqrt(dist), i))
    
    # Sort by distance ascending
    distances.sort(key=lambda x: x[0])
    
    # Return indices of the top 5% (max 40 rows for 800 records)
    limit = max(1, len(rows) // 20)
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    best_indices = remember(header, rows)
    years_idx = header.index('YearsAtCompany+')
    
    print("Employees most similar to the last record:")
    print(f"{'Index':<10} | {'YearsAtCompany+'}")
    print("-" * 30)
    for idx in best_indices:
        print(f"{idx:<10} | {rows[idx][years_idx]}")

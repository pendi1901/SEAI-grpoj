import csv
import math

def get_distance(row1, row2, header):
    """
    Calculate Euclidean distance between two rows for numeric columns,
    and Hamming distance for symbolic columns.
    """
    dist = 0.0
    for i, col in enumerate(header):
        if col.endswith('+') or col.endswith('-'):
            continue
        
        v1, v2 = row1[i], row2[i]
        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            # Normalize numeric distance (rough approximation)
            dist += (v1 - v2) ** 2
        else:
            # Symbolic distance
            if v1 != v2:
                dist += 1.0
    return math.sqrt(dist)

def remember(header, rows):
    """
    Finds the 5% of rows most similar to the first row in the dataset.
    """
    if not rows:
        return []
    
    target = rows[0]
    # Calculate distances to the target row
    distances = []
    for i, row in enumerate(rows):
        if i == 0: continue
        d = get_distance(target, row, header)
        distances.append((d, i))
    
    # Sort by distance (ascending)
    distances.sort(key=lambda x: x[0])
    
    # Return top 5%
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
            
    indices = remember(header, rows)
    
    tenure_idx = header.index("YearsAtCompany+")
    print(f"Employees most similar to the first record (Row 0):")
    for i in indices:
        print(f"Row {i}: YearsAtCompany+ = {rows[i][tenure_idx]}")

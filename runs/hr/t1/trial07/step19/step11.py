import csv

def remember(header, rows):
    """
    Finds the 5% of employees most similar to the first employee in the dataset.
    Similarity is calculated using Euclidean distance on normalized numeric inputs.
    """
    # Identify goal columns and input columns
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    input_indices = [i for i, h in enumerate(header) if i not in goal_indices and header[i][0].isupper()]
    
    # Target is the first row
    target = rows[0]
    
    # Normalize numeric inputs for distance calculation
    mins = [min(row[i] for row in rows) for i in input_indices]
    maxs = [max(row[i] for row in rows) for i in input_indices]
    ranges = [maxs[j] - mins[j] if maxs[j] != mins[j] else 1.0 for j in range(len(input_indices))]
    
    def get_dist(r1, r2):
        d = 0.0
        for j, idx in enumerate(input_indices):
            d += ((r1[idx] - r2[idx]) / ranges[j])**2
        return d**0.5

    # Calculate distances to target for all rows
    distances = []
    for i, row in enumerate(rows):
        if i == 0: continue  # Skip self
        distances.append((i, get_dist(target, row)))
    
    # Sort by distance ascending
    distances.sort(key=lambda x: x[1])
    
    # Return top 5%
    limit = max(1, int(len(rows) * 0.05))
    return [item[0] for item in distances[:limit]]

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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    best_indices = remember(header, rows)
    tenure_idx = header.index('YearsAtCompany+')
    
    print(f"Found {len(best_indices)} employees most similar to the first record:")
    for idx in best_indices:
        print(f"- Row {idx}: Tenure={rows[idx][tenure_idx]:.1f} years")

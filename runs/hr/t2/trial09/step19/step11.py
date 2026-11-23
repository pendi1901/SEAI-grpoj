import csv
import step01

def get_similarity(row1, row2, header):
    """
    Calculates a simple similarity score between two rows.
    Higher score means more similar.
    """
    score = 0
    for i, name in enumerate(header):
        # Skip goal columns as they are the target of the query
        if name.endswith('+') or name.endswith('-'):
            continue
        
        # Compare values
        if row1[i] == row2[i]:
            score += 1
        elif isinstance(row1[i], float) and isinstance(row2[i], float):
            # For numeric inputs, inverse of normalized difference
            diff = abs(row1[i] - row2[i])
            score += 1 / (1 + diff)
    return score

def remember(header, rows):
    """
    Finds the 5% of rows most similar to the first row (the 'target' employee).
    """
    target = rows[0]
    similarities = []
    
    for i in range(1, len(rows)):
        sim = get_similarity(target, rows[i], header)
        similarities.append((sim, i))
    
    # Sort by similarity descending
    similarities.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5%
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in similarities[:limit]]

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
    
    print("Employees most similar to the target (Row 0):")
    yac_idx = header.index('YearsAtCompany+')
    
    for i in best_indices:
        r = rows[i]
        print(f"- Row {i}: Stayed for {r[yac_idx]:.0f} years.")

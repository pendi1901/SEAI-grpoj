import csv
import step02

def find_similar(header, rows, target_row, k=5):
    """
    Finds the k most similar rows to the target_row based on numeric inputs.
    """
    # Identify numeric input columns (excluding goals)
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [
        i for i, name in enumerate(header) 
        if name[0].isupper() and i not in goal_indices
    ]
    
    distances = []
    for i, r_row in enumerate(rows):
        # Skip if the row is the target itself
        if r_row == target_row:
            continue
            
        dist = 0
        for idx in input_indices:
            val_t = target_row[idx]
            val_r = r_row[idx]
            if isinstance(val_t, (int, float)) and isinstance(val_r, (int, float)):
                # Normalize distance by range if possible, but simple Euclidean is fine here
                dist += (val_t - val_r) ** 2
            else:
                dist += 1e9 # Penalty for mismatch
        distances.append((dist**0.5, i))
    
    distances.sort(key=lambda x: x[0])
    return [d[1] for d in distances[:k]]

def remember(header, rows):
    """
    Returns the indices of the 5% most similar employees to the first row.
    """
    target = rows[0]
    limit = max(1, len(rows) // 20)
    return find_similar(header, rows, target, k=limit)

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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    indices = remember(header, rows)
    years_idx = header.index('YearsAtCompany+')
    
    print(f"Employees most similar to the first record (Index 0):")
    print(f"{'Index':<10} | {'YearsAtCompany+'}")
    print("-" * 30)
    for i in indices:
        print(f"{i:<10} | {rows[i][years_idx]}")

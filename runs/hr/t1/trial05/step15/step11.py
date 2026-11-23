import csv

def remember(header, rows):
    """
    Given an employee (the first row), find the 5% most similar employees
    based on numeric input features and report their tenure (YearsAtCompany+).
    """
    # Identify goal columns and input columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i, name in enumerate(header) if name[0].isupper() and i not in goal_indices]
    
    # The target is the first row
    target = rows[0]
    
    # Calculate Euclidean distance to all other rows
    distances = []
    for i in range(1, len(rows)):
        dist = 0
        valid = True
        for idx in input_indices:
            # Only compare if both are numeric
            if isinstance(target[idx], float) and isinstance(rows[i][idx], float):
                dist += (target[idx] - rows[i][idx]) ** 2
            else:
                # If symbolic, add penalty if different
                if target[idx] != rows[i][idx]:
                    dist += 1.0
        distances.append((dist**0.5, i))
    
    # Sort by distance (ascending)
    distances.sort(key=lambda x: x[0])
    
    # Return top 5% (max 40 for 800 rows)
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    indices = remember(header, rows)
    
    idx_tenure = header.index('YearsAtCompany+')
    
    print("Employees most similar to the first record and their tenure:")
    print(f"{'Index':<10} | {'YearsAtCompany':<15}")
    print("-" * 30)
    for i in indices:
        print(f"{i:<10} | {rows[i][idx_tenure]:<15.1f}")

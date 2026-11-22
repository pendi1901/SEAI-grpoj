import csv
from step01 import remember as step01_remember

def remember(header, rows):
    """
    Finds the setups most similar to the 'current' setup (the first row in the dataset).
    Similarity is based on Euclidean distance of input features.
    """
    # The 'current' setup is defined as the first row
    current_row = rows[0]
    
    # Identify input columns (all columns except the 3 goals)
    goal_indices = [0, 1, 2]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    def get_distance(row1, row2):
        dist = 0
        for i in input_indices:
            v1, v2 = row1[i], row2[i]
            if isinstance(v1, str):
                dist += 0 if v1 == v2 else 1
            else:
                dist += (v1 - v2) ** 2
        return dist ** 0.5

    # Calculate distances to the current setup
    distances = []
    for i in range(1, len(rows)):
        distances.append((get_distance(current_row, rows[i]), i))
    
    # Sort by distance ascending (most similar first)
    distances.sort(key=lambda x: x[0])
    
    # Return top 5% (max 40 rows for 800 data rows)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in distances[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    try:
                        processed.append(float(val))
                    except ValueError:
                        processed.append(0.0)
                else:
                    processed.append(val)
            rows.append(processed)

    best_indices = remember(header, rows)
    
    print("Analysis complete. Found setups most similar to the current team configuration.")
    print(f"Indices of the {len(best_indices)} most similar setups:")
    print(best_indices)
    
    print("\nTop 3 most similar configurations and their scores (1-MRE + ACC + PRED):")
    for i in range(min(3, len(best_indices))):
        idx = best_indices[i]
        r = rows[idx]
        score = (1.0 - r[0]) + r[1] + r[2]
        print(f"Row {idx}: Score {score:.4f} | Data: {r}")

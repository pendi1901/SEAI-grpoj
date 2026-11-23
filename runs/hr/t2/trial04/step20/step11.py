import csv
import step02

def remember(header, rows):
    """
    Finds the 5% of rows most similar to the first row in the dataset.
    Similarity is based on Euclidean distance of numeric input columns.
    """
    # Identify goal column
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    # Identify numeric input columns
    input_indices = [i for i, name in enumerate(header) if i != goal_idx and name[0].isupper()]
    
    # Target row is the first one
    target = rows[0]
    
    def get_dist(row1, row2):
        d = 0
        for i in input_indices:
            # Handle potential missing values or non-numeric data
            if isinstance(row1[i], (int, float)) and isinstance(row2[i], (int, float)):
                d += (row1[i] - row2[i])**2
        return d**0.5

    # Calculate distances for all rows (excluding the target itself)
    distances = []
    for i in range(1, len(rows)):
        dist = get_dist(target, rows[i])
        distances.append((dist, i))
    
    # Sort by distance ascending (most similar first)
    distances.sort(key=lambda x: x[0])
    
    # Return the indices of the top 5%
    n = len(rows)
    limit = max(1, int(n * 0.05))
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

    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    best_indices = remember(header, rows)
    
    print(f"Employees most similar to the first record (Row 0):")
    for i in best_indices:
        print(f"Row {i}: {header[goal_idx]} = {rows[i][goal_idx]}")

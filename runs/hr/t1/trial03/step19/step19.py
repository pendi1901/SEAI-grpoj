import csv

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed'.
    We use a K-Nearest Neighbors approach to calculate the distance of each row 
    to its nearest neighbor in the dataset. Rows with a very large distance to 
    their nearest neighbor are 'unlike' the rest of the population.
    """
    # Identify numeric input columns (excluding goal columns)
    input_indices = [
        i for i, name in enumerate(header) 
        if name[0].isupper() and not (name.endswith('+') or name.endswith('-'))
    ]

    # Normalize numeric inputs to [0, 1] for distance calculation
    normalized_rows = []
    for row in rows:
        norm_row = []
        for i in input_indices:
            # Simple min-max normalization based on column stats
            col_vals = [r[i] for r in rows]
            min_v, max_v = min(col_vals), max(col_vals)
            rng = max_v - min_v if max_v != min_v else 1
            norm_row.append((row[i] - min_v) / rng)
        normalized_rows.append(norm_row)

    # For each row, find the distance to the nearest neighbor
    suspicion_scores = []
    for i in range(len(normalized_rows)):
        min_dist = float('inf')
        for j in range(len(normalized_rows)):
            if i == j:
                continue
            # Euclidean distance
            dist = sum((normalized_rows[i][k] - normalized_rows[j][k])**2 for k in range(len(input_indices)))
            if dist < min_dist:
                min_dist = dist
        suspicion_scores.append((min_dist, i))

    # Sort by distance descending (most distant = most unlike others)
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicion_scores]

def load_data(filename):
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
    return header, rows

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    header, rows = load_data(filename)
    
    suspects = spot(header, rows)
    
    print("Rows identified as 'unlike anyone we have employed' (most suspicious first):")
    for i in suspects[:10]:
        print(f"- Row {i} (Distance to nearest neighbor: High)")
        
    print("\nStrategy: We calculated the Euclidean distance of each employee's numeric profile "
          "to their nearest neighbor. Employees with the largest distances are the most unique "
          "and represent cases where our estimation models are least likely to be accurate.")

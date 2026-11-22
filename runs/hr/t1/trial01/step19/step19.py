import csv

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed' by measuring
    the distance of each row from the rest of the dataset.
    
    We use the Mahalanobis-like distance (standardized Euclidean distance)
    for numeric columns. Rows with a high average distance from the 
    population mean are considered 'suspicious' or 'outliers' that 
    the model cannot reliably estimate.
    """
    # Identify numeric input columns (excluding goals)
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i, name in enumerate(header) if name[0].isupper() and i not in goal_indices]
    
    # Calculate mean and standard deviation for each numeric input
    stats = {}
    for i in input_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if len(vals) > 0:
            mu = sum(vals) / len(vals)
            sigma = (sum((x - mu) ** 2 for x in vals) / len(vals)) ** 0.5
            stats[i] = (mu, sigma)
            
    # Score rows based on their distance from the population norm
    row_scores = []
    for idx, row in enumerate(rows):
        total_z = 0
        count = 0
        for i in input_indices:
            if i in stats and stats[i][1] > 0:
                mu, sigma = stats[i]
                val = row[i] if isinstance(row[i], (int, float)) else 0
                # Z-score: how many standard deviations away from the mean
                total_z += abs(val - mu) / sigma
                count += 1
        
        if count > 0:
            # Average Z-score represents how 'unusual' the row is
            row_scores.append((total_z / count, idx))
            
    # Sort by score descending (most unusual first)
    row_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return only the indices
    return [item[1] for item in row_scores]

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
            
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying employees who are 'unlike' the current staff.")
    print("When a new hire profile is too far from these norms, our estimates cannot be trusted.")
    print("\nTop 5 most unique/suspicious row indices:")
    for i in range(min(5, len(suspicious_indices))):
        idx = suspicious_indices[i]
        print(f"- Row {idx}")
    
    print("\nConclusion: These rows represent outliers in our data. Predictions for profiles")
    print("similar to these will have high uncertainty.")

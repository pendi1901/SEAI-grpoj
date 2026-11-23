import csv

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' by detecting outliers in the input space.
    A row is considered suspicious if its input values are statistically 
    unlikely compared to the distribution of inputs in the rest of the dataset.
    """
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]
    
    # Calculate mean and standard deviation for numeric inputs to detect outliers
    stats = {}
    for i in input_indices:
        col_data = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if col_data:
            mean = sum(col_data) / len(col_data)
            std = (sum((x - mean) ** 2 for x in col_data) / len(col_data)) ** 0.5
            stats[i] = (mean, std if std > 0 else 1.0)

    suspicion_scores = []
    for row_idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            val = row[i]
            if isinstance(val, (int, float)) and i in stats:
                mean, std = stats[i]
                # Z-score: how many standard deviations away from the mean
                z = abs(val - mean) / std
                score += z
            elif isinstance(val, str):
                # For symbolic, check if it's a rare category
                col_vals = [r[i] for r in rows]
                freq = col_vals.count(val) / len(col_vals)
                if freq < 0.05:  # Rare category
                    score += 3.0
        
        suspicion_scores.append((score, row_idx))

    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return indices of the top 10 most suspicious rows
    return [item[1] for item in suspicion_scores[:10]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = []
                for i, val in enumerate(row):
                    if header[i] in ['criterion']:
                        processed.append(val)
                    else:
                        processed.append(float(val))
                rows.append(processed)
        
        suspicious_indices = spot(header, rows)
        
        print("Analysis complete. The following rows are suspected to be failed runs (outliers):")
        for idx in suspicious_indices:
            print(f"- Row index: {idx}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

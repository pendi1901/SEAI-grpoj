import csv

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' by looking for outliers in the input 
    space. Rows with input values that are extreme compared to the rest of the 
    dataset are flagged as potentially erroneous entries.
    """
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate statistics for numeric inputs to find outliers
    numeric_indices = [i for i in input_indices if header[i] != 'criterion']
    
    # Compute mean and standard deviation for each numeric column
    stats = {}
    for i in numeric_indices:
        vals = [r[i] for r in rows]
        mean = sum(vals) / len(vals)
        std = (sum((x - mean)**2 for x in vals) / len(vals))**0.5
        stats[i] = (mean, std)

    suspicious = []
    for row_idx, row in enumerate(rows):
        score = 0
        # Check numeric outliers (Z-score)
        for i in numeric_indices:
            mean, std = stats[i]
            if std > 0:
                z_score = abs(row[i] - mean) / std
                if z_score > 3:  # Threshold for extreme outlier
                    score += z_score
        
        # Check symbolic: if criterion is rare, it might be a typo/error
        crit_idx = header.index('criterion')
        crit_vals = [r[crit_idx] for r in rows]
        if crit_vals.count(row[crit_idx]) < len(rows) * 0.01:
            score += 5.0
            
        if score > 0:
            suspicious.append((row_idx, score))
            
    # Sort by score descending (most suspicious first)
    suspicious.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in suspicious]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [val if header[i] == 'criterion' else float(val) 
                                 for i, val in enumerate(row)]
                rows.append(processed_row)
        
        suspects = spot(header, rows)
        
        print(f"Identified {len(suspects)} potentially erroneous rows.")
        print("Top 5 most suspicious row indices:")
        for i in suspects[:5]:
            print(f"- Row {i}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

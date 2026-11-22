import csv

def spot(header, rows):
    """
    Identifies rows that are outliers. We calculate the mean and standard 
    deviation for each numeric input column and flag rows that have values 
    more than 3 standard deviations away from the mean.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate stats for each input column
    stats = {}
    for i in input_indices:
        vals = [float(row[i]) for row in rows]
        mu = sum(vals) / len(vals)
        sd = (sum((x - mu) ** 2 for x in vals) / len(vals)) ** 0.5
        stats[i] = (mu, sd)
    
    # Score rows based on how many standard deviations they are from the mean
    # A higher score means more suspicious.
    suspicion_scores = []
    for row_idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            mu, sd = stats[i]
            if sd > 0:
                val = float(row[i])
                dist = abs(val - mu) / sd
                if dist > 3:
                    score += dist
        if score > 0:
            suspicion_scores.append((row_idx, score))
            
    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[1], reverse=True)
    return [item[0] for item in suspicion_scores]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        suspicious_rows = spot(header, rows)
        
        if not suspicious_rows:
            print("No suspicious rows found.")
        else:
            print(f"Found {len(suspicious_rows)} potentially mistyped rows.")
            print("Top 5 most suspicious row indices:")
            for idx in suspicious_rows[:5]:
                print(f"- Row {idx}")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

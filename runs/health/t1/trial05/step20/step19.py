import csv

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' by looking for input values 
    that are far outside the observed range of the training data.
    """
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    numeric_indices = [i for i in input_indices if header[i] != 'criterion']
    
    # Calculate min/max for each numeric input to define the "known" range
    bounds = {}
    for i in numeric_indices:
        vals = [r[i] for r in rows if r[i] != "?"]
        if vals:
            bounds[i] = (min(vals), max(vals))

    # Identify valid symbolic values
    crit_idx = header.index('criterion')
    valid_criteria = set(r[crit_idx] for r in rows if r[crit_idx] != "?")

    suspicious = []
    for row_idx, row in enumerate(rows):
        score = 0
        # Check for numeric values outside the observed range
        for i in numeric_indices:
            if row[i] == "?": continue
            low, high = bounds[i]
            if row[i] < low or row[i] > high:
                score += 1.0
        
        # Check for unknown symbolic values
        if row[crit_idx] != "?" and row[crit_idx] not in valid_criteria:
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
        
        if not suspects:
            print("No suspicious configurations found.")
        else:
            print(f"Identified {len(suspects)} rows with settings outside the observed range.")
            print("Top 5 most suspicious row indices:")
            for i in suspects[:5]:
                print(f"- Row {i}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

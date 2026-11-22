import csv

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' by looking for outliers in input 
    columns. A row is suspicious if its input values are significantly 
    different from the median of that column.
    """
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Calculate medians for numeric columns to detect outliers
    medians = {}
    for i in input_indices:
        vals = [r[i] for r in rows if not isinstance(r[i], str)]
        if vals:
            sorted_vals = sorted(vals)
            medians[i] = sorted_vals[len(sorted_vals) // 2]

    suspicion_scores = []
    for row_idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            val = row[i]
            if not isinstance(val, str):
                # Calculate deviation from median
                if medians[i] != 0:
                    score += abs((val - medians[i]) / medians[i])
                else:
                    score += abs(val)
            else:
                # Symbolic columns: check if value is rare
                col_vals = [r[i] for r in rows]
                if col_vals.count(val) < len(rows) * 0.05:
                    score += 1.0
        
        suspicion_scores.append((score, row_idx))

    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicion_scores if item[0] > 0]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)
    
    suspicious_indices = spot(header, rows)
    
    print(f"Identified {len(suspicious_indices)} potentially failed/erroneous runs.")
    print("Top 5 most suspicious row indices:", suspicious_indices[:5])

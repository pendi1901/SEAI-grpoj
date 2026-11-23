import csv
import step01

def spot(header, rows):
    """
    Identifies 'failed' rows by looking for outliers in the input space.
    Rows that are statistical outliers in their input features are often 
    the result of failed runs or data entry errors.
    """
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate mean and standard deviation for numeric inputs to find outliers
    numeric_inputs = [i for i in input_indices if isinstance(rows[0][i], float)]
    
    outlier_scores = []
    for r_idx, row in enumerate(rows):
        score = 0
        for i in numeric_inputs:
            col_vals = [r[i] for r in rows]
            mean = sum(col_vals) / len(col_vals)
            std = (sum((x - mean) ** 2 for x in col_vals) / len(col_vals)) ** 0.5
            if std > 0:
                # Z-score magnitude
                score += abs((row[i] - mean) / std)
        outlier_scores.append((score, r_idx))
    
    # Sort by score descending (most suspicious first)
    outlier_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% of rows as suspicious
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in outlier_scores[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        suspicious = spot(header, rows)
        print(f"Analysis complete. Identified {len(suspicious)} potentially failed/erroneous rows.")
        print("Indices of the most suspicious rows (most suspicious first):")
        print(suspicious[:10])
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

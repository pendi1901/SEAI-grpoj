import csv
from step01 import remember

def spot(header, rows):
    """
    Identifies suspicious rows (outliers) by checking if any input value
    is significantly far from the median of its column.
    """
    input_indices = [i for i, h in enumerate(header) 
                     if not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate column statistics
    stats = {}
    for i in input_indices:
        col_vals = [r[i] for r in rows if not isinstance(r[i], str)]
        if col_vals:
            median = sorted(col_vals)[len(col_vals) // 2]
            # Use range as a proxy for spread
            spread = max(col_vals) - min(col_vals)
            stats[i] = (median, spread if spread > 0 else 1)

    suspicion_scores = []
    for row_idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            val = row[i]
            if not isinstance(val, str) and i in stats:
                median, spread = stats[i]
                # Score based on distance from median normalized by spread
                score += (abs(val - median) / spread) ** 2
        suspicion_scores.append((row_idx, score))

    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[1], reverse=True)
    return [idx for idx, score in suspicion_scores if score > 0]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = []
                for i, val in enumerate(row):
                    processed.append(val if header[i] == 'criterion' else float(val))
                rows.append(processed)
        
        suspects = spot(header, rows)
        print("Analysis: Rows identified as potentially failed runs (most suspicious first):")
        print(suspects[:10])
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

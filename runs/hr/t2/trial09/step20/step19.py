import csv
import step09

def spot(header, rows):
    """
    Identifies rows that contain input values that are 'unlike anyone we have employed'.
    We use the logic from step09 to detect outliers in numeric columns,
    but we also extend it to check for symbolic values that have never been seen before
    or are extremely rare (e.g., frequency < 1% of the dataset).
    """
    # Reuse the numeric outlier detection from step09
    suspicious_indices = step09.spot(header, rows)
    
    # Add symbolic rarity detection
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]
    
    # Calculate frequencies for symbolic columns
    symbolic_freqs = {}
    for i in input_indices:
        if not header[i][0].isupper():
            vals = [r[i] for r in rows]
            total = len(vals)
            counts = {}
            for v in vals:
                counts[v] = counts.get(v, 0) + 1
            symbolic_freqs[i] = {v: count / total for v, count in counts.items()}
    
    # Score rows by symbolic rarity
    rarity_scores = {}
    for idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            if i in symbolic_freqs:
                val = row[i]
                freq = symbolic_freqs[i].get(val, 0)
                # If a value is extremely rare (< 0.5%), it's suspicious
                if freq < 0.005:
                    score += (1.0 - freq)
        rarity_scores[idx] = score
    
    # Combine scores: numeric suspicion + symbolic rarity
    combined = []
    for idx in range(len(rows)):
        # Get numeric score from step09 logic (re-calculated or retrieved)
        num_score = 0
        for s, r_idx in step09.spot(header, [rows[idx]]): # Simplified check
            num_score = s
            
        total_score = num_score + rarity_scores.get(idx, 0)
        if total_score > 0:
            combined.append((total_score, idx))
            
    # Sort by total suspicion score descending
    combined.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in combined]

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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    suspicious = spot(header, rows)
    
    print("Analysis: Identifying rows that contain data unlike our historical records.")
    print(f"We identified {len(suspicious)} rows that contain unusual or outlier values.")
    print("Estimates for these rows may not be trustworthy as they deviate from established patterns.")
    print(f"Top 5 most suspicious row indices: {suspicious[:5]}")

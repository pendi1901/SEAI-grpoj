import csv
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with poor performance.
    We define 'bad' rows as those in the bottom 10% of the score distribution.
    We then calculate the correlation between input values and the 'badness' 
    (inverse of the score) to find the culprits.
    """
    # Identify goals and inputs
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate scores for all rows using step01 logic
    # We reuse the scoring logic by creating a temporary list of scores
    scores = []
    for row in rows:
        score = 0
        for i in goal_indices:
            # Simple score: normalize and sum
            col_vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
            mn, mx = min(col_vals), max(col_vals)
            rng = mx - mn
            norm = (row[i] - mn) / rng if rng > 0 else 0
            score += (1 - norm) if header[i].endswith('-') else norm
        scores.append(score)
    
    # Identify the worst 10%
    indexed_scores = sorted(zip(scores, range(len(rows))))
    worst_indices = [idx for score, idx in indexed_scores[:len(rows) // 10]]
    
    # For each input, check if its distribution in 'worst' rows differs significantly
    # from the global distribution.
    culprits = []
    for i in input_indices:
        vals = [rows[idx][i] for idx in worst_indices if isinstance(rows[idx][i], (int, float))]
        if not vals: continue
        
        avg_val = sum(vals) / len(vals)
        global_vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        global_avg = sum(global_vals) / len(global_vals)
        
        # If the average of this input in bad rows is significantly different 
        # from the global average, it's a potential culprit.
        if abs(avg_val - global_avg) > (0.2 * (max(global_vals) - min(global_vals))):
            culprits.append(header[i])
            
    return culprits

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for val in row:
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            data.append(processed_row)

    culprits = blame(header, data)
    print("Analysis complete.")
    print("The following settings appear to be driving poor performance:")
    for c in culprits:
        print(f"- {c}")

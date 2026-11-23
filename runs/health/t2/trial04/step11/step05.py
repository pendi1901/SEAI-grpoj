import csv
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate with poor performance.
    'Bad' rows are defined as the bottom 10% based on the multi-objective score.
    We compare the distribution of input values in the bad rows vs the rest.
    """
    # Identify goal indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Identify input indices
    input_indices = [i for i, h in enumerate(header) if h not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Score rows using step01 logic
    scores = []
    for row in rows:
        # Simple normalization for scoring
        mres = [r[mre_idx] for r in rows]
        accs = [r[acc_idx] for r in rows]
        preds = [r[pred_idx] for r in rows]
        
        def norm(val, vals, rev):
            mn, mx = min(vals), max(vals)
            if mx == mn: return 0.5
            n = (val - mn) / (mx - mn)
            return 1.0 - n if rev else n
            
        s = (norm(row[mre_idx], mres, True) + norm(row[acc_idx], accs, False) + norm(row[pred_idx], preds, False)) / 3.0
        scores.append(s)
        
    # Define bad rows (bottom 10%)
    indexed_scores = sorted(enumerate(scores), key=lambda x: x[1])
    limit = max(1, len(rows) // 10)
    bad_indices = [idx for idx, score in indexed_scores[:limit]]
    
    # Calculate average difference in inputs between bad rows and the rest
    impacts = []
    for i in input_indices:
        bad_vals = [rows[idx][i] for idx in bad_indices if isinstance(rows[idx][i], (int, float))]
        all_vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        
        if not bad_vals or not all_vals:
            continue
            
        avg_bad = sum(bad_vals) / len(bad_vals)
        avg_all = sum(all_vals) / len(all_vals)
        
        # We look for inputs where the bad rows deviate significantly from the mean
        impacts.append((header[i], abs(avg_bad - avg_all)))
        
    # Return top 2 inputs that correlate most with bad performance
    impacts.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in impacts[:2]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)
            
    blamed = blame(header, rows)
    print("The settings most responsible for poor performance are:")
    for col in blamed:
        print(f"- {col}")

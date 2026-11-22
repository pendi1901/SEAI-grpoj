import csv

def blame(header, rows):
    """
    Identifies which input columns correlate most strongly with poor performance.
    We define 'bad' rows as those in the bottom 25% of a multi-objective score.
    We then calculate the correlation between input settings and the score.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    input_cols = [i for i, h in enumerate(header) if h not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Calculate a score for each row (higher is better)
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]
    
    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)
    
    def get_score(r):
        s_mre = (max_mre - r[mre_idx]) / (max_mre - min_mre) if max_mre > min_mre else 0
        s_acc = (r[acc_idx] - min_acc) / (max_acc - min_acc) if max_acc > min_acc else 0
        s_pred = (r[pred_idx] - min_pred) / (max_pred - min_pred) if max_pred > min_pred else 0
        return s_mre + s_acc + s_pred

    scores = [get_score(r) for r in rows]
    
    # Identify the 'bad' rows (bottom 25%)
    threshold = sorted(scores)[len(scores) // 4]
    bad_rows = [rows[i] for i, s in enumerate(scores) if s <= threshold]
    
    # For each input column, calculate how much its values in bad rows 
    # deviate from the global average.
    damages = []
    for i in input_cols:
        col_vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not col_vals: continue
        
        avg = sum(col_vals) / len(col_vals)
        bad_vals = [r[i] for r in bad_rows if isinstance(r[i], (int, float))]
        if not bad_vals: continue
        
        bad_avg = sum(bad_vals) / len(bad_vals)
        # Damage is the absolute difference between bad row average and global average
        damages.append((abs(bad_avg - avg), header[i]))
        
    damages.sort(reverse=True)
    return [d[1] for d in damages[:3]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)
            
    culprits = blame(header, rows)
    print("The settings most responsible for poor performance are:")
    for c in culprits:
        print(f"- {c}")

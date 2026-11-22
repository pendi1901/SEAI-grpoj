import csv
from step01 import remember

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (high score) and is small (low N_estimators).
    We use 50 labels to sample the space, then pick the best trade-off.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    n_est_idx = header.index('N_estimators')

    # We sample 50 rows to get their true goals
    sampled = []
    for i in range(min(50, len(rows))):
        goals = label(i)
        row = [goals[0], goals[1], goals[2]] + rows[i][3:]
        sampled.append((row, i))

    # Normalize goals for scoring
    mres = [r[0][mre_idx] for r in sampled]
    accs = [r[0][acc_idx] for r in sampled]
    preds = [r[0][pred_idx] for r in sampled]
    n_ests = [r[0][n_est_idx] for r in sampled]

    def norm(v, mi, ma): return (v - mi) / (ma - mi) if ma > mi else 0
    
    best_score = -float('inf')
    best_idx = 0

    for row, original_idx in sampled:
        # Score = (Forecast Quality) - (Size Penalty)
        # Forecast Quality: 1-MRE + ACC + PRED
        # Size Penalty: Normalized N_estimators (smaller is better)
        q = (1 - norm(row[mre_idx], min(mres), max(mres))) + \
            norm(row[acc_idx], min(accs), max(accs)) + \
            norm(row[pred_idx], min(preds), max(preds))
        
        size_penalty = norm(row[n_est_idx], min(n_ests), max(n_ests))
        
        # We want high quality and low size
        score = q - size_penalty
        
        if score > best_score:
            best_score = score
            best_idx = original_idx
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)

    def label(i):
        return [rows[i][0], rows[i][1], rows[i][2]]

    masked_rows = [r[:] for r in rows]
    for r in masked_rows:
        r[0] = r[1] = r[2] = "?"

    best_idx = choose(header, masked_rows, label)
    print(f"Recommended setup index: {best_idx}")
    print("This setup balances high forecasting accuracy with a smaller model size for nightly runs.")

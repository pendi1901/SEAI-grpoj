import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    """
    n = len(rows)
    if n == 0:
        return []

    # Identify goal column indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Extract goals for normalization
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]

    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.0
        norm = (val - min_v) / (max_v - min_v)
        return (1.0 - norm) if reverse else norm

    scores = []
    for i, row in enumerate(rows):
        # Score = average of normalized goals
        s = (normalize(row[mre_idx], min_mre, max_mre, True) +
             normalize(row[acc_idx], min_acc, max_acc, False) +
             normalize(row[pred_idx], min_pred, max_pred, False)) / 3.0
        scores.append((s, i))

    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)

    # Return top 5% (or at least 1)
    limit = max(1, int(n * 0.05))
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] in ['criterion']:
                        processed_row.append(val)
                    else:
                        processed_row.append(float(val))
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print("Top-performing setups identified based on multi-objective optimization (MRE-, ACC+, PRED40+):")
        for idx in best_indices:
            row = rows[idx]
            mre, acc, pred = row[0], row[1], row[2]
            print(f"- Row {idx}: MRE={mre:.4f}, ACC={acc:.4f}, PRED40={pred:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

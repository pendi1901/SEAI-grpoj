import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We normalize the values and calculate a score for each row.
    """
    # Identify column indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Extract values for normalization
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]

    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def normalize(val, min_v, max_v):
        if max_v == min_v: return 0.0
        return (val - min_v) / (max_v - min_v)

    scores = []
    for i, row in enumerate(rows):
        # Normalize: MRE (lower is better -> 1 - norm), ACC/PRED (higher is better -> norm)
        n_mre = 1.0 - normalize(row[mre_idx], min_mre, max_mre)
        n_acc = normalize(row[acc_idx], min_acc, max_acc)
        n_pred = normalize(row[pred_idx], min_pred, max_pred)
        
        # Simple aggregate score
        score = n_mre + n_acc + n_pred
        scores.append((score, i))

    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (max 5% of 800 = 40)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns to floats
            processed_row = []
            for i, val in enumerate(row):
                if header[i] in ['criterion']:
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
    
    best_indices = remember(header, rows)
    
    print(f"Found {len(best_indices)} unusually trustworthy setups.")
    print("Top indices:", best_indices)
    print("Example of top setup:")
    print(rows[best_indices[0]])

import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We normalize values to [0, 1] and use a simple weighted sum (or Pareto-like approach)
    to rank the rows.
    """
    n = len(rows)
    limit = max(1, n // 20)  # 5% limit
    
    # Identify column indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Collect values to normalize
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]
    
    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)
    
    def normalize(val, min_v, max_v):
        if max_v == min_v: return 0
        return (val - min_v) / (max_v - min_v)
    
    scores = []
    for i, row in enumerate(rows):
        # Score = (1 - norm_mre) + norm_acc + norm_pred
        s = (1 - normalize(row[mre_idx], min_mre, max_mre)) + \
            normalize(row[acc_idx], min_acc, max_acc) + \
            normalize(row[pred_idx], min_pred, max_pred)
        scores.append((s, i))
    
    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
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
    
    print(f"Analysis complete. Found {len(best_indices)} top-performing setups.")
    print("Indices of the most trustworthy setups:")
    print(best_indices)
    
    # Print details of the top 1
    top_idx = best_indices[0]
    print(f"\nTop setup details (Row {top_idx}):")
    for h, v in zip(header, rows[top_idx]):
        print(f"  {h}: {v}")

import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We normalize the values and use a simple weighted sum to rank them.
    """
    n = len(rows)
    if n == 0:
        return []

    # Identify column indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Extract values for normalization
    mres = [row[mre_idx] for row in rows]
    accs = [row[acc_idx] for row in rows]
    preds = [row[pred_idx] for row in rows]

    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def normalize(val, min_v, max_v):
        if max_v == min_v: return 0.5
        return (val - min_v) / (max_v - min_v)

    scores = []
    for i, row in enumerate(rows):
        # Normalize: MRE (lower is better -> 1 - norm), ACC/PRED (higher is better -> norm)
        s_mre = 1 - normalize(row[mre_idx], min_mre, max_mre)
        s_acc = normalize(row[acc_idx], min_acc, max_acc)
        s_pred = normalize(row[pred_idx], min_pred, max_pred)
        
        # Aggregate score
        total = s_mre + s_acc + s_pred
        scores.append((total, i))

    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (or at least 1)
    limit = max(1, int(n * 0.05))
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    try:
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
        
        print(f"Found {len(best_indices)} top-performing setups:")
        for idx in best_indices:
            row = rows[idx]
            print(f"Row {idx}: MRE={row[0]:.4f}, ACC={row[1]:.4f}, PRED40={row[2]:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

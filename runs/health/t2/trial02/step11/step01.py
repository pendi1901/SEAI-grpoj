import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We normalize the values and use a simple weighted sum (Pareto-like approach).
    """
    n = len(rows)
    if n == 0:
        return []

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
        if max_v == min_v: return 0
        return (val - min_v) / (max_v - min_v)

    scores = []
    for i, row in enumerate(rows):
        # Normalize: MRE is minimized (1 - norm), others maximized (norm)
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
    
    # Print details of the top 3 for the customer
    print("\nTop 3 setups details:")
    for idx in best_indices[:3]:
        print(f"Row {idx}: MRE={rows[idx][0]:.4f}, ACC={rows[idx][1]:.4f}, PRED40={rows[idx][2]:.4f}")

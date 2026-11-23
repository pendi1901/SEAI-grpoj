import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We normalize values to [0, 1] and calculate a score.
    """
    # Identify column indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Collect data for normalization
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]

    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.5
        norm = (val - min_v) / (max_v - min_v)
        return (1 - norm) if reverse else norm

    scores = []
    for i, row in enumerate(rows):
        # Score = average of normalized goals
        s = (normalize(row[mre_idx], min_mre, max_mre, True) +
             normalize(row[acc_idx], min_acc, max_acc) +
             normalize(row[pred_idx], min_pred, max_pred)) / 3
        scores.append((s, i))

    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (max 40 rows for 800 input rows)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns to floats
            processed_row = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    best_indices = remember(header, rows)
    
    print(f"Analysis complete. Found {len(best_indices)} highly trustworthy setups.")
    print("Top performing row indices:", best_indices)
    print("\nSample of best row values (MRE, ACC, PRED40):")
    for idx in best_indices[:3]:
        r = rows[idx]
        print(f"Row {idx}: {r[0]:.4f}, {r[1]:.4f}, {r[2]:.4f}")

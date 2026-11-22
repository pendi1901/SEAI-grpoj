import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    """
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
             normalize(row[acc_idx], min_acc, max_acc, False) +
             normalize(row[pred_idx], min_pred, max_pred, False)) / 3
        scores.append((s, i))

    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (max 40 rows for 800 records)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print("Top performing setups identified:")
        for idx in best_indices[:5]:
            row = rows[idx]
            print(f"Index {idx}: MRE={row[0]:.4f}, ACC={row[1]:.4f}, PRED40={row[2]:.4f}")
        
        print(f"\nTotal of {len(best_indices)} setups identified as top 5% performers.")
        exit(0)
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

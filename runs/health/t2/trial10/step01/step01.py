import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We normalize the goals to [0, 1] and calculate a composite score.
    """
    n = len(rows)
    if n == 0:
        return []

    # Identify indices for goals
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Extract values to find min/max for normalization
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]

    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.5
        norm = (val - min_v) / (max_v - min_v)
        return 1 - norm if reverse else norm

    scores = []
    for i, row in enumerate(rows):
        # Score = average of normalized goals
        s1 = normalize(row[mre_idx], min_mre, max_mre, reverse=True)
        s2 = normalize(row[acc_idx], min_acc, max_acc)
        s3 = normalize(row[pred_idx], min_pred, max_pred)
        scores.append(( (s1 + s2 + s3) / 3, i))

    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (or at least 1)
    limit = max(1, int(n * 0.05))
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                # Convert numeric columns to float
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print(f"Analysis complete. Found {len(best_indices)} top-performing setups.")
        print("Indices of the most trustworthy setups:")
        print(best_indices)
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

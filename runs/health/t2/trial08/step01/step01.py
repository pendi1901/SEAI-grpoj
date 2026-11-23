import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We normalize values to [0, 1] and calculate a score for each row.
    """
    n = len(rows)
    if n == 0:
        return []

    # Identify column indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Extract columns for normalization
    mres = [row[mre_idx] for row in rows]
    accs = [row[acc_idx] for row in rows]
    preds = [row[pred_idx] for row in rows]

    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.0
        norm = (val - min_v) / (max_v - min_v)
        return (1.0 - norm) if reverse else norm

    scores = []
    for i in range(n):
        # Score = average of normalized goals (higher is better)
        s1 = normalize(rows[i][mre_idx], min_mre, max_mre, reverse=True)
        s2 = normalize(rows[i][acc_idx], min_acc, max_acc)
        s3 = normalize(rows[i][pred_idx], min_pred, max_pred)
        scores.append((s1 + s2 + s3) / 3.0)

    # Select top 5% (or at least 1)
    limit = max(1, n // 20)
    indexed_scores = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return [idx for idx, score in indexed_scores[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                # Convert numeric columns to float, keep symbolic as strings
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
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

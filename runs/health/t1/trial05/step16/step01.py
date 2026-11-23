import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We normalize values to [0, 1] and use a simple weighted sum (or Pareto-like ranking).
    """
    n = len(rows)
    if n == 0:
        return []

    # Identify goal indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Collect values for normalization
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]

    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.0
        norm = (val - min_v) / (max_v - min_v)
        return 1.0 - norm if reverse else norm

    scores = []
    for i, row in enumerate(rows):
        # Calculate score: lower MRE is better, higher ACC/PRED is better
        s1 = normalize(row[mre_idx], min_mre, max_mre, reverse=True)
        s2 = normalize(row[acc_idx], min_acc, max_acc)
        s3 = normalize(row[pred_idx], min_pred, max_pred)
        # Average the normalized objectives
        scores.append((s1 + s2 + s3) / 3.0)

    # Get top 5% indices
    limit = max(1, int(n * 0.05))
    indexed_scores = list(enumerate(scores))
    indexed_scores.sort(key=lambda x: x[1], reverse=True)
    
    return [x[0] for x in indexed_scores[:limit]]

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
        print(f"Found {len(best_indices)} top-performing setups.")
        print("Indices of the most trustworthy setups:")
        print(best_indices)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We normalize the goals to [0, 1] and calculate a composite score.
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

    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.5
        norm = (val - min_v) / (max_v - min_v)
        return 1 - norm if reverse else norm

    scores = []
    for i, row in enumerate(rows):
        # Score = average of normalized goals
        s = (normalize(row[mre_idx], min_mre, max_mre, True) +
             normalize(row[acc_idx], min_acc, max_acc, False) +
             normalize(row[pred_idx], min_pred, max_pred, False)) / 3
        scores.append((s, i))

    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)

    # Return top 5% (or at least 1)
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
    
    print(f"Analysis complete. Found {len(best_indices)} top-performing setups.")
    print("Indices of the most trustworthy setups:")
    print(best_indices)
    
    # Print details of the top 3 for the customer
    print("\nTop 3 setups:")
    for i in best_indices[:3]:
        print(f"Row {i}: MRE={rows[i][0]:.4f}, ACC={rows[i][1]:.4f}, PRED40={rows[i][2]:.4f}")

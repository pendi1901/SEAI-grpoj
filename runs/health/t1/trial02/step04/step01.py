import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    """
    # Identify column indices
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    # Normalize values to [0, 1] to compare different scales
    # Since we don't know the global min/max, we use the current batch
    mres = [r[idx_mre] for r in rows]
    accs = [r[idx_acc] for r in rows]
    preds = [r[idx_pred] for r in rows]

    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def score(row):
        # Normalize: lower MRE is better, higher ACC/PRED is better
        # Handle division by zero if all values are identical
        s_mre = (max_mre - row[idx_mre]) / (max_mre - min_mre) if max_mre > min_mre else 0
        s_acc = (row[idx_acc] - min_acc) / (max_acc - min_acc) if max_acc > min_acc else 0
        s_pred = (row[idx_pred] - min_pred) / (max_pred - min_pred) if max_pred > min_pred else 0
        return s_mre + s_acc + s_pred

    # Calculate scores and keep track of original indices
    scored_rows = []
    for i, row in enumerate(rows):
        scored_rows.append((score(row), i))

    # Sort by score descending
    scored_rows.sort(key=lambda x: x[0], reverse=True)

    # Return top 5% (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored_rows[:limit]]

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
        
        print(f"Analysis complete. Found {len(best_indices)} top-performing setups.")
        print("Indices of the most trustworthy setups:")
        print(best_indices)
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import csv

def get_utility(header, row):
    """
    Calculates a normalized utility score for a row.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # We use the row's own values to normalize against the dataset
    # but since we need a score per row, we use a simple weighted sum
    # of normalized goals.
    mre = row[mre_idx]
    acc = row[acc_idx]
    pred = row[pred_idx]
    
    # Normalize (assuming ranges based on typical data distribution)
    # MRE is usually [0, 1], ACC [0, 1], PRED [0, 1]
    return (1.0 - mre) + acc + pred

def remember(header, rows):
    """
    Finds the 5% of rows that are most similar to the 'best' performing row
    found in the dataset, based on input configuration similarity.
    """
    # 1. Find the best row
    utilities = [(get_utility(header, r), i) for i, r in enumerate(rows)]
    best_idx = max(utilities, key=lambda x: x[0])[1]
    best_row = rows[best_idx]
    
    # 2. Define input indices
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # 3. Calculate similarity (Euclidean distance in input space)
    def similarity(r1, r2):
        dist = 0
        for i in input_indices:
            v1, v2 = r1[i], r2[i]
            if isinstance(v1, (int, float)):
                dist += (v1 - v2) ** 2
            else:
                dist += 0 if v1 == v2 else 1
        return dist

    # 4. Rank rows by similarity to the best row
    similarities = []
    for i, row in enumerate(rows):
        if i == best_idx: continue
        similarities.append((similarity(best_row, row), i))
    
    similarities.sort(key=lambda x: x[0])
    
    # 5. Return top 5%
    limit = max(1, int(len(rows) * 0.05))
    return [idx for _, idx in similarities[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
            
    best_indices = remember(header, rows)
    
    print("Top setups most similar to the best-performing configuration:")
    for idx in best_indices[:5]:
        u = get_utility(header, rows[idx])
        print(f"Row {idx}: Utility={u:.4f}, MRE={rows[idx][0]:.4f}, ACC={rows[idx][1]:.4f}")

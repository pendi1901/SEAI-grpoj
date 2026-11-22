import csv

def remember(header, rows):
    """
    Identifies the best rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We use a simple Pareto-based approach or weighted normalization.
    Given the constraints, we normalize the goals and pick the top 5%.
    """
    # Identify column indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Extract goals and normalize
    # MRE is minimize, so we treat it as (1 - value) or negative value
    # ACC and PRED are maximize.
    
    scored = []
    for i, row in enumerate(rows):
        mre = row[mre_idx]
        acc = row[acc_idx]
        pred = row[pred_idx]
        
        # Simple score: (1 - MRE) + ACC + PRED
        # This assumes values are roughly in [0, 1] range
        score = (1.0 - mre) + acc + pred
        scored.append((score, i))
    
    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns
            processed_row = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    best_indices = remember(header, rows)
    
    print(f"Found {len(best_indices)} trustworthy setups.")
    print("Indices of the best performing rows:")
    print(best_indices)

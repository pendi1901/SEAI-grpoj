import csv
from step01 import remember

def spot(header, rows):
    """
    Identifies suspicious rows (failed runs).
    A row is suspicious if its goal performance is significantly worse 
    than the rest of the dataset (outliers in the negative direction).
    """
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    def get_score(row):
        # Normalize goals: (1 - MRE) + ACC + PRED
        # Lower score = worse performance
        return (1.0 - row[idx_mre]) + row[idx_acc] + row[idx_pred]

    # Calculate scores for all rows
    scores = []
    for i, row in enumerate(rows):
        scores.append((get_score(row), i))

    # Sort by score ascending (worst first)
    scores.sort(key=lambda x: x[0])

    # A "failed run" is likely in the bottom 5% of performance
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                # Convert numeric columns, keep symbolic as strings
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    try:
                        processed.append(float(val))
                    except ValueError:
                        processed.append(0.0)
                else:
                    processed.append(val)
            rows.append(processed)

    suspicious_indices = spot(header, rows)
    
    print(f"Analysis complete. Identified {len(suspicious_indices)} potentially failed runs.")
    print("Indices of the most suspicious rows (worst performance first):")
    print(suspicious_indices[:10])

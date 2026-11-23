import csv

def spot(header, rows):
    """
    Identifies rows that look like failed runs.
    A failed run often results in extreme outliers in the goal columns
    (e.g., MRE- near 1.0 or 0.0, ACC+ near 0.0).
    We calculate a 'suspicion score' based on how far a row's goals
    deviate from the population mean.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Calculate means for the goals to establish a baseline
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]
    
    m_mre = sum(mres) / len(mres)
    m_acc = sum(accs) / len(accs)
    m_pred = sum(preds) / len(preds)

    suspicion = []
    for i, row in enumerate(rows):
        # Suspicion: Euclidean distance from the mean of goals
        # Failed runs often have MRE near 1.0 (bad) and ACC/PRED near 0.0 (bad)
        d_mre = (row[mre_idx] - m_mre) ** 2
        d_acc = (row[acc_idx] - m_acc) ** 2
        d_pred = (row[pred_idx] - m_pred) ** 2
        
        # Weight MRE higher as it is a primary error metric
        score = (d_mre * 2.0) + d_acc + d_pred
        suspicion.append((score, i))

    # Sort by suspicion score descending
    suspicion.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicion]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)
            
    suspects = spot(header, rows)
    
    print("Top 5 most suspicious rows (potential failed runs):")
    for i in range(5):
        idx = suspects[i]
        print(f"Row {idx}: Suspicion Score {i+1}")
    
    print("\nThese rows exhibit goal values significantly deviating from the norm, "
          "suggesting they may be failed or erroneous experimental runs.")

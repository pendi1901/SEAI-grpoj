import csv
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder
from step01 import remember

def justify(header, rows, row):
    """
    Estimates the performance of the given row and compares it against all other rows.
    Returns (fraction_better, reason).
    """
    # Identify indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Prepare data for KNN: predict all three goals
    # We use KNN to predict MRE, ACC, and PRED40 based on input columns
    X = []
    y = []
    for r in rows:
        # Features: columns 3 to end
        features = []
        for i in range(3, len(header)):
            val = r[i]
            if isinstance(val, str):
                features.append(hash(val))
            else:
                features.append(float(val))
        X.append(features)
        y.append([float(r[mre_idx]), float(r[acc_idx]), float(r[pred_idx])])
    
    # Prepare target row features
    target_features = []
    for i in range(3, len(header)):
        val = row[i]
        if isinstance(val, str):
            target_features.append(hash(val))
        else:
            target_features.append(float(val))
            
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X, y)
    pred_mre, pred_acc, pred_pred = model.predict([target_features])[0]
    
    # Score heuristic: (1 - MRE) + ACC + PRED40
    target_score = (1.0 - pred_mre) + pred_acc + pred_pred
    
    def get_score(r):
        return (1.0 - float(r[mre_idx])) + float(r[acc_idx]) + float(r[pred_idx])
    
    scores = [get_score(r) for r in rows]
    better_than_count = sum(1 for s in scores if target_score > s)
    p = better_than_count / len(rows)
    
    reason = f"This setup is estimated to outperform {p:.1%} of all known configurations based on its input parameters."
    
    return p, reason

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
    
    # Pick a sample row to justify
    sample_row = rows[0][:]
    sample_row[0] = sample_row[1] = sample_row[2] = "?"
    
    p, reason = justify(header, rows, sample_row)
    print(f"Justification: {reason}")

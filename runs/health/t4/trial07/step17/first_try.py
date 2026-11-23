import csv
import random
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
import step07

def get_utility(row):
    """
    Utility function: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    Utility = (1 - MRE) + ACC + PRED
    """
    return (1.0 - float(row[0])) + float(row[1]) + float(row[2])

def get_size(header, row):
    """
    Proxy for 'small enough to run every night': 
    Minimize N_estimators and Max_depth.
    """
    n_idx = header.index('N_estimators')
    d_idx = header.index('Max_depth')
    # Normalize size (lower is better)
    return (float(row[n_idx]) / 200.0) + (float(row[d_idx]) / 20.0)

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (high utility) and is small (low size).
    We optimize for: Utility - (0.5 * NormalizedSize).
    """
    n_rows = len(rows)
    labeled_indices = []
    
    def get_score(row):
        return get_utility(row) - (0.5 * get_size(header, row))

    # Initial random sample
    for i in random.sample(range(n_rows), 10):
        label(i)
        labeled_indices.append(i)

    # Iteratively pick best candidates based on predicted score
    for _ in range(40):
        # Use step07's transformation logic
        X_train = [step07.choose.__globals__['transform'](rows[i]) for i in labeled_indices]
        y_train = [get_score(rows[i]) for i in labeled_indices]
        
        model = KNeighborsRegressor(n_neighbors=min(len(labeled_indices), 5))
        model.fit(X_train, y_train)
        
        best_pred = -float('inf')
        best_i = -1
        
        for i in range(n_rows):
            if i not in labeled_indices:
                pred = model.predict([step07.choose.__globals__['transform'](rows[i])])[0]
                if pred > best_pred:
                    best_pred = pred
                    best_i = i
        
        label(best_i)
        labeled_indices.append(best_i)

    return max(labeled_indices, key=lambda i: get_score(rows[i]))

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    true_rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(v) if header[i][0].isupper() else v for i, v in enumerate(row)]
            true_rows.append(processed)
    
    rows = [["?" if i < 3 else r[i] for i in range(len(r))] for r in true_rows]
    
    def label(i):
        rows[i] = true_rows[i]
        return true_rows[i]

    best_idx = choose(header, rows, label)
    print(f"Found optimal setup at index {best_idx}.")
    print(f"This configuration balances high forecast accuracy with a small footprint, "
          f"making it ideal for nightly execution.")
    print(f"Goals: MRE={rows[best_idx][0]:.4f}, ACC={rows[best_idx][1]:.4f}, PRED={rows[best_idx][2]:.4f}")

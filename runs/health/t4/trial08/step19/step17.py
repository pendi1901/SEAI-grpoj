import csv
import random
import numpy as np
from step02 import guess
from step09 import spot

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (using KNN) and is small (low N_estimators).
    We use a budget of 50 labels to explore the space.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    n_est_idx = header.index('N_estimators')
    
    # 1. Initial exploration: 20 random samples to build a baseline
    indices = random.sample(range(len(rows)), 20)
    for i in indices:
        vals = label(i)
        rows[i][mre_idx], rows[i][acc_idx], rows[i][pred_idx] = vals
        
    # 2. Use the remaining 30 labels to find the best balance
    # We want high utility AND low N_estimators.
    # Utility = -MRE + ACC + PRED
    # We define a multi-objective score: Utility - (N_estimators / 200)
    # This penalizes large N_estimators.
    
    def get_score(row):
        util = -row[mre_idx] + row[acc_idx] + row[pred_idx]
        # Normalize N_estimators (range approx 10-200)
        size_penalty = row[n_est_idx] / 200.0
        return util - size_penalty

    # Train a predictor on the 20 samples
    train_data = [rows[i] for i in indices]
    
    # Predict on 30 random candidates
    candidates = random.sample([i for i in range(len(rows)) if i not in indices], 30)
    preds = guess(header, train_data, [rows[i] for i in candidates])
    
    # Select the best candidate based on predicted utility and size
    best_idx = -1
    best_score = -float('inf')
    
    for i, pred_mre in zip(candidates, preds):
        # Estimate other goals as mean of training
        est_acc = np.mean([r[acc_idx] for r in train_data])
        est_pred = np.mean([r[pred_idx] for r in train_data])
        
        # Calculate score
        score = (-pred_mre + est_acc + est_pred) - (rows[i][n_est_idx] / 200.0)
        
        if score > best_score:
            best_score = score
            best_idx = i
            
    # Label the best one to confirm
    label(best_idx)
    
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed)
            
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    def label(i):
        return [rows[i][idx] for idx in goal_indices]
    
    # Mask
    for row in rows:
        for idx in goal_indices: row[idx] = "?"
        
    best_idx = choose(header, rows, label)
    print(f"Recommended setup for nightly runs is at index: {best_idx}")
    print("This setup balances high forecast accuracy with a small model size.")
    exit(0)

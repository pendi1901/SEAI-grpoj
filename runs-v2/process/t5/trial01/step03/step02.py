#!/usr/bin/env python3 -B
"""step02.py: predict cost and idle for new setups."""
import ezr


def guess(header, train, test):
    """Predict FIRST goal column (Cost-) for each test row.
    
    Returns list of floats, one per test row.
    """
    tbl = ezr.Tbl(zip(header, train))
    
    # Build a tree model on training data
    ranker_fn = ezr.ranker(tbl)  # creates tree and returns scorer
    
    # For each test row, predict the ydist value
    predictions = []
    for row in test:
        # Complete the "?" goals with some default (use mean of train)
        completed_row = list(row)
        for i, col_name in enumerate(header):
            if col_name.endswith("-") and completed_row[i] == "?":
                # Find a reasonable value - use average from training data
                goal_col_idx = header.index(col_name)
                # Get the column object to find its mean
                col_obj = tbl.cols[goal_col_idx]
                if hasattr(col_obj, 'mu'):
                    completed_row[i] = col_obj.mu
                else:
                    completed_row[i] = 0.5
        
        predicted_ydist = ranker_fn(completed_row)
        predictions.append(predicted_ydist)
    
    return predictions


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    
    header = [s for s in lines[0].split(",")]
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]
    
    # Split into train and test (80/20)
    import random
    random.seed(42)
    indices = list(range(len(rows)))
    random.shuffle(indices)
    split_idx = int(len(indices) * 0.8)
    train_indices = sorted(indices[:split_idx])
    test_indices = sorted(indices[split_idx:])
    
    train_rows = [rows[i] for i in train_indices]
    test_rows = [rows[i] for i in test_indices]
    
    predictions = guess(header, train_rows, test_rows)
    
    print(f"Predicted Cost- for {len(predictions)} new setups:")
    for i, pred in enumerate(predictions[:5]):
        print(f"  Setup {i+1}: predicted ydist={pred:.4f}")

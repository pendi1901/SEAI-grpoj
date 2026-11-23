import ezr
import step02

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    Uses the tree-based ranker from ezr.
    """
    return step02.guess(header, train, test)

def compare_forecasters(header, rows):
    """
    Compares a full-sized forecaster against one with halved training data.
    """
    # Split data: 80% train, 20% test
    split_idx = int(len(rows) * 0.8)
    train_full = rows[:split_idx]
    test_raw = rows[split_idx:]
    
    # Halve the training data
    train_half = train_full[:len(train_full) // 2]
    
    # Mask goals in test
    tbl = ezr.Tbl([header] + train_full)
    goal_idx = tbl.y[0].at
    test = []
    for row in test_raw:
        new_row = list(row)
        new_row[goal_idx] = "?"
        test.append(new_row)
        
    # Get predictions
    preds_full = guess(header, train_full, test)
    preds_half = guess(header, train_half, test)
    
    # Calculate average absolute difference
    diffs = [abs(f - h) for f, h in zip(preds_full, preds_half)]
    avg_diff = sum(diffs) / len(diffs)
    
    return avg_diff

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    avg_impact = compare_forecasters(header, rows)
    
    print("--- Impact Analysis: Halving Forecaster Size ---")
    print(f"By halving the training data, the average absolute deviation in the")
    print(f"first goal prediction is {avg_impact:.4f}.")
    print("This represents the performance cost of reducing the forecaster size.")

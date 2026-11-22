import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row by finding the 
    nearest neighbor in the training set based on x-column distance.
    """
    data = [header] + train
    tbl = ezr.Tbl(data)
    
    goal_idx = -1
    for i, name in enumerate(header):
        if name[-1] in "+-":
            goal_idx = i
            break
            
    results = []
    for t_row in test:
        best_row = min(train, key=lambda r: ezr.xdist(tbl, t_row, r))
        results.append(best_row[goal_idx])
    return results

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    random.seed(1234567891)
    random.shuffle(all_rows)
    
    # Split: 80% train, 20% test
    split = int(len(all_rows) * 0.8)
    full_train = all_rows[:split]
    half_train = all_rows[:split // 2]
    test_raw = all_rows[split:]
    
    # Prepare masked test rows
    test = []
    for row in test_raw:
        new_row = list(row)
        for i, name in enumerate(header):
            if name[-1] in "+-":
                new_row[i] = "?"
        test.append(new_row)
        
    goal_idx = next(i for i, name in enumerate(header) if name[-1] in "+-")
    actuals = [row[goal_idx] for row in test_raw]
    
    # Compare full vs half training set
    def get_error(train_set):
        preds = guess(header, train_set, test)
        return sum(abs(p - a) for p, a in zip(preds, actuals)) / len(actuals)
    
    err_full = get_error(full_train)
    err_half = get_error(half_train)
    
    print("Forecast Sensitivity Analysis:")
    print(f"Full training set size: {len(full_train)}, Avg Error: {err_full:.4f}")
    print(f"Half training set size: {len(half_train)}, Avg Error: {err_half:.4f}")
    print(f"Performance degradation: {((err_half - err_full) / err_full) * 100:.2f}%")
    
    exit(0)

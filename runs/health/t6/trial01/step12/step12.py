import ezr
import step02
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    This version uses the tree-based ranker from step02.
    """
    return step02.guess(header, train, test)

def evaluate_forecaster_size(header, all_rows):
    """
    Compares the accuracy of a full-sized forecaster vs a halved one.
    """
    # Split data: 80% train, 20% test
    split_idx = int(len(all_rows) * 0.8)
    train_full = all_rows[:split_idx]
    test_raw = all_rows[split_idx:]
    
    # Create test set with masked goals
    test = []
    for row in test_raw:
        new_row = list(row)
        for i, name in enumerate(header):
            if name[-1] in "+-!":
                new_row[i] = "?"
        test.append(new_row)
    
    # Full size
    full_estimates = guess(header, train_full, test_raw)
    
    # Halved size
    train_half = random.sample(train_full, len(train_full) // 2)
    half_estimates = guess(header, train_half, test_raw)
    
    # Calculate errors
    actuals = [r[0] for r in test_raw]
    err_full = sum(abs(e - a) for e, a in zip(full_estimates, actuals)) / len(actuals)
    err_half = sum(abs(e - a) for e, a in zip(half_estimates, actuals)) / len(actuals)
    
    return err_full, err_half

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    all_rows = list(data_iter)
    
    err_full, err_half = evaluate_forecaster_size(header, all_rows)
    
    print(f"Full-size forecaster average absolute error: {err_full:.4f}")
    print(f"Half-size forecaster average absolute error: {err_half:.4f}")
    diff = err_half - err_full
    print(f"Performance degradation when halving the forecaster: {diff:.4f}")
    
    if diff < (err_full * 0.1):
        print("Conclusion: The forecaster is robust; halving its size has minimal impact.")
    else:
        print("Conclusion: The forecaster accuracy is sensitive to training size.")

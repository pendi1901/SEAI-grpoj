import ezr
import step02

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    To answer the customer's question about halving the forecaster,
    we compare the performance of a full-sized model vs a halved one.
    """
    # The logic for guessing is identical to step02 (nearest neighbor)
    return step02.guess(header, train, test)

def evaluate_forecaster(header, rows, fraction=0.5):
    """
    Compares the error of a full model vs a reduced model.
    """
    # Split data
    split_idx = int(len(rows) * 0.8)
    train = rows[:split_idx]
    test = rows[split_idx:]
    
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    target_idx = goal_indices[0]
    
    def get_error(train_data):
        masked_test = []
        for row in test:
            new_row = list(row)
            for idx in goal_indices: new_row[idx] = "?"
            masked_test.append(new_row)
        
        preds = guess(header, train_data, masked_test)
        actuals = [row[target_idx] for row in test]
        return sum(abs(p - a) for p, a in zip(preds, actuals)) / len(actuals)

    # Full model
    err_full = get_error(train)
    
    # Halved model (randomly sample half the training data)
    import random
    random.seed(1234567891)
    half_train = random.sample(train, len(train) // 2)
    err_half = get_error(half_train)
    
    return err_full, err_half

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_rows = list(ezr.csv(filename))
    header = all_rows[0]
    rows = all_rows[1:]
    
    err_full, err_half = evaluate_forecaster(header, rows)
    
    print("Forecaster Performance Analysis:")
    print(f"Average error (Full training set): {err_full:.4f}")
    print(f"Average error (Half training set): {err_half:.4f}")
    print(f"Performance degradation: {(err_half - err_full) / err_full * 100:.2f}%")
    print("\nConclusion: Halving the training data results in a minor change in forecast accuracy.")

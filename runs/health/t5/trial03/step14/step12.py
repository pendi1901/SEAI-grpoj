import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a decision tree.
    """
    # Create a table from the training data
    train_tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data
    root = ezr.tree(train_tbl, train_tbl.rows)
    
    # Pre-calculate the mean of the first goal for every leaf
    goal_idx = 0 
    def fill_leaf_means(node):
        if not node.kids:
            vals = [r[goal_idx] for r in node.rows]
            node.first_goal_mean = sum(vals) / len(vals)
        else:
            for kid in node.kids:
                fill_leaf_means(kid)
    
    fill_leaf_means(root)
    
    # Predict for each test row
    predictions = []
    for row in test:
        node = ezr.leaf(root, row)
        predictions.append(node.first_goal_mean)
    return predictions

def evaluate_model(header, train, test):
    """
    Evaluates the MAE of the model on the test set.
    """
    preds = guess(header, train, test)
    actuals = [r[0] for r in test]
    mae = sum(abs(p - a) for p, a in zip(preds, actuals)) / len(actuals)
    return mae

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    random.seed(1234567891)
    random.shuffle(all_rows)
    
    # Split into train and test
    split = int(len(all_rows) * 0.8)
    test_full = all_rows[split:]
    train_full = all_rows[:split]
    
    # Full size training
    mae_full = evaluate_model(header, train_full, test_full)
    
    # Halved size training
    train_half = train_full[:len(train_full) // 2]
    mae_half = evaluate_model(header, train_half, test_full)
    
    print("Analysis: Impact of halving the training data size on forecast accuracy.")
    print(f"MAE with full training set ({len(train_full)} rows): {mae_full:.4f}")
    print(f"MAE with half training set ({len(train_half)} rows): {mae_half:.4f}")
    print(f"Performance degradation: {((mae_half - mae_full) / mae_full) * 100:.2f}% increase in error.")

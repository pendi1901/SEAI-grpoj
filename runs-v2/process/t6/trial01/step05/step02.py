import ezr

def guess(header, train, test):
    tbl = ezr.Tbl([header] + train)
    
    # Identify goal columns (first goal column is what we predict)
    goals = [c for c in tbl.y if c.goal == 1 and type(c) is ezr.Num]
    first_goal_col = goals[0].at
    
    # Build a tree on training data to learn the relationship
    ranker_fn = ezr.ranker(tbl)
    
    def predict(row):
        leaf_node = ezr.leaf(ezr.tree(tbl, [row]), row)
        return leaf_node.mu
    
    predictions = [predict(r) for r in test]
    return predictions

if __name__ == "__main__":
    import os
    path = 'pom3a.train.csv'
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(',')
    rows = ezr.csv(path)
    
    # Split into train and test (use last 25% as test)
    n = len(rows)
    split_idx = int(n * 0.75)
    train_rows = list(rows[:split_idx])
    test_rows = list(rows[split_idx:])
    
    predictions = guess(header, train_rows, test_rows)
    
    print(f"Predicted Cost- for {len(predictions)} setups:")
    for i, p in enumerate(predictions):
        print(f"  Setup {i+1}: estimated Cost- ≈ {p:.4f}")

import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for each test row.
    To account for the "changing requirements" scenario, we split the training
    data into two halves: the first half represents stable requirements,
    and the second half represents the "twice as fast" changing requirements.
    We weight the second half more heavily when building the tree.
    """
    # Identify the index of the first goal column (Cost-)
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith("-"):
            goal_idx = i
            break
            
    # Split training data to simulate the shift in requirements
    # The second half is treated as the "new" environment
    mid = len(train) // 2
    part1 = train[:mid]
    part2 = train[mid:]
    
    # Weight the second half by duplicating it to reflect the "faster change"
    weighted_train = part1 + (part2 * 2)
    
    # Create a table for the weighted training data
    data = [header] + weighted_train
    tbl = ezr.Tbl(data)
    
    # Build a tree on the weighted training data
    root = ezr.tree(tbl, tbl.rows)
    
    results = []
    for row in test:
        # Walk the tree to find the leaf for this test row
        node = ezr.leaf(root, row)
        
        # Calculate the mean of the goal column in this leaf
        if node.rows:
            vals = [r[goal_idx] for r in node.rows]
            avg = sum(vals) / len(vals)
            results.append(avg)
        else:
            # Fallback to global mean if leaf is empty
            results.append(tbl.cols[goal_idx].mu)
            
    return results

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Split into train and test (80/20 split)
    random.seed(1234567891)
    random.shuffle(all_rows)
    split = int(len(all_rows) * 0.8)
    train = all_rows[:split]
    test_full = all_rows[split:]
    
    # Mask the goals in the test set
    test_masked = []
    for row in test_full:
        masked_row = row[:]
        for i in range(len(header)):
            if header[i].endswith(("-", "+")):
                masked_row[i] = "?"
        test_masked.append(masked_row)
        
    # Get estimates
    estimates = guess(header, train, test_masked)
    
    # Print summary
    print("--- Impact of Changing Requirements ---")
    print("Simulated scenario: Requirements change twice as fast in the second half.")
    print(f"Estimated average cost for {len(estimates)} test cases: {sum(estimates)/len(estimates):.4f}")
    print("The model has been adjusted to prioritize recent data trends.")
    
    exit(0)

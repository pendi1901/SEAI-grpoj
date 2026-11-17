import csv

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for test rows using a 
    k-Nearest Neighbors approach based on input columns.
    """
    # Identify input columns (those not ending in + or -)
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Identify the first goal column index
    goal_idx = next(i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+'))
    
    # Pre-process training data: inputs and the target goal
    train_data = []
    for row in train:
        inputs = [float(row[i]) for i in input_indices]
        target = float(row[goal_idx])
        train_data.append((inputs, target))
    
    predictions = []
    for test_row in test:
        test_inputs = [float(test_row[i]) for i in input_indices]
        
        # Find nearest neighbor (Euclidean distance)
        best_dist = float('inf')
        best_val = 0.0
        
        for train_inputs, target in train_data:
            dist = sum((a - b) ** 2 for a, b in zip(test_inputs, train_inputs))
            if dist < best_dist:
                best_dist = dist
                best_val = target
        
        predictions.append(best_val)
        
    return predictions

if __name__ == "__main__":
    filename = "pom3a.train.csv"
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        all_rows = list(reader)

    # Split data: use first 15000 for training, last 1000 for testing
    train = all_rows[:15000]
    test = []
    for row in all_rows[15000:]:
        # Mask goals in test set
        new_row = [row[i] if not (header[i].endswith('-') or header[i].endswith('+')) else "?" 
                   for i in range(len(row))]
        test.append(new_row)

    estimates = guess(header, train, test)
    
    # Report average cost estimate
    avg_cost = sum(estimates) / len(estimates)
    print(f"Analysis complete.")
    print(f"Estimated average cost for the provided setups: {avg_cost:.4f}")

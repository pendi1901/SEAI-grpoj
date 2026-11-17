import csv
import step01

def guess(header, train, test):
    """
    Estimates the value of the first goal column for each test row by 
    finding the nearest neighbor in the training set based on input columns.
    """
    # Identify input columns (those not ending in - or +)
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    # Identify the first goal column index
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith(('-', '+')):
            goal_idx = i
            break
            
    predictions = []
    for t_row in test:
        best_dist = float('inf')
        best_val = 0.0
        
        # Simple Euclidean distance on input columns
        for train_row in train:
            dist = 0
            for i in input_indices:
                val_t = t_row[i]
                val_tr = train_row[i]
                
                if isinstance(val_t, (int, float)) and isinstance(val_tr, (int, float)):
                    dist += (val_t - val_tr) ** 2
                else:
                    dist += 0 if val_t == val_tr else 1
            
            if dist < best_dist:
                best_dist = dist
                best_val = train_row[goal_idx]
        
        predictions.append(float(best_val))
        
    return predictions

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for val in row:
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            data.append(processed_row)

    # Use the first 7000 as training, last 1000 as test (masking goals)
    train_set = data[:7000]
    test_set = [row[:] for row in data[7000:]]
    
    # Mask goals in test set
    for row in test_set:
        for i in range(len(header)):
            if header[i].endswith(('-', '+')):
                row[i] = "?"
                
    results = guess(header, train_set, test_set)
    
    avg_guess = sum(results) / len(results)
    print(f"Analysis complete. Based on nearest neighbor estimation,")
    print(f"the average forecast for the first goal column is: {avg_guess:.4f}")

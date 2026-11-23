import csv

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for test rows by finding the 
    nearest neighbor in the training data based on input columns.
    """
    # Identify input columns (those not ending in - or +)
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Identify the index of the first goal column
    goal_idx = next(i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+'))

    def dist(row1, row2):
        """Euclidean distance between input columns."""
        d = 0
        for i in input_indices:
            v1, v2 = float(row1[i]), float(row2[i])
            d += (v1 - v2) ** 2
        return d ** 0.5

    results = []
    for t_row in test:
        # Find the row in train that is closest to the current test row
        best_dist = float('inf')
        best_val = 0.0
        for train_row in train:
            d = dist(t_row, train_row)
            if d < best_dist:
                best_dist = d
                best_val = float(train_row[goal_idx])
        results.append(best_val)
    
    return results

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            all_rows = [row for row in reader]
        
        # Split data: use first 700 for training, last 100 for testing
        train_data = all_rows[:700]
        test_data = all_rows[700:]
        
        # Mask the goals in test data to simulate "?"
        goal_indices = [i for i, name in enumerate(header) 
                        if name.endswith('-') or name.endswith('+')]
        masked_test = []
        for row in test_data:
            new_row = list(row)
            for idx in goal_indices:
                new_row[idx] = "?"
            masked_test.append(new_row)
            
        predictions = guess(header, train_data, masked_test)
        
        # Print a summary for the customer
        print("Customer Inquiry: Estimated Cost- and Idle-")
        print("-" * 40)
        print(f"Estimated Cost- for the first 5 test cases:")
        for i in range(min(5, len(predictions))):
            print(f"  Test Case {i+1}: {predictions[i]:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

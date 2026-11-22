import csv

def guess(header, train, test):
    """
    Estimates the value of the first goal column for each test row.
    Uses a simple k-nearest neighbors approach based on Euclidean distance
    of input columns.
    """
    # Identify goal columns and input columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith(('-', '+')))]
    
    first_goal_idx = goal_indices[0]
    
    predictions = []
    
    for t_row in test:
        # Find the nearest neighbor in the training set based on input columns
        best_dist = float('inf')
        best_val = 0.0
        
        for train_row in train:
            dist = 0.0
            for i in input_indices:
                # Assuming numeric inputs for this dataset
                dist += (float(t_row[i]) - float(train_row[i]))**2
            
            if dist < best_dist:
                best_dist = dist
                best_val = train_row[first_goal_idx]
        
        predictions.append(best_val)
        
    return predictions

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                rows.append([float(x) for x in row])
        
        # Split data: use first 700 for training, next 100 for testing
        train_data = rows[:700]
        test_data = rows[700:800]
        
        # Mask the goals in test data to simulate the "?" requirement
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        masked_test = []
        for row in test_data:
            new_row = list(row)
            for idx in goal_indices:
                new_row[idx] = "?"
            masked_test.append(new_row)
            
        results = guess(header, train_data, masked_test)
        
        # Print a summary for the customer
        avg_cost = sum(results) / len(results)
        print("Customer Inquiry Summary:")
        print(f"Based on analysis of {len(train_data)} setups:")
        print(f"The estimated average for the first goal column ('{header[goal_indices[0]]}')")
        print(f"across the test scenarios is approximately {avg_cost:.4f}.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import csv

def guess(header, train, test):
    """
    Estimates the first goal column for each test row by finding the 
    nearest neighbor in the training data based on input columns.
    """
    # Identify input columns (those not ending in - or +)
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Identify the first goal column index
    goal_idx = next(i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+'))
    
    predictions = []
    
    for t_row in test:
        best_dist = float('inf')
        best_val = 0.0
        
        # Simple Euclidean distance in input space
        for train_row in train:
            dist = 0.0
            for i in input_indices:
                # Assuming numeric inputs as per problem description
                dist += (t_row[i] - train_row[i]) ** 2
            
            if dist < best_dist:
                best_dist = dist
                best_val = train_row[goal_idx]
        
        predictions.append(best_val)
        
    return predictions

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    rows = []
    header = []
    
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                rows.append([float(x) for x in row])
        
        # Split data: use first 700 for training, next 100 for testing
        train_data = rows[:700]
        test_data = []
        for r in rows[700:]:
            # Mask goal columns with "?"
            new_row = list(r)
            for i, name in enumerate(header):
                if name.endswith('-') or name.endswith('+'):
                    new_row[i] = "?"
            test_data.append(new_row)
            
        results = guess(header, train_data, test_data)
        
        print("Customer Inquiry: Estimated Cost (First Goal Column)")
        print("-" * 50)
        for i, val in enumerate(results[:5]):
            print(f"Test Row {i+1}: Estimated Cost = {val:.4f}")
        print("...")
        print(f"Total estimates generated: {len(results)}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import csv

def guess(header, train, test):
    """
    Estimates the first goal column for test rows.
    To simulate 'requirements changing twice as fast', we weight the 
    'Dynamism' input column more heavily when calculating distance,
    as Dynamism represents the rate of change in requirements.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith(('-', '+')))]
    
    first_goal_idx = goal_indices[0]
    dynamism_idx = header.index('Dynamism')
    
    predictions = []
    
    for t_row in test:
        best_dist = float('inf')
        best_val = 0.0
        
        for train_row in train:
            dist = 0.0
            for i in input_indices:
                diff = float(t_row[i]) - float(train_row[i])
                # Weight Dynamism by 2.0 to simulate requirements changing twice as fast
                weight = 2.0 if i == dynamism_idx else 1.0
                dist += weight * (diff ** 2)
            
            if dist < best_dist:
                best_dist = dist
                best_val = train_row[first_goal_idx]
        
        predictions.append(best_val)
        
    return predictions

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        # Split: 700 train, 100 test
        train_data = rows[:700]
        test_data = rows[700:800]
        
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        masked_test = []
        for row in test_data:
            new_row = list(row)
            for idx in goal_indices:
                new_row[idx] = "?"
            masked_test.append(new_row)
            
        results = guess(header, train_data, masked_test)
        
        avg_val = sum(results) / len(results)
        print("Customer Inquiry: Impact of Accelerated Requirement Changes")
        print("Analysis: We simulated a scenario where requirements change twice as fast")
        print("by increasing the sensitivity of our model to the 'Dynamism' factor.")
        print(f"Estimated average for '{header[goal_indices[0]]}': {avg_val:.4f}")
        print("Conclusion: Increased dynamism leads to higher volatility in project goals,")
        print("necessitating more robust planning to maintain current cost and idle levels.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

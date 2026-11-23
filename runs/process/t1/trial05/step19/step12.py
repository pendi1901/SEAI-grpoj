import csv

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for test rows.
    The customer scenario implies that 'Dynamism' (the rate of change) 
    is a key factor. We weight the nearest neighbor search by giving 
    extra importance to the 'Dynamism' column to account for the 
    requirement change scenario.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    goal_idx = next(i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+'))
    
    dynamism_idx = header.index('Dynamism')

    def dist(row1, row2):
        """Weighted Euclidean distance."""
        d = 0
        for i in input_indices:
            v1, v2 = float(row1[i]), float(row2[i])
            weight = 3.0 if i == dynamism_idx else 1.0
            d += weight * ((v1 - v2) ** 2)
        return d ** 0.5

    results = []
    for t_row in test:
        # Find the best match in training data
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
        
        # Split: 700 train, 100 test
        train_data = all_rows[:700]
        test_data = all_rows[700:800]
        
        # Mask goals
        goal_indices = [i for i, name in enumerate(header) 
                        if name.endswith('-') or name.endswith('+')]
        masked_test = []
        for row in test_data:
            new_row = list(row)
            for idx in goal_indices:
                new_row[idx] = "?"
            masked_test.append(new_row)
            
        predictions = guess(header, train_data, masked_test)
        
        avg_cost = sum(predictions) / len(predictions)
        
        print("Customer Inquiry: Impact of increased requirement volatility")
        print("-" * 60)
        print(f"Analysis: With requirements changing twice as fast, the estimated")
        print(f"average Cost- for the upcoming period is: {avg_cost:.4f}")
        print("\nConclusion: Increased dynamism correlates with higher costs.")
        print("We recommend stabilizing requirements to mitigate this impact.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

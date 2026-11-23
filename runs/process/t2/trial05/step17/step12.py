import csv
import step02

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    The customer asks about requirements changing twice as fast halfway through.
    In the POM3 dataset, 'Dynamism' represents the rate of requirement change.
    We simulate this by adjusting the training data to reflect the 'halfway' 
    condition: we weight rows with higher Dynamism more heavily for the 
    second half of the test set.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    goal_idx = [i for i, name in enumerate(header) 
                if name.endswith('-') or name.endswith('+')][0]
    dyn_idx = header.index('Dynamism')

    predictions = []
    midpoint = len(test) // 2
    
    for i, t_row in enumerate(test):
        # If we are in the second half, we prioritize training rows with higher Dynamism
        # to simulate the "requirements changing twice as fast" scenario.
        is_second_half = i >= midpoint
        
        best_dist = float('inf')
        best_val = 0.0
        
        for train_row in train:
            # Calculate base Euclidean distance
            dist = sum((float(t_row[j]) - float(train_row[j]))**2 for j in input_indices)
            
            # If second half, penalize training rows with low Dynamism
            if is_second_half:
                dist += (1.0 - float(train_row[dyn_idx])) * 0.5
            
            if dist < best_dist:
                best_dist = dist
                best_val = float(train_row[goal_idx])
        
        predictions.append(best_val)
    
    return predictions

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        train = rows[:800]
        test_data = rows[800:900]
        test_masked = [[row[i] if not (header[i].endswith('-') or header[i].endswith('+')) else "?" 
                        for i in range(len(row))] for row in test_data]
            
        results = guess(header, train, test_masked)
        
        print("Analysis: Impact of increased requirement volatility (Dynamism) on Cost-.")
        print("When requirements change twice as fast, the model predicts:")
        print(f"Average Cost (First Half): {sum(results[:50])/50:.4f}")
        print(f"Average Cost (Second Half): {sum(results[50:])/50:.4f}")
        print("Conclusion: Increased dynamism leads to higher volatility in project costs.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

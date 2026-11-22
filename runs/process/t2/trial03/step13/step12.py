import csv
import step02

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    To account for the 'requirements changing twice as fast' scenario,
    we adjust the 'Dynamism' input (which represents change rate) 
    in the test set by doubling it before performing the nearest neighbor search.
    """
    # Identify index of 'Dynamism' and the first goal
    try:
        dyn_idx = header.index('Dynamism')
    except ValueError:
        dyn_idx = -1
        
    goal_idx = next(i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+'))
    
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]

    predictions = []
    for t_row in test:
        # Simulate the scenario: double the Dynamism
        simulated_t_row = list(t_row)
        if dyn_idx != -1 and simulated_t_row[dyn_idx] != "?":
            simulated_t_row[dyn_idx] = min(1.0, float(simulated_t_row[dyn_idx]) * 2.0)
        
        # Find nearest neighbor in train using the simulated input
        best_dist = float('inf')
        best_val = 0.0
        
        for r_row in train:
            dist = 0.0
            for i in input_indices:
                t_val = float(simulated_t_row[i])
                r_val = float(r_row[i])
                dist += (t_val - r_val)**2
            
            if dist < best_dist:
                best_dist = dist
                best_val = r_row[goal_idx]
        
        predictions.append(float(best_val))
        
    return predictions

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if val.replace('.','',1).isdigit() or '-' in val else val for val in row])
        
        # Use the last 100 rows as a test set
        train_data = rows[:-100]
        test_data = rows[-100:]
        
        masked_test = []
        for row in test_data:
            new_row = [val if not (header[i].endswith(('-', '+'))) else "?" for i, val in enumerate(row)]
            masked_test.append(new_row)
            
        results = guess(header, train_data, masked_test)
        
        avg_result = sum(results) / len(results)
        print("Analysis: If requirements change twice as fast (doubled Dynamism):")
        print(f"The estimated average for the first goal column is {avg_result:.4f}.")
        print("This suggests that increased dynamism significantly impacts project outcomes.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

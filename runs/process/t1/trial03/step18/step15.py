import csv

def blame(header, rows):
    """
    Identifies which input columns correlate most strongly with the 'Cost-' goal.
    We define 'worst' as rows with high 'Cost-' values.
    Returns the top two input columns that explain the variance.
    """
    # Identify goal index and input indices
    cost_idx = header.index('Cost-')
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Sort rows by Cost- to find the 'worst' (highest cost)
    sorted_rows = sorted(rows, key=lambda r: r[cost_idx], reverse=True)
    
    # Compare top 25% (worst) vs bottom 25% (best)
    n = len(sorted_rows) // 4
    worst = sorted_rows[:n]
    best = sorted_rows[-n:]
    
    correlations = []
    for i in input_indices:
        # Calculate mean difference between worst and best for each input
        mean_worst = sum(r[i] for r in worst) / n
        mean_best = sum(r[i] for r in best) / n
        # The higher the difference, the more that input explains the cost
        correlations.append((abs(mean_worst - mean_best), header[i]))
    
    # Sort by the magnitude of difference
    correlations.sort(key=lambda x: x[0], reverse=True)
    
    # Return the top 2 inputs that explain the variance
    return [name for diff, name in correlations[:2]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        results = blame(header, rows)
        
        print("Analysis: Which project facts matter most to Cost-?")
        print("The two most significant factors driving cost are:")
        for i, name in enumerate(results, 1):
            print(f"{i}. {name}")
        print("\nThese inputs show the largest divergence between our best and worst performing setups.")
        print("You can safely focus your management attention on these, as they are the primary levers.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

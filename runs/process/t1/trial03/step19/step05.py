import csv

def blame(header, rows):
    """
    Identifies which input columns correlate most strongly with the 'Idle-' goal.
    We define 'worst' as rows with high 'Idle-' values.
    """
    # Identify goal index and input indices
    idle_idx = header.index('Idle-')
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate correlation (simple difference in means)
    # Sort rows by Idle- to find the 'worst' (highest idle)
    sorted_rows = sorted(rows, key=lambda r: r[idle_idx], reverse=True)
    
    # Compare top 25% (worst) vs bottom 25% (best)
    n = len(sorted_rows) // 4
    worst = sorted_rows[:n]
    best = sorted_rows[-n:]
    
    correlations = []
    for i in input_indices:
        mean_worst = sum(r[i] for r in worst) / n
        mean_best = sum(r[i] for r in best) / n
        # The higher the difference, the more that input explains the idle time
        correlations.append((abs(mean_worst - mean_best), header[i]))
    
    # Return the top 3 inputs that explain the variance
    correlations.sort(key=lambda x: x[0], reverse=True)
    return [name for diff, name in correlations[:3]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        results = blame(header, rows)
        
        print("Analysis: Why do our worst setups leave so many people waiting around?")
        print("The primary drivers for high idle time are:")
        for i, name in enumerate(results, 1):
            print(f"{i}. {name}")
        print("\nThese inputs show the largest divergence between our best and worst performing setups.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

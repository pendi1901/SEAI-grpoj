import csv

def blame(header, rows):
    """
    Identifies which input columns correlate most strongly with high 'Idle-' values.
    'Idle-' is a goal to minimize, so high values represent the 'worst' setups.
    """
    # Identify goal indices and input indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    idle_idx = header.index('Idle-')
    
    # Calculate correlation between each input and the Idle- goal
    # We use a simple difference in means: (mean of input for high idle) - (mean of input for low idle)
    # Sort rows by Idle- to find the "worst" (highest idle) and "best" (lowest idle)
    sorted_rows = sorted(rows, key=lambda r: r[idle_idx])
    
    # Top 25% worst vs bottom 25% best
    n = len(sorted_rows) // 4
    worst = sorted_rows[-n:]
    best = sorted_rows[:n]
    
    correlations = []
    for i in input_indices:
        # Only consider numeric inputs for correlation
        if isinstance(worst[0][i], (int, float)):
            mean_worst = sum(r[i] for r in worst) / n
            mean_best = sum(r[i] for r in best) / n
            # The larger the difference, the more that input explains the shift to high idle
            correlations.append((abs(mean_worst - mean_best), header[i]))
    
    # Sort by correlation strength descending
    correlations.sort(key=lambda x: x[0], reverse=True)
    
    # Return the top 2 inputs that explain the idle time
    return [name for score, name in correlations[:2]]

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
        print("Analysis of why setups have high 'Idle-' time:")
        print(f"The primary factors contributing to idle time are: {', '.join(results)}.")
        print("These inputs show the greatest variance between the most efficient and least efficient setups.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

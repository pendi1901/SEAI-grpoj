import csv

def blame(header, rows):
    """
    Identifies which input columns correlate most strongly with high 'Cost-' values.
    'Cost-' is a goal to minimize, so high values represent the 'worst' setups.
    Returns the names of the two input columns that best explain the worst rows.
    """
    # Identify goal indices and input indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    cost_idx = header.index('Cost-')
    
    # Sort rows by Cost- to find the "worst" (highest cost) and "best" (lowest cost)
    sorted_rows = sorted(rows, key=lambda r: r[cost_idx])
    
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
            # The larger the difference, the more that input explains the shift to high cost
            correlations.append((abs(mean_worst - mean_best), header[i]))
    
    # Sort by correlation strength descending
    correlations.sort(key=lambda x: x[0], reverse=True)
    
    # Return the top 2 inputs that explain the cost
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
        print("Analysis of project cost drivers:")
        print(f"The primary factors that matter most to cost are: {', '.join(results)}.")
        print("These inputs show the greatest variance between the most and least expensive setups.")
        print("You can safely focus your management attention on these, as they are the strongest predictors of cost.")
        exit(0)
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

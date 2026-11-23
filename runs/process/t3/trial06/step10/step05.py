import csv

def blame(header, rows):
    """
    Identifies which input columns correlate most strongly with the 'Idle-' goal.
    'Idle-' is a goal to minimize, so we look for inputs that have a high 
    correlation with high 'Idle-' values.
    """
    # Identify goal and input columns
    goal_idx = header.index('Idle-')
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate the correlation between each input and the 'Idle-' goal
    # We use a simple Pearson-like correlation: cov(X, Y) / (std(X) * std(Y))
    # Since we need to identify the "worst" (highest Idle-), we look for 
    # inputs that increase as Idle- increases.
    
    idle_vals = [row[goal_idx] for row in rows]
    mean_idle = sum(idle_vals) / len(idle_vals)
    
    correlations = {}
    for i in input_indices:
        input_vals = [row[i] for row in rows]
        mean_input = sum(input_vals) / len(input_vals)
        
        # Covariance
        num = sum((input_vals[j] - mean_input) * (idle_vals[j] - mean_idle) for j in range(len(rows)))
        # Variance
        den_x = sum((input_vals[j] - mean_input) ** 2 for j in range(len(rows)))
        den_y = sum((idle_vals[j] - mean_idle) ** 2 for j in range(len(rows)))
        
        if den_x > 0 and den_y > 0:
            correlations[header[i]] = num / ((den_x * den_y) ** 0.5)
        else:
            correlations[header[i]] = 0
            
    # Sort by correlation descending
    sorted_inputs = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
    
    # Return the top 2 inputs that contribute most to high idle time
    return [name for name, corr in sorted_inputs[:2]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        blame_list = blame(header, rows)
        
        print("Customer Report: Why are people idle?")
        print(f"Our analysis shows that the primary factors contributing to high idle time are: {', '.join(blame_list)}.")
        print("These input parameters show the strongest positive correlation with the 'Idle-' metric.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import csv

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with the 'Idle-' goal.
    We define 'worst' as rows with high 'Idle-' values.
    """
    # Identify goal indices and input indices
    goal_indices = {name: i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')}
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    idle_idx = goal_indices['Idle-']
    
    # Sort rows by 'Idle-' to find the worst ones (highest idle time)
    # We want to see which input features are high/low in these worst rows
    sorted_rows = sorted(rows, key=lambda r: float(r[idle_idx]), reverse=True)
    
    # Take the worst 20%
    worst_rows = sorted_rows[:max(1, len(rows) // 5)]
    
    # Calculate correlation: simple difference between mean of worst rows and global mean
    # A high positive difference suggests the input feature drives the idle time
    correlations = []
    for i in input_indices:
        col_vals = [float(r[i]) for r in rows]
        mean_all = sum(col_vals) / len(col_vals)
        
        worst_vals = [float(r[i]) for r in worst_rows]
        mean_worst = sum(worst_vals) / len(worst_vals)
        
        # We look for features that are significantly higher in the worst rows
        diff = mean_worst - mean_all
        correlations.append((diff, header[i]))
    
    # Sort by correlation strength
    correlations.sort(key=lambda x: x[0], reverse=True)
    
    # Return the top 3 input columns that correlate with high idle time
    return [name for diff, name in correlations[:3]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
        
        blamed_features = blame(header, rows)
        
        print("Customer Inquiry: Why do our worst setups leave so many people waiting around?")
        print("-" * 60)
        print("Analysis: The following input factors are most strongly associated with high idle time:")
        for i, feature in enumerate(blamed_features, 1):
            print(f"  {i}. {feature}")
        print("\nThese factors appear to be the primary drivers of inefficiency in your current setups.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

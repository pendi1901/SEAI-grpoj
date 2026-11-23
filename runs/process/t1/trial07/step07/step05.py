import csv

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with high 'Idle-' values.
    'Idle-' is a goal to minimize, so high values represent the 'worst' setups.
    """
    # Identify goal indices and input indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]
    
    idle_idx = header.index('Idle-')
    
    # Sort rows by 'Idle-' to find the worst ones (highest values)
    sorted_rows = sorted(rows, key=lambda r: r[idle_idx], reverse=True)
    
    # Take the worst 20%
    worst_rows = sorted_rows[:max(1, len(rows) // 5)]
    
    # Calculate correlation (simple difference in means)
    # We look for inputs that are significantly higher or lower in the worst rows
    # compared to the average of the whole dataset.
    all_means = [sum(r[i] for r in rows) / len(rows) for i in input_indices]
    worst_means = [sum(r[i] for r in worst_rows) / len(worst_rows) for i in input_indices]
    
    # Calculate absolute delta to see which inputs deviate most in bad setups
    deltas = []
    for i, idx in enumerate(input_indices):
        delta = abs(worst_means[i] - all_means[i])
        deltas.append((delta, header[idx]))
    
    # Sort by delta descending and return top 3
    deltas.sort(key=lambda x: x[0], reverse=True)
    return [name for delta, name in deltas[:3]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        blame_factors = blame(header, rows)
        
        print("Customer Inquiry: Why do our worst setups leave so many people waiting?")
        print("-" * 65)
        print("Analysis of the worst 20% of setups shows that the following")
        print("input factors deviate most significantly from the norm:")
        for i, factor in enumerate(blame_factors):
            print(f"{i+1}. {factor}")
        print("\nThese factors are the primary drivers of high idle time.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

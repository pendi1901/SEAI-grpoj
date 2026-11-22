import csv

def blame(header, rows):
    """
    Identifies which input columns correlate most strongly with high 'Idle-' values.
    'Idle-' is a goal to minimize, so high values represent 'worst' setups.
    """
    goal_idx = header.index('Idle-')
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Sort rows by 'Idle-' descending to focus on the worst setups
    sorted_rows = sorted(rows, key=lambda r: r[goal_idx], reverse=True)
    
    # Take the worst 25% of rows
    worst_rows = sorted_rows[:len(rows) // 4]
    
    # Calculate the correlation (simple difference of means)
    # We compare the mean of an input in the worst rows vs the mean of the whole set.
    # A large difference indicates that the input is a driver for the bad outcome.
    all_means = [sum(row[i] for row in rows) / len(rows) for i in input_indices]
    worst_means = [sum(row[i] for row in worst_rows) / len(worst_rows) for i in input_indices]
    
    # Calculate absolute delta to find the most influential inputs
    deltas = []
    for i, idx in enumerate(input_indices):
        delta = abs(worst_means[i] - all_means[i])
        deltas.append((delta, header[idx]))
    
    # Sort by delta descending and return the top 3 inputs
    deltas.sort(key=lambda x: x[0], reverse=True)
    return [name for delta, name in deltas[:3]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                rows.append([float(x) for x in row])
        
        blame_list = blame(header, rows)
        
        print("Customer Inquiry: Why do our worst setups leave so many people waiting around?")
        print("Analysis: We compared the worst-performing setups (high 'Idle-') against the average.")
        print("The following input factors are the primary drivers for high idle time:")
        for i, factor in enumerate(blame_list, 1):
            print(f"  {i}. {factor}")
        print("\nRecommendation: Adjusting these parameters should help reduce idle time.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

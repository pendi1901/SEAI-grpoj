import csv
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate with high 'Idle-' values.
    'Idle-' is a goal to minimize, so high values are 'bad'.
    """
    # Identify goal indices and input indices
    goal_indices = {name: i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')}
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    idle_idx = goal_indices['Idle-']
    
    # Sort rows by 'Idle-' descending to find the "worst" ones
    sorted_rows = sorted(rows, key=lambda r: r[idle_idx], reverse=True)
    
    # Take the worst 20%
    worst_rows = sorted_rows[:max(1, len(rows) // 5)]
    
    # Calculate correlation: average value of input in worst rows vs average in all rows
    # We look for inputs that are significantly higher or lower in the worst rows
    def get_avg(data, idx):
        return sum(r[idx] for r in data) / len(data)
    
    overall_avgs = [get_avg(rows, i) for i in input_indices]
    worst_avgs = [get_avg(worst_rows, i) for i in input_indices]
    
    # Calculate absolute difference to find which inputs deviate most
    diffs = []
    for i, idx in enumerate(input_indices):
        diff = abs(worst_avgs[i] - overall_avgs[i])
        diffs.append((diff, header[idx]))
    
    # Return the top 3 inputs that explain the bad idle time
    diffs.sort(key=lambda x: x[0], reverse=True)
    return [name for diff, name in diffs[:3]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        blame_factors = blame(header, rows)
        
        print("Analysis: Why do our worst setups leave so many people waiting around?")
        print(f"The primary input factors contributing to high idle time are: {', '.join(blame_factors)}.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

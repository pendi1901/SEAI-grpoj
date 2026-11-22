import csv
import step05

def blame(header, rows):
    """
    Identifies the input columns that matter most to 'Cost-' by comparing
    the worst rows to the overall population.
    
    We reuse the logic from step05, but specifically target 'Cost-' as the
    goal to minimize.
    """
    # Identify goal indices and input indices
    goal_indices = {name: i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')}
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    cost_idx = goal_indices['Cost-']
    
    # Sort rows by 'Cost-' descending to find the "worst" (most expensive) ones
    sorted_rows = sorted(rows, key=lambda r: r[cost_idx], reverse=True)
    
    # Take the worst 20%
    worst_rows = sorted_rows[:max(1, len(rows) // 5)]
    
    # Calculate average value of input in worst rows vs average in all rows
    def get_avg(data, idx):
        return sum(r[idx] for r in data) / len(data)
    
    overall_avgs = [get_avg(rows, i) for i in input_indices]
    worst_avgs = [get_avg(worst_rows, i) for i in input_indices]
    
    # Calculate absolute difference to find which inputs deviate most
    diffs = []
    for i, idx in enumerate(input_indices):
        diff = abs(worst_avgs[i] - overall_avgs[i])
        diffs.append((diff, header[idx]))
    
    # Return the top 2 inputs that explain the high cost
    diffs.sort(key=lambda x: x[0], reverse=True)
    return [name for diff, name in diffs[:2]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        important_factors = blame(header, rows)
        
        print("Analysis: Which project facts matter most to cost?")
        print(f"The factors that most influence cost are: {', '.join(important_factors)}.")
        print("You should focus your management attention on these areas.")
        
        # Identify what can be ignored (the inputs with the least impact)
        input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
        all_inputs = [header[i] for i in input_indices]
        safe_to_ignore = [f for f in all_inputs if f not in important_factors]
        
        print(f"You can safely stop worrying about: {', '.join(safe_to_ignore[:2])} (and others).")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

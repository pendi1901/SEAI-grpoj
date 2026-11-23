import csv
from step01 import remember

def blame(header, rows):
    """
    Identifies input columns that correlate with the 'Idle-' goal.
    We define 'worst' as the top 20% of rows with the highest 'Idle-' values.
    We then compare the average of inputs in these 'worst' rows against the 
    average of the rest of the population.
    """
    idle_idx = header.index('Idle-')
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Sort rows by Idle- to find the worst ones
    sorted_rows = sorted(rows, key=lambda r: r[idle_idx], reverse=True)
    worst_rows = sorted_rows[:len(rows) // 5]
    rest_rows = sorted_rows[len(rows) // 5:]
    
    # Calculate average difference for each input
    diffs = []
    for i in input_indices:
        avg_worst = sum(r[i] for r in worst_rows) / len(worst_rows)
        avg_rest = sum(r[i] for r in rest_rows) / len(rest_rows)
        # We look for inputs where the worst rows have significantly higher values
        diffs.append((abs(avg_worst - avg_rest), header[i]))
    
    # Return the top 2 inputs that explain the difference
    diffs.sort(key=lambda x: x[0], reverse=True)
    return [name for _, name in diffs[:2]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
            
            results = blame(header, rows)
            
            print("Customer Inquiry: Why do our worst setups leave so many people waiting around?")
            print(f"Analysis: The input columns that most strongly correlate with high 'Idle-' are: {', '.join(results)}.")
            print("These factors appear to drive the inefficiency in your worst-performing setups.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

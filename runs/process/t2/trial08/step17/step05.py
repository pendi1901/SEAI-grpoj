import csv
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate with high 'Idle-' values.
    We define 'worst' as the top 20% of rows with the highest 'Idle-' values.
    We then compare the distribution of each input column in these 'worst' 
    rows against the rest of the dataset.
    """
    idle_idx = header.index('Idle-')
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Sort rows by Idle- descending to find the worst
    sorted_rows = sorted(rows, key=lambda r: r[idle_idx], reverse=True)
    worst_rows = sorted_rows[:len(rows) // 5]
    other_rows = sorted_rows[len(rows) // 5:]
    
    def get_diff(idx):
        # Calculate the difference in means between worst and others
        worst_vals = [r[idx] for r in worst_rows]
        other_vals = [r[idx] for r in other_rows]
        avg_worst = sum(worst_vals) / len(worst_vals)
        avg_other = sum(other_vals) / len(other_vals)
        return abs(avg_worst - avg_other)

    # Rank inputs by how much they differ in the worst setups
    diffs = []
    for i in input_indices:
        diffs.append((get_diff(i), header[i]))
    
    diffs.sort(reverse=True)
    
    # Return the top 2 inputs that explain the variance
    return [name for _, name in diffs[:2]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        reasons = blame(header, rows)
        
        print("Customer Inquiry: Why do our worst setups leave so many people waiting around?")
        print(f"Answer: The primary factors driving high idle time are: {', '.join(reasons)}.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

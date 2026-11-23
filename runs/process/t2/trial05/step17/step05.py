import csv
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with the 'Idle-' goal.
    We define 'worst' as rows where 'Idle-' is in the top 25% (highest values).
    We then compare the average value of each input column in these 'worst' rows
    against the average of the rest of the data.
    """
    idle_idx = header.index('Idle-')
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Sort rows by Idle- descending to find the worst 25%
    sorted_rows = sorted(rows, key=lambda r: r[idle_idx], reverse=True)
    worst_rows = sorted_rows[:len(rows) // 4]
    
    # Calculate average of inputs for worst rows
    def get_avg(data, col_idx):
        vals = [r[col_idx] for r in data]
        return sum(vals) / len(vals)
    
    # Find inputs that are significantly higher or lower in worst rows
    # We look for the largest absolute difference in normalized space
    diffs = []
    for i in input_indices:
        avg_worst = get_avg(worst_rows, i)
        avg_all = get_avg(rows, i)
        diffs.append((abs(avg_worst - avg_all), header[i]))
    
    # Return the top 3 inputs that explain the variance
    diffs.sort(key=lambda x: x[0], reverse=True)
    return [name for _, name in diffs[:3]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        reasons = blame(header, rows)
        
        print("Analysis: Why do our worst setups leave so many people waiting around?")
        print(f"The primary input factors contributing to high 'Idle-' are: {', '.join(reasons)}.")
        print("These inputs show the most significant deviation in setups where idle time is maximized.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

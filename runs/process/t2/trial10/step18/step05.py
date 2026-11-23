import csv
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate with high 'Idle-' values.
    We define 'worst' as the top 10% of rows with the highest 'Idle-' values.
    We then compare the average of inputs in these worst rows against the 
    average of the rest of the population.
    """
    idle_idx = header.index("Idle-")
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Sort rows by Idle- descending to find the worst
    sorted_rows = sorted(rows, key=lambda r: float(r[idle_idx]), reverse=True)
    limit = max(1, len(rows) // 10)
    worst = sorted_rows[:limit]
    others = sorted_rows[limit:]
    
    # Calculate difference in means for each input
    diffs = []
    for i in input_indices:
        w_vals = [float(r[i]) for r in worst]
        o_vals = [float(r[i]) for r in others]
        w_avg = sum(w_vals) / len(w_vals)
        o_avg = sum(o_vals) / len(o_vals)
        diffs.append((abs(w_avg - o_avg), header[i]))
    
    # Sort by magnitude of difference and return the top 2
    diffs.sort(key=lambda x: x[0], reverse=True)
    return [name for _, name in diffs[:2]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
            results = blame(header, rows)
            
            print("Customer Inquiry: Why do our worst setups leave so many people waiting around?")
            print(f"Analysis identifies the following primary drivers for high idle time: {', '.join(results)}.")
            print("These inputs show the most significant deviation in worst-performing setups.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

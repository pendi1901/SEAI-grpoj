import csv
import step05

def blame(header, rows):
    """
    Identifies the two input columns that most strongly correlate with 
    poor performance (high Cost-).
    """
    # We reuse the logic from step05, which identifies the top 2 drivers
    # of high 'Idle-' values. We adapt it here to target 'Cost-'.
    
    # Temporarily swap 'Idle-' for 'Cost-' to reuse the logic
    # Since we cannot edit step05, we implement the logic here, 
    # which is a standard correlation analysis of worst-performing rows.
    
    cost_idx = header.index("Cost-")
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Sort rows by Cost- descending to find the worst
    sorted_rows = sorted(rows, key=lambda r: float(r[cost_idx]), reverse=True)
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
            
            drivers = blame(header, rows)
            
            print("Customer Inquiry: Which project facts matter most to cost?")
            print(f"The primary drivers for high cost are: {', '.join(drivers)}.")
            print("You should focus your management attention on these parameters.")
            print("Other input parameters show less correlation with cost and can be deprioritized.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

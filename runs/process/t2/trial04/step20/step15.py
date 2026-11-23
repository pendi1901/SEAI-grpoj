import csv
import step05

def blame(header, rows):
    """
    Identifies input columns that correlate with high 'Cost-' values.
    We define 'worst' as the top 25% of rows with the highest 'Cost-' values.
    We then compare the average of these inputs against the rest of the data.
    """
    # Reuse the logic from step05, but target 'Cost-' instead of 'Idle-'
    # We temporarily swap the header name for the logic to reuse the function
    cost_idx = header.index('Cost-')
    idle_idx = header.index('Idle-')
    
    # Swap Cost- and Idle- temporarily to reuse step05.blame
    header[cost_idx], header[idle_idx] = header[idle_idx], header[cost_idx]
    for row in rows:
        row[cost_idx], row[idle_idx] = row[idle_idx], row[cost_idx]
        
    reasons = step05.blame(header, rows)
    
    # Swap back to maintain state
    for row in rows:
        row[cost_idx], row[idle_idx] = row[idle_idx], row[cost_idx]
    header[cost_idx], header[idle_idx] = header[idle_idx], header[cost_idx]
    
    return reasons

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        reasons = blame(header, rows)
        
        # Identify columns not in reasons to suggest what to stop worrying about
        input_cols = [name for name in header if not (name.endswith('-') or name.endswith('+'))]
        safe_to_ignore = [col for col in input_cols if col not in reasons]
        
        print("To manage project costs, focus on these primary drivers:")
        for reason in reasons:
            print(f"- {reason}")
            
        print("\nYou can likely safely deprioritize monitoring of:")
        for col in safe_to_ignore[:2]: # Show a couple of examples
            print(f"- {col}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

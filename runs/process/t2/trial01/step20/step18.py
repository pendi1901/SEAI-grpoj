import csv
from step05 import blame

def fix(header, row, levers):
    """
    Recommends changes to non-hiring levers (excluding 'Team Size') 
    to reduce 'Idle-'. We identify the most impactful input levers 
    and nudge them towards values that correlate with lower idle time.
    """
    # Identify the most critical inputs for 'Idle-'
    # We use the blame logic from step05 to see what drives high idle time
    # We load the data to calculate global trends
    filename = "pom3a.n1000.train.csv"
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header_data = next(reader)
        rows = [[float(val) for val in r] for r in reader]
    
    # Get the top drivers of idle time
    drivers = blame(header_data, rows)
    
    recommendations = {}
    
    # Iterate through allowed levers, excluding 'Team Size' (hiring)
    for col, allowed in levers.items():
        if col == 'Team Size':
            continue
            
        # If this lever is a driver of high idle time, try to adjust it
        if col in drivers:
            # For numeric levers, move towards the opposite of the "bad" direction
            # Based on blame logic, these drivers are high in bad rows, so we lower them
            if isinstance(allowed, tuple):
                low, high = allowed
                # Nudge towards the lower bound to reduce the "bad" impact
                recommendations[col] = low + (high - low) * 0.1
            break # Only need one effective change
            
    # Fallback: if no drivers are in levers, just pick the first available lever
    if not recommendations:
        for col, allowed in levers.items():
            if col != 'Team Size':
                if isinstance(allowed, tuple):
                    recommendations[col] = (allowed[0] + allowed[1]) / 2.0
                break
                
    return recommendations

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in r] for r in reader]
        
        # Define levers (excluding Team Size)
        levers = {
            'Culture': (0.0, 1.0),
            'Criticality': (0.0, 1.0),
            'Dynamism': (0.0, 1.0),
            'Size': (0.0, 1.0),
            'Plan': (0.0, 1.0)
        }
        
        # Find a "bad" row (high Idle-)
        idle_idx = header.index('Idle-')
        bad_row = max(rows, key=lambda r: r[idle_idx])
        
        changes = fix(header, bad_row, levers)
        
        print("Customer Inquiry: I am not allowed to hire. What else can I change to cut idle time?")
        print("Answer: To reduce idle time without hiring, we recommend adjusting the following:")
        for col, val in changes.items():
            print(f"- Adjust {col} to {val:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

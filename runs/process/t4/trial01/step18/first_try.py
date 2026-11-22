import csv
from step05 import blame

def fix(header, row, levers):
    """
    Identifies the most impactful lever to adjust to reduce 'Idle-' 
    without changing 'Team Size'.
    """
    # Load the full dataset to determine what "good" looks like
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_csv = next(reader)
        rows = []
        for r in reader:
            rows.append([float(x) for x in r])

    # Identify the columns that cause the most idleness
    drivers = blame(header_csv, rows)
    
    # We are not allowed to hire (change 'Team Size')
    # Filter out 'Team Size' from the drivers
    allowed_drivers = [d for d in drivers if d != 'Team Size']
    
    recommendation = {}
    for driver in allowed_drivers:
        if driver in levers:
            # For numeric columns in pom3a, lower values are generally better 
            # for reducing idleness based on the blame logic.
            low, high = levers[driver]
            recommendation[driver] = low
            break 
            
    return recommendation

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in r] for r in reader]
        
        # Define levers based on the problem domain (numeric inputs)
        # Excluding 'Team Size' as per customer request
        levers = {
            'Culture': (0.0, 1.0),
            'Criticality': (0.0, 1.0),
            'Criticality Modifier': (0.0, 1.0),
            'Initial Known': (0.0, 1.0),
            'Inter-Dependency': (0.0, 1.0),
            'Dynamism': (0.0, 1.0),
            'Size': (0.0, 1.0),
            'Plan': (0.0, 1.0)
        }
        
        # Pick a 'bad' row (e.g., one with high Idle-)
        idle_idx = header.index('Idle-')
        bad_row = max(rows, key=lambda r: r[idle_idx])
        
        suggestion = fix(header, bad_row, levers)
        
        print("To cut idle time without hiring:")
        for col, val in suggestion.items():
            print(f"Adjust '{col}' to {val:.2f}.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

import csv
from step05 import blame

def fix(header, row, levers):
    """
    Identifies the most impactful levers to adjust to improve a 'bad' row.
    We prioritize changing the columns identified by 'blame' as the primary
    drivers of poor performance (specifically for 'Idle-').
    """
    # Load the full dataset to determine what "good" looks like
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_csv = next(reader)
        rows = [[float(x) for x in r] for r in reader]

    # Identify the columns that cause the most idleness
    drivers = blame(header_csv, rows)
    
    recommendations = {}
    for driver in drivers:
        if driver in levers:
            low, high = levers[driver]
            # To reduce Idle-, we move the lever to the value that 
            # correlates with better performance (the opposite of the 'worst' direction).
            # Since blame() returns drivers where worst_avg > best_avg, 
            # we move the lever towards the lower bound.
            recommendations[driver] = low
            break 
            
    return recommendations

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in r] for r in reader]
        
        # Define levers based on the problem domain (numeric inputs)
        # All inputs in pom3a are numeric [0, 1]
        levers = {
            'Culture': (0.0, 1.0),
            'Criticality': (0.0, 1.0),
            'Criticality Modifier': (0.0, 1.0),
            'Initial Known': (0.0, 1.0),
            'Inter-Dependency': (0.0, 1.0),
            'Dynamism': (0.0, 1.0),
            'Size': (0.0, 1.0),
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0)
        }
        
        # Pick a 'bad' row (e.g., one with high Idle-)
        idle_idx = header.index('Idle-')
        bad_row = max(rows, key=lambda r: r[idle_idx])
        
        suggestion = fix(header, bad_row, levers)
        
        print("To rescue the project from being over budget and idle:")
        for col, val in suggestion.items():
            print(f"Adjust '{col}' to {val:.2f}.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

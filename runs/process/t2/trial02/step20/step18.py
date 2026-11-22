import csv
from step08 import fix as step08_fix

def fix(header, row, levers):
    """
    Recommends changes to cut idle time.
    Since we cannot hire (Team Size is fixed), we exclude it from the levers
    and use the logic from step08 to find the best improvement for the remaining levers.
    """
    # Filter out 'Team Size' from the allowed levers as per customer constraint
    allowed_levers = {k: v for k, v in levers.items() if k != 'Team Size'}
    
    # Use the existing fix logic from step08 to find the best change
    return step08_fix(header, row, allowed_levers)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        # Define levers excluding 'Team Size'
        levers = {
            "Culture": (0.0, 1.0),
            "Criticality": (0.0, 1.0),
            "Criticality Modifier": (0.0, 1.0),
            "Initial Known": (0.0, 1.0),
            "Inter-Dependency": (0.0, 1.0),
            "Dynamism": (0.0, 1.0),
            "Size": (0.0, 1.0),
            "Plan": (0.0, 1.0)
        }
        
        # Find a row with high Idle-
        idle_idx = header.index("Idle-")
        bad_row = max(rows, key=lambda r: float(r[idle_idx]))
        
        recommendation = fix(header, bad_row, levers)
        
        print("To cut idle time without hiring, we recommend the following adjustments:")
        for col, val in recommendation.items():
            print(f"- Adjust {col} to {val:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

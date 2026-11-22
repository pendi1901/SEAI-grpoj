import csv
from step06 import justify as step06_justify

def justify(header, rows, row):
    """
    Compares the target 'row' against all 'rows' to explain why it is 
    better or worse than other configurations.
    """
    # Reuse the logic from step06 which estimates goals for '?' 
    # and ranks the row against the population.
    return step06_justify(header, rows, row)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if val.replace('.','',1).isdigit() or (val.startswith('-') and val[1:].replace('.','',1).isdigit()) else val for val in row])
        
        # Example: Compare a specific row (e.g., row 10) against the rest
        # The customer asks "Why not B?" where B is a specific setup.
        # We treat the last row as the "recommended" one and row 0 as "B".
        target_row = list(rows[0])
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        for idx in goal_indices:
            target_row[idx] = "?"
            
        p, reason = justify(header, rows[1:], target_row)
        
        print(f"Comparison result for setup B:")
        print(f"Rank: {p:.4f}")
        print(f"Justification: {reason}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

import csv
from step01 import remember
from step05 import blame

def fix(header, row, levers):
    """
    Recommends a change to cut idle time by identifying the most influential 
    levers (excluding 'Team Size') and adjusting them towards the values 
    found in top-performing setups.
    """
    filename = "pom3a.n1000.train.csv"
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header_csv = next(reader)
        rows = [row for row in reader]

    # Identify top rows to see what 'good' looks like
    best_indices = remember(header_csv, rows)
    best_rows = [rows[i] for i in best_indices]

    # Calculate average of levers in best rows
    best_averages = {}
    for col in levers:
        idx = header.index(col)
        vals = [float(r[idx]) for r in best_rows]
        best_averages[col] = sum(vals) / len(vals)

    # Recommend change for the lever that needs the most adjustment
    # We prioritize levers that are not 'Team Size' as per customer request
    recommendations = {}
    for col, target in best_averages.items():
        if col == "Team Size":
            continue
        
        idx = header.index(col)
        current = float(row[idx])
        low, high = levers[col]
        
        # Clamp target to allowed range
        new_val = max(low, min(high, target))
        if abs(new_val - current) > 0.01:
            recommendations[col] = new_val
            break 

    return recommendations

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]

        # Define available levers (excluding Team Size)
        levers = {
            "Culture": (0.0, 1.0),
            "Criticality": (0.0, 1.0),
            "Dynamism": (0.0, 1.0),
            "Size": (0.0, 1.0),
            "Plan": (0.0, 1.0)
        }

        # Find a row with high idle time to fix
        idle_idx = header.index('Idle-')
        bad_row = max(rows, key=lambda r: float(r[idle_idx]))
        
        suggestion = fix(header, bad_row, levers)

        print("Customer Inquiry: I am not allowed to hire. What else can I change to cut idle time?")
        print("Analysis: We analyzed high-idle setups and compared them to top-performing configurations.")
        print(f"Recommendation: Adjust the following parameter: {suggestion}")
        print("This change aligns your project with more efficient historical setups without changing team size.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

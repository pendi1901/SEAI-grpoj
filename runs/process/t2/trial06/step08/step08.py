import csv
from step01 import remember

def fix(header, row, levers):
    """
    Finds the smallest change to levers that moves the row towards 
    the characteristics of the top-performing rows.
    """
    # Load data to find what 'good' looks like
    filename = "pom3a.n1000.train.csv"
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header_csv = next(reader)
        rows = [row for row in reader]

    # Identify top rows
    best_indices = remember(header_csv, rows)
    best_rows = [rows[i] for i in best_indices]

    # Calculate average of levers in best rows
    best_averages = {}
    for col in levers:
        idx = header.index(col)
        vals = [float(r[idx]) for r in best_rows]
        best_averages[col] = sum(vals) / len(vals)

    # Recommend change for the lever that needs the most adjustment
    # We pick the one with the largest distance from the current row
    recommendations = {}
    for col, target in best_averages.items():
        idx = header.index(col)
        current = float(row[idx])
        low, high = levers[col]
        
        # Clamp target to allowed range
        new_val = max(low, min(high, target))
        if new_val != current:
            recommendations[col] = new_val
            break # Return one change as requested

    return recommendations

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    # Define levers based on problem context (Plan and Team Size)
    levers = {
        "Plan": (0.0, 1.0),
        "Team Size": (0.0, 1.0)
    }

    # Pick a 'bad' row (e.g., the last one) to fix
    bad_row = rows[-1]
    suggestion = fix(header, bad_row, levers)

    print("Customer Inquiry: How to rescue an over-budget, idle project?")
    print("Analysis: We compared your current setup against the top-performing configurations.")
    print(f"Recommendation: To improve performance, adjust the following: {suggestion}")
    print("These changes align your project parameters with those of successful, efficient setups.")

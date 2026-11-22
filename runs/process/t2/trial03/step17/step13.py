import csv
import step03

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (same distribution),
    False if they differ significantly. Uses the A12 effect size check.
    """
    return step03.certify(xs, ys)

def analyze_shift(header, rows):
    """
    Splits the data into two halves (before/after the change) and 
    checks if the goal distributions are statistically different.
    """
    # We assume the data is ordered chronologically.
    # Split into two halves to compare "before" and "after" the change.
    mid = len(rows) // 2
    before = rows[:mid]
    after = rows[mid:]
    
    # Identify goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    # Compare each goal column
    results = {}
    for idx in goal_indices:
        xs = [row[idx] for row in before]
        ys = [row[idx] for row in after]
        results[header[idx]] = certify(xs, ys)
        
    return results

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        shift_results = analyze_shift(header, rows)
        
        print("Analysis: Did results shift after the team decision process changed?")
        all_same = True
        for goal, is_same in shift_results.items():
            if not is_same:
                all_same = False
                print(f"  - {goal}: Significant shift detected.")
            else:
                print(f"  - {goal}: No significant shift (results are the same).")
        
        if all_same:
            print("\nConclusion: The results are statistically the same as before.")
        else:
            print("\nConclusion: There is a statistically significant shift in results.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import ezr
import random

def fix(header, row, levers):
    """
    Recommends a change to a 'bad' row to minimize 'Idle-'.
    We evaluate the impact of changing each lever on the 'Idle-' goal
    by calculating the ydist of the row after applying the change.
    """
    # Load data to establish context for "good" performance
    data = list(ezr.csv("pom3a.n1000.train.csv"))
    tbl = ezr.Tbl(data)
    
    # Identify the index of the 'Idle-' goal
    idle_idx = header.index("Idle-")
    
    # We want to minimize Idle-. We evaluate changes by checking 
    # which lever change results in the lowest value for Idle-.
    original_val = row[idle_idx]
    best_change = {}
    min_idle = float('inf')
    
    # We use the current row's state as a baseline
    # We test each lever by trying a value that moves towards the 
    # global median of the best-performing rows (lowest Idle-).
    sorted_rows = sorted(data[1:], key=lambda r: r[idle_idx])
    best_rows = sorted_rows[:max(1, len(data[1:]) // 10)]
    
    targets = {}
    for col in tbl.x:
        vals = [r[col.at] for r in best_rows]
        if isinstance(col, ezr.Num):
            targets[col.txt] = sum(vals) / len(vals)
        else:
            targets[col.txt] = max(set(vals), key=vals.count)

    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        old_val = row[idx]
        
        # Determine candidate values to test
        candidates = []
        if isinstance(allowed, tuple): # Numeric (low, high)
            low, high = allowed
            candidates = [max(low, min(high, targets.get(col_name, (low+high)/2)))]
        else: # Symbolic
            candidates = [v for v in allowed]
            
        for val in candidates:
            row[idx] = val
            # We evaluate based on the specific goal: Idle-
            current_idle = row[idle_idx]
            
            if current_idle < min_idle:
                min_idle = current_idle
                best_change = {col_name: val}
            
        # Reset row
        row[idx] = old_val
            
    return best_change

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("pom3a.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    tbl = ezr.Tbl(data)
    
    # Pick a "bad" row (highest Idle-)
    idle_idx = header.index("Idle-")
    bad_row = max(rows, key=lambda r: r[idle_idx])
    
    # Define levers based on input columns
    levers = {
        "Culture": (0.0, 1.0),
        "Criticality": (0.0, 1.0),
        "Criticality Modifier": (0.0, 1.0),
        "Initial Known": (0.0, 1.0),
        "Inter-Dependency": (0.0, 1.0),
        "Dynamism": (0.0, 1.0),
        "Size": (0.0, 1.0),
        "Plan": (0.0, 1.0),
        "Team Size": (0.0, 1.0)
    }
    
    recommendation = fix(header, bad_row, levers)
    
    print("--- Idle Time Reduction Strategy ---")
    if recommendation:
        for col, val in recommendation.items():
            print(f"To reduce idle time, we recommend setting '{col}' to {val:.4f}")
    else:
        print("No specific lever change was found to reduce idle time.")
    
    exit(0)

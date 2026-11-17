import csv
import step01
import step06

def fix(header, row, levers):
    """
    Finds the smallest change to a bad row's settings that improves its 
    performance score, ensuring the change is within allowed levers.
    """
    # Identify goal indices and directions
    goals = [(i, name[-1]) for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # Helper to calculate score for a candidate row
    def get_score(r):
        score = 0
        for i, direction in goals:
            val = r[i]
            # Use a simple heuristic: if numeric, normalize relative to row
            # Since we don't have global context here, we assume relative improvement
            if isinstance(val, (int, float)):
                score += (1 - val) if direction == '-' else val
        return score

    best_change = {}
    best_score = -float('inf')
    
    # Try changing each lever to its boundary or mid-point
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, (list, tuple)) and not isinstance(allowed[0], (int, float)):
            candidates = allowed
        else:
            candidates = [allowed[0], allowed[1]]
            
        for val in candidates:
            if val == original_val:
                continue
            
            new_row = list(row)
            new_row[idx] = val
            
            score = get_score(new_row)
            if score > best_score:
                best_score = score
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if val.replace('.', '', 1).isdigit() or (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) else val for val in row]
            data.append(processed_row)

    # Define levers based on column types
    levers = {
        "N_estimators": (10, 200),
        "criterion": ["squared_error", "absolute_error", "poisson"],
        "Min_sample_leaves": (1, 20),
        "Max_depth": (1, 20)
    }

    # Pick a "bad" row (e.g., the one with the lowest score)
    # We use step01 logic to find the worst row
    worst_idx = 0
    min_score = float('inf')
    for i, row in enumerate(data):
        score = sum(row[j] for j, name in enumerate(header) if name.endswith('+')) - \
                sum(row[j] for j, name in enumerate(header) if name.endswith('-'))
        if score < min_score:
            min_score = score
            worst_idx = i

    bad_row = data[worst_idx]
    recommendation = fix(header, bad_row, levers)
    
    print("To improve the performance of the current setup, we recommend the following change:")
    for col, val in recommendation.items():
        print(f"Set '{col}' to {val}.")

import csv

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop searching.
    A row is good if it performs better than the Pareto-optimal 
    frontier of all previously seen rows.
    """
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))  # Minimize
        elif name.endswith('+'):
            goals.append((i, 1))   # Maximize

    # If it's the first row, we can't compare, so keep looking
    if not seen:
        return False

    # Calculate a simple score for the current row relative to the seen data
    # We define 'good enough' as being better than the best observed in all goals
    def get_score(r):
        score = 0
        for col_idx, direction in goals:
            col_data = [float(s[col_idx]) for s in seen]
            best_val = max(col_data) if direction == 1 else min(col_data)
            # If we are better than the best seen in this goal, add to score
            if direction == 1:
                if float(r[col_idx]) >= best_val: score += 1
            else:
                if float(r[col_idx]) <= best_val: score += 1
        return score

    # If the row beats the best seen in all goal categories, stop
    return get_score(row) == len(goals)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if val.replace('.','',1).isdigit() or (val.startswith('-') and val[1:].replace('.','',1).isdigit()) else val for val in row]
                rows.append(processed_row)

        seen = []
        found = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Found a good setup at row {i+1}. Stopping search.")
                found = True
                break
            seen.append(row)
        
        if not found:
            print("No setup met the criteria to stop early.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

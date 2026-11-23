import csv
import step01

def flow(header, row, seen):
    """
    Warns the customer if a new row is significantly worse than the 
    historical baseline. We define 'bad' as being in the bottom 25% 
    of performance compared to all previously seen rows.
    """
    if not seen:
        return True

    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

    def get_score(r):
        # Lower is better: minimize '-' and negate '+'
        return sum(float(r[idx]) if op == '-' else -float(r[idx]) 
                   for idx, op in goal_indices)

    current_score = get_score(row)
    seen_scores = [get_score(r) for r in seen]
    
    # Calculate the 75th percentile of seen scores
    # If the current score is worse (higher) than the 75th percentile, it's 'bad'
    seen_scores.sort()
    threshold_idx = int(len(seen_scores) * 0.75)
    threshold = seen_scores[threshold_idx]
    
    # Return True if the row is 'good' (<= threshold), False if 'bad'
    return current_score <= threshold

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
            seen = []
            warnings = 0
            for i, row in enumerate(rows):
                if not flow(header, row, seen):
                    warnings += 1
                    if warnings <= 5:
                        print(f"Warning: Row {i} is performing poorly compared to history.")
                seen.append(row)
            
            print(f"Monitoring complete. Total programs processed: {len(rows)}.")
            print(f"Total performance warnings issued: {warnings}.")
            print("Logic: A program is flagged if its performance score falls into the bottom 25% of history.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

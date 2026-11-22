import csv

def flow(header, row, seen):
    """
    Warns if a project is going bad. We define 'bad' as a row that is 
    significantly worse than the average of the 'seen' history.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def score_row(r):
        total = 0.0
        for idx, op in goal_indices:
            val = float(r[idx])
            total += val if op == '-' else (1.0 - val)
        return total

    # If we have no history, we cannot judge if it is going bad
    if not seen:
        return False

    # Calculate current score
    current_score = score_row(row)
    
    # Calculate average score of history
    history_scores = [score_row(r) for r in seen]
    avg_history = sum(history_scores) / len(history_scores)
    
    # If current score is significantly worse (higher) than the average,
    # we flag it as "going bad".
    # We use a threshold of 1.5x the average to trigger a warning.
    if current_score > (avg_history * 1.5):
        return True
        
    return False

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
            seen = []
            warnings = 0
            for row in rows:
                if flow(header, row, seen):
                    warnings += 1
                seen.append(row)
            
            print("Customer Inquiry: Warn me the moment a project starts to go bad.")
            print(f"Analysis: Processed {len(rows)} weekly reports.")
            print(f"Warning: {warnings} projects were flagged as performing significantly worse than the historical average.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import csv

def flow(header, row, seen):
    """
    Warns the customer if a new row is significantly worse than the 
    historical baseline. We define 'going bad' as a row whose 
    aggregate goal performance is significantly below the 
    moving average of the 'seen' data.
    """
    goal_indices = [i for i, col in enumerate(header) if col.endswith(('-', '+'))]
    
    def get_score(r):
        # Normalize goals: '-' minimized (negated), '+' maximized (as is)
        score = 0
        for i in goal_indices:
            val = r[i]
            if header[i].endswith('-'):
                score -= val
            else:
                score += val
        return score

    # Need a baseline to determine what 'bad' is
    if len(seen) < 20:
        return False
    
    # Calculate moving average of performance
    scores = [get_score(r) for r in seen]
    avg_score = sum(scores) / len(scores)
    std_dev = (sum((s - avg_score)**2 for s in scores) / len(scores))**0.5
    
    # If the new row is more than 2 standard deviations below the mean,
    # it is performing significantly worse than the established trend.
    current_score = get_score(row)
    if current_score < (avg_score - 2 * std_dev):
        return True
        
    return False

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        seen = []
        warnings = 0
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                warnings += 1
                print(f"Warning: Row at index {i} is performing significantly worse than the baseline.")
            seen.append(row)
            
        if warnings == 0:
            print("No performance degradation detected in the provided data stream.")
        else:
            print(f"Analysis complete. {warnings} instances of performance degradation were flagged.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

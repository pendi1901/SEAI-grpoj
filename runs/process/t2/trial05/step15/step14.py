import csv
import step01

def flow(header, row, seen):
    """
    Warns the user if the current row is significantly worse than the 
    historical baseline. We define 'bad' as a row whose goal performance 
    is in the bottom 10% of the 'seen' data.
    """
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        total = 0
        for i in goal_indices:
            val = float(r[i])
            total += (1.0 - val) if header[i].endswith('-') else val
        return total

    # Need a baseline to determine what is "bad"
    if len(seen) < 50:
        return False

    # Calculate scores for all seen rows
    seen_scores = [get_score(s) for s in seen]
    current_score = get_score(row)
    
    # Define a threshold: if current score is worse than the 10th percentile
    # of historical performance, flag it as "bad".
    seen_scores.sort()
    threshold = seen_scores[len(seen_scores) // 10]
    
    return current_score < threshold

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
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
                print(f"Warning: Row {i} is performing poorly compared to historical data.")
            seen.append(row)
            
        print(f"Monitoring complete. Total bad setups detected: {warnings}.")
        exit(0)
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

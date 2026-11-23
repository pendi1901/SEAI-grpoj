import csv
import step04

def flow(header, row, seen):
    """
    Warns the customer by returning True if the current row is significantly 
    worse than the historical average of 'seen' rows.
    
    We define 'going bad' as a row whose performance score is worse than 
    the mean score of all previously seen rows by at least one standard deviation.
    """
    if not seen:
        return False

    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith(('-', '+'))]

    def score_row(r):
        total = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            total += val if op == '-' else (1.0 - val)
        return total

    # Calculate scores of all seen rows
    seen_scores = [score_row(r) for r in seen]
    
    # Calculate mean and standard deviation of seen scores
    mean = sum(seen_scores) / len(seen_scores)
    std = (sum((s - mean)**2 for s in seen_scores) / len(seen_scores))**0.5
    
    # Current row score
    current_score = score_row(row)
    
    # If current score is worse (higher) than mean + 1 std dev, warn (return True)
    if std > 0 and current_score > (mean + std):
        return True
    
    return False

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        warnings = 0
        seen = []
        for row in rows:
            if flow(header, row, seen):
                warnings += 1
            seen.append(row)
            
        print("Customer Inquiry: Warn me the moment a programme starts to go bad.")
        print(f"Answer: Monitoring complete. {warnings} programmes showed signs of performance degradation.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

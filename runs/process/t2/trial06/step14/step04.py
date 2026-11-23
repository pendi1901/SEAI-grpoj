import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides whether to accept a row based on whether it is better than 
    the best seen so far. Uses the same scoring logic as step01.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def score(r):
        s = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            s += val if op == '-' else -val
        return s

    current_score = score(row)
    
    # If this is the first row, accept it
    if not seen:
        return True
    
    # Otherwise, accept if it's better than everything seen so far
    best_seen_score = min(score(r) for r in seen)
    return current_score < best_seen_score

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        accepted = []
        seen = []
        for row in rows:
            if flow(header, row, seen):
                accepted.append(row)
            seen.append(row)
            
        print("Customer Inquiry: Online Decision Making")
        print(f"Processed {len(rows)} proposals one by one.")
        print(f"Strategy: Accept a proposal only if it is the best seen so far.")
        print(f"Total proposals approved: {len(accepted)}")
        print("This approach ensures we only commit to improvements over previous options.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import csv
import step01

def flow(header, row, seen):
    """
    Decides whether to accept a row based on whether it is better than 
    the current best seen so far.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def score_row(r):
        total = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            total += val if op == '-' else (1.0 - val)
        return total

    # If this is the first row, accept it
    if not seen:
        return True

    # Calculate score of current row and the best score seen so far
    current_score = score_row(row)
    best_score = min(score_row(r) for r in seen)

    # Accept if it's better than the best seen so far
    return current_score < best_score

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        accepted = []
        seen = []
        for row in rows:
            if flow(header, row, seen):
                accepted.append(row)
            seen.append(row)
            
        print(f"Customer Inquiry: Sequential decision making.")
        print(f"Processed {len(rows)} proposals.")
        print(f"Accepted {len(accepted)} proposals that improved upon previous bests.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

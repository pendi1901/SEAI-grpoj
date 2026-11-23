import csv
import step01

def flow(header, row, seen):
    """
    Decides whether to accept a row based on whether it is better than 
    the best seen so far. Since we cannot go back, we use a simple 
    threshold: accept if it's better than the current best.
    """
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        total = 0
        for i in goal_indices:
            val = r[i]
            # Minimize '-' (lower is better), Maximize '+' (higher is better)
            # Normalize: if '-', use val; if '+', use (1-val)
            if header[i].endswith('-'):
                total += val
            else:
                total += (1.0 - val)
        return total

    if not seen:
        return True
    
    current_score = get_score(row)
    best_seen_score = min(get_score(r) for r in seen)
    
    # Accept if this row is better than anything seen so far
    return current_score < best_seen_score

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        seen = []
        accepted_count = 0
        for row in rows:
            if flow(header, row, seen):
                accepted_count += 1
            seen.append(row)
            
        print(f"Processed {len(rows)} proposals.")
        print(f"Accepted {accepted_count} proposals based on sequential improvement.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

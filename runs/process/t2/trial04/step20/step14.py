import csv
import step01

def flow(header, row, seen):
    """
    Warns if a project starts to go bad.
    We define 'bad' as a significant degradation in performance compared to 
    the historical best. If the current row's score is worse than the 
    best seen so far by a significant margin (e.g., 2 standard deviations 
    or a simple threshold), we return True to flag it.
    """
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        total = 0
        for i in goal_indices:
            val = r[i]
            # Normalize: minimize '-' (val), maximize '+' (1-val)
            if header[i].endswith('-'):
                total += val
            else:
                total += (1.0 - val)
        return total

    if not seen:
        return False
    
    current_score = get_score(row)
    best_score = min(get_score(r) for r in seen)
    
    # If the current project is significantly worse than the best seen (e.g., 
    # score is 50% worse than the best), we flag it as "going bad".
    # This acts as an early warning system.
    if current_score > (best_score * 1.5):
        return True
    
    return False

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        seen = []
        warnings = 0
        for row in rows:
            if flow(header, row, seen):
                warnings += 1
            seen.append(row)
            
        print(f"Monitoring complete. {warnings} projects showed signs of degradation.")
        print("An early warning was triggered whenever a project's performance "
              "dropped significantly below the historical best.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

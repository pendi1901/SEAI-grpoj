import csv
from step01 import remember

def flow(header, row, seen):
    """
    Warns the user if a row is 'bad' compared to the history of 'seen' rows.
    We define 'bad' as a row that performs significantly worse than the 
    best-performing configurations seen so far.
    """
    if not seen:
        return False

    # Identify goal indices and directions
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    goal_directions = [-1 if header[i].endswith('-') else 1 for i in goal_indices]

    # Calculate normalized scores for all seen rows
    def get_scores(data):
        m = len(goal_indices)
        cols = [[float(r[idx]) for r in data] for idx in goal_indices]
        mins = [min(c) for c in cols]
        maxs = [max(c) for c in cols]
        
        normalized = []
        for r in data:
            row_scores = []
            for i in range(m):
                val = float(r[goal_indices[i]])
                denom = maxs[i] - mins[i]
                norm = (val - mins[i]) / denom if denom != 0 else 0
                row_scores.append(1 - norm if goal_directions[i] == -1 else norm)
            normalized.append(min(row_scores))
        return normalized

    # Evaluate current row against history
    all_data = seen + [row]
    scores = get_scores(all_data)
    
    # If the current row's score is in the bottom 25% of the history, warn the user
    current_score = scores[-1]
    history_scores = scores[:-1]
    
    # Threshold: if the row is worse than 75% of the history, it's "going bad"
    threshold = sorted(history_scores)[len(history_scores) // 4]
    
    return current_score < threshold

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        seen = []
        warnings = 0
        for row in rows:
            if flow(header, row, seen):
                warnings += 1
            seen.append(row)
            
        print(f"Analysis complete. Processed {len(rows)} weekly updates.")
        print(f"Warning: {warnings} configurations were identified as performing poorly.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

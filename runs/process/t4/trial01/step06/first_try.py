import csv
from step01 import remember
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the goals for the target row, compares it against all rows,
    and returns the percentile rank and a justification string.
    """
    # Identify goal indices and input indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Estimate goals for the target row using KNN (from step02 logic)
    # We need to pass the target row as a list of lists to guess()
    estimated_goals = guess(header, rows, [row])[0]
    
    # Create a full version of the target row with estimated goals
    full_row = list(row)
    for i, goal_idx in enumerate(goal_indices):
        full_row[goal_idx] = estimated_goals[i]
    
    # Calculate normalized scores for all rows (including the target)
    all_data = rows + [full_row]
    
    # Re-use remember logic to get normalized scores
    # We need to calculate the aggregate score for all rows
    goal_directions = [-1 if header[i].endswith('-') else 1 for i in goal_indices]
    
    cols = [[float(r[idx]) for r in all_data] for idx in goal_indices]
    mins = [min(c) for c in cols]
    maxs = [max(c) for c in cols]
    
    def get_agg_score(r):
        scores = []
        for i, idx in enumerate(goal_indices):
            val = float(r[idx])
            denom = maxs[i] - mins[i]
            norm = (val - mins[i]) / denom if denom != 0 else 0
            scores.append(1 - norm if goal_directions[i] == -1 else norm)
        return min(scores)
    
    target_score = get_agg_score(full_row)
    all_scores = [get_agg_score(r) for r in rows]
    
    # Calculate fraction of rows that are worse than target
    better_than_count = sum(1 for s in all_scores if s < target_score)
    p = better_than_count / len(rows)
    
    reason = f"This setup is better than {p:.1%} of all known configurations based on its estimated performance across all goals."
    
    return (p, reason)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if val.replace('.','',1).isdigit() or (val.startswith('-') and val[1:].replace('.','',1).isdigit()) else val for val in row])
        
        # Pick a sample row to justify (e.g., the last one)
        target_row = list(rows[-1])
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        for idx in goal_indices:
            target_row[idx] = "?"
            
        p, reason = justify(header, rows[:-1], target_row)
        print(f"Rank: {p:.4f}")
        print(f"Justification: {reason}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

import csv
import random
import step01

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We filter for rows with high 'Size' and 'Criticality', then
    sample from those to find the best within the 50-label budget.
    """
    # Identify indices
    size_idx = header.index('Size')
    crit_idx = header.index('Criticality')
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

    # Filter for "large and high criticality" (top 50% of both)
    # We use a simple heuristic to find candidates
    candidates = []
    for i, row in enumerate(rows):
        if row[size_idx] > 0.5 and row[crit_idx] > 0.5:
            candidates.append(i)
    
    # If not enough candidates, fall back to all rows
    if len(candidates) < 50:
        candidates = list(range(len(rows)))
        
    # Sample up to 50 from the candidates
    to_sample = random.sample(candidates, min(50, len(candidates)))
    
    best_idx = -1
    best_score = float('inf')
    
    for idx in to_sample:
        true_goals = label(idx)
        
        # Calculate score
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = true_goals[i]
            if header[g_idx].endswith('-'):
                score += val
            else:
                score += (1.0 - val)
        
        if score < best_score:
            best_score = score
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            full_data = [[float(val) for val in row] for row in reader]
            
        goal_indices = [i for i, name in enumerate(header) 
                        if name.endswith('-') or name.endswith('+')]
        
        masked_rows = []
        for row in full_data:
            new_row = list(row)
            for i in goal_indices:
                new_row[i] = "?"
            masked_rows.append(new_row)
            
        def label(i):
            return [full_data[i][g] for g in goal_indices]
            
        best_idx = choose(header, masked_rows, label)
        
        print(f"Best setup for large, high-criticality project found at row index: {best_idx}")
        print("Goal values for this setup:")
        for i in goal_indices:
            print(f"  {header[i]}: {full_data[best_idx][i]:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

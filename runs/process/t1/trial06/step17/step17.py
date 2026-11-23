import csv
import random

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We filter for high 'Size' and 'Criticality' inputs, then use a 
    small-budget search to find the best among those candidates.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    size_idx = header.index('Size')
    crit_idx = header.index('Criticality')

    # Filter for "large and high-criticality" projects
    # We look for rows where Size and Criticality are in the top 50%
    candidates = []
    for i, row in enumerate(rows):
        if row[size_idx] > 0.5 and row[crit_idx] > 0.5:
            candidates.append(i)
    
    # If not enough candidates, fall back to all rows
    if len(candidates) < 10:
        candidates = list(range(len(rows)))
    
    # Budget: 50 labels. We sample 50 candidates to find the best.
    sample_size = min(len(candidates), 50)
    sampled = random.sample(candidates, sample_size)
    
    best_idx = -1
    best_score = float('inf')
    
    for i in sampled:
        goals = label(i)
        # Calculate score: minimize '-' and maximize '+'
        score = 0
        for j, g_idx in enumerate(goal_indices):
            val = goals[j]
            if header[g_idx].endswith('-'):
                score += val
            else:
                score += (1.0 - val)
        
        if score < best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            full_rows = [[float(x) for x in row] for row in reader]
        
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        rows_hidden = [[("?" if i in goal_indices else val) for i, val in enumerate(r)] for r in full_rows]
        
        labeled_count = 0
        def label(i):
            global labeled_count
            labeled_count += 1
            if labeled_count > 50:
                raise Exception("Too many labels!")
            return [full_rows[i][idx] for idx in goal_indices]
            
        best_idx = choose(header, rows_hidden, label)
        
        print("Analysis: Finding the best setup for large, high-criticality projects.")
        print(f"Recommended configuration found at index: {best_idx}")
        print(f"Total labels used: {labeled_count}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

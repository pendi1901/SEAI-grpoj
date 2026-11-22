import csv
import random
from step01 import remember

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-stakes project.
    We use a heuristic: sample 50 rows, label them, and pick the best.
    Since failure is damaging, we prioritize the 'remember' logic 
    to identify high-performing regions before sampling.
    """
    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

    def get_score(row_goals):
        s = 0
        for i, (idx, op) in enumerate(goal_indices):
            val = float(row_goals[i])
            s += val if op == '-' else -val
        return s

    # Strategy: 
    # 1. Use 'remember' on the whole dataset to find the top 5% candidates.
    # 2. If we have enough budget, sample from those candidates.
    # 3. If the dataset is small, just sample 50 evenly.
    
    n = len(rows)
    best_indices = remember(header, rows)
    
    # We have a budget of 50 labels.
    # We prioritize labeling the rows identified as 'best' by our heuristic.
    to_label = best_indices[:50]
    
    # If we have budget left, fill with random samples to explore
    if len(to_label) < 50:
        remaining = 50 - len(to_label)
        others = [i for i in range(n) if i not in to_label]
        to_label.extend(random.sample(others, min(len(others), remaining)))

    best_idx = -1
    best_score = float('inf')

    for i in to_label:
        true_goals = label(i)
        score = get_score(true_goals)
        
        if score < best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        # Mock label function for the test harness
        def label(i):
            return [rows[i][idx] for idx, _ in 
                    [(j, name[-1]) for j, name in enumerate(header) 
                     if name.endswith('-') or name.endswith('+')]]

        best_row_idx = choose(header, rows, label)
        
        print(f"For high-stakes projects, the recommended setup is at row index: {best_row_idx}")
        print("This selection was made by prioritizing historically high-performing configurations.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import csv
import random
from step01 import remember

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We filter for high 'Size' and 'Criticality' first, then sample
    to find the best performer within that subset.
    """
    size_idx = header.index('Size')
    crit_idx = header.index('Criticality')
    
    # Filter for "large" and "high criticality" projects (top 50% of each)
    # This narrows the search space to the relevant domain.
    candidates = []
    for i, row in enumerate(rows):
        if row[size_idx] > 0.5 and row[crit_idx] > 0.5:
            candidates.append(i)
            
    # Sample up to 50 from this subset
    sample_size = min(50, len(candidates))
    sampled_indices = random.sample(candidates, sample_size)
    
    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    def score_goals(goals):
        total = 0
        for i, (idx, op) in enumerate(goal_indices):
            val = goals[i]
            total += val if op == '-' else (1.0 - val)
        return total
    
    best_score = float('inf')
    best_idx = -1
    
    for i in sampled_indices:
        true_goals = label(i)
        current_score = score_goals(true_goals)
        if current_score < best_score:
            best_score = current_score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_data = []
            for row in reader:
                numeric_row = [float(x) for x in row]
                rows.append(numeric_row)
                true_data.append([numeric_row[i] for i, name in enumerate(header) 
                                 if name.endswith(('-', '+'))])
            
            # Mask goals
            goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
            for row in rows:
                for idx in goal_indices:
                    row[idx] = "?"
            
            def label(i):
                return true_data[i]
            
            best_idx = choose(header, rows, label)
            
            print("Customer Inquiry: Best setup for a large, high-criticality project?")
            print(f"Analysis: After trialling a subset of high-impact configurations,")
            print(f"the recommended setup is at index {best_idx}.")
            print(f"Goals for this setup: {true_data[best_idx]}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 setups.
    We use a simple random sampling strategy to explore the space,
    labeling 50 rows and returning the index of the one with the best aggregate score.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    
    # Pre-calculate min/max for normalization based on the first 50 rows
    # or just use a heuristic since we only have 50 labels.
    # We will label 50 random rows.
    indices = list(range(len(rows)))
    random.shuffle(indices)
    sample_indices = indices[:50]
    
    best_idx = -1
    best_score = -float('inf')
    
    # Store labeled data to normalize
    labeled_data = []
    for i in sample_indices:
        goals = label(i)
        labeled_data.append((i, goals))
        
    # Normalize goals
    # Transpose goals to get min/max per goal
    all_goals = [d[1] for d in labeled_data]
    mins = [min(g[i] for g in all_goals) for i in range(len(goal_indices))]
    maxs = [max(g[i] for g in all_goals) for i in range(len(goal_indices))]
    
    for i, goals in labeled_data:
        scores = []
        for j, g_idx in enumerate(goal_indices):
            val = goals[j]
            norm = (val - mins[j]) / (maxs[j] - mins[j] + 1e-9)
            # '-' minimize, '+' maximize
            if header[g_idx].endswith('-'):
                scores.append(1 - norm)
            else:
                scores.append(norm)
        
        agg = sum(scores) / len(scores)
        if agg > best_score:
            best_score = agg
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals = []
            for row in reader:
                processed = []
                goals = []
                for i, val in enumerate(row):
                    if header[i].endswith(('-', '+')):
                        goals.append(float(val))
                        processed.append("?")
                    else:
                        try:
                            processed.append(float(val))
                        except ValueError:
                            processed.append(val)
                rows.append(processed)
                true_goals.append(goals)
        
        def label(i):
            return true_goals[i]
        
        best_idx = choose(header, rows, label)
        print(f"Customer Inquiry: Best setup found after 50 trials.")
        print(f"The best row index is: {best_idx}")
        print("Goals for this setup:")
        for i, h in enumerate(header):
            if h.endswith(('-', '+')):
                print(f"  {h}: {true_goals[best_idx][header.index(h) - (len(header)-len(true_goals[0]))]:.4f}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

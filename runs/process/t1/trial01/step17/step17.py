import csv
import random

def get_score(header, row):
    """Calculates a normalized score [0, 1] where lower is better."""
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))
    
    scores = []
    for idx, op in goal_indices:
        val = float(row[idx])
        scores.append(val if op == '-' else (1.0 - val))
    return sum(scores) / len(scores)

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We filter for rows where 'Size' and 'Criticality' are high,
    then sample from those to find the best performer within 50 labels.
    """
    size_idx = header.index('Size')
    crit_idx = header.index('Criticality')
    
    # Filter for "large" and "high criticality" projects
    # Using 0.7 as a threshold for "high"
    candidates = [i for i, row in enumerate(rows) 
                  if float(row[size_idx]) > 0.7 and float(row[crit_idx]) > 0.7]
    
    # If not enough candidates, fall back to all rows
    if len(candidates) < 50:
        candidates = list(range(len(rows)))
        
    # Sample up to 50 candidates
    sample_indices = random.sample(candidates, min(len(candidates), 50))
    
    best_idx = -1
    best_score = float('inf')
    
    for i in sample_indices:
        true_goals = label(i)
        temp_row = list(rows[i])
        goal_indices = [idx for idx, name in enumerate(header) if name.endswith(('-', '+'))]
        for j, g_idx in enumerate(goal_indices):
            temp_row[g_idx] = true_goals[j]
            
        score = get_score(header, temp_row)
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
            full_data = [[float(x) for x in row] for row in reader]
            rows = []
            for row in full_data:
                masked = [("?" if header[i].endswith(('-', '+')) else row[i]) for i in range(len(row))]
                rows.append(masked)

        def label(i):
            goal_indices = [idx for idx, name in enumerate(header) if name.endswith(('-', '+'))]
            return [full_data[i][idx] for idx in goal_indices]

        best_idx = choose(header, rows, label)
        
        print("Customer Inquiry: Optimal Setup for Large, High-Criticality Projects")
        print(f"Analysis: After evaluating targeted samples, the best setup is at index {best_idx}.")
        print("This configuration minimizes risk and cost for large-scale, high-stakes projects.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

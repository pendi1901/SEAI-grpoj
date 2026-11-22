import csv
import random

def choose(header, rows, label):
    """
    Finds the best setup for a 'large' project (high 'Size') where failure is 
    damaging (high 'Criticality'). We prioritize rows that meet these criteria 
    and then optimize for the best goal performance within a 50-label budget.
    """
    size_idx = header.index('Size')
    crit_idx = header.index('Criticality')
    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

    def score_row(row_values):
        total = 0.0
        for idx, op in goal_indices:
            val = float(row_values[idx])
            total += val if op == '-' else (1.0 - val)
        return total

    # 1. Filter for 'large' and 'high criticality' projects
    # We look for rows where Size > 0.7 and Criticality > 0.7
    candidates = [i for i, row in enumerate(rows) 
                  if float(row[size_idx]) > 0.7 and float(row[crit_idx]) > 0.7]
    
    # If no candidates found, fallback to all rows
    if not candidates:
        candidates = list(range(len(rows)))

    # 2. Sample up to 50 candidates to find the best one
    trials = min(50, len(candidates))
    sample_indices = random.sample(candidates, trials)
    
    best_idx = -1
    best_score = float('inf')
    
    for i in sample_indices:
        true_goals = label(i)
        temp_row = list(rows[i])
        for j, (idx, _) in enumerate(goal_indices):
            temp_row[idx] = true_goals[j]
            
        current_score = score_row(temp_row)
        if current_score < best_score:
            best_score = current_score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
            # Define label function
            def label(i):
                return [float(rows[i][j]) for j, name in enumerate(header) 
                        if name.endswith('-') or name.endswith('+')]
            
            # Mask rows
            masked_rows = []
            for row in rows:
                new_row = list(row)
                for i in range(len(header)):
                    if header[i].endswith('-') or header[i].endswith('+'):
                        new_row[i] = "?"
                masked_rows.append(new_row)
            
            best_idx = choose(header, masked_rows, label)
            
            print("Customer Inquiry: Best setup for a large, high-criticality project?")
            print(f"Analysis: After evaluating candidates, the best configuration is at index {best_idx}.")
            print("This setup was selected by prioritizing high-impact project parameters and minimizing goal scores.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

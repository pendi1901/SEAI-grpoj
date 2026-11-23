import csv
import step01
import step07

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We filter for rows where 'Size' and 'Criticality' are high,
    then sample from those to find the best within the 50-label budget.
    """
    # Identify indices for filtering
    size_idx = header.index('Size')
    crit_idx = header.index('Criticality')
    
    # Filter for "large" and "high criticality" (above median)
    sizes = [r[size_idx] for r in rows]
    crits = [r[crit_idx] for r in rows]
    med_size = sum(sizes) / len(sizes)
    med_crit = sum(crits) / len(crits)
    
    candidates = [i for i, r in enumerate(rows) 
                  if r[size_idx] >= med_size and r[crit_idx] >= med_crit]
    
    # If not enough candidates, fall back to all rows
    if not candidates:
        candidates = list(range(len(rows)))
        
    # Sample up to 50 candidates
    import random
    sample_size = min(len(candidates), 50)
    to_test = random.sample(candidates, sample_size)
    
    best_idx = -1
    best_score = float('inf')
    
    def get_score(row_with_goals):
        total = 0
        for i, name in enumerate(header):
            if name.endswith('-'):
                total += row_with_goals[i]
            elif name.endswith('+'):
                total += (1.0 - row_with_goals[i])
        return total

    for idx in to_test:
        goals = label(idx)
        temp_row = list(rows[idx])
        goal_ptr = 0
        for i, name in enumerate(header):
            if name.endswith('-') or name.endswith('+'):
                temp_row[i] = goals[goal_ptr]
                goal_ptr += 1
        
        score = get_score(temp_row)
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
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        def label(i):
            return [rows[i][j] for j, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
        
        best_idx = choose(header, rows, label)
        
        print("Customer Inquiry: Find the best setup for a large, high-criticality project.")
        print(f"Answer: The best setup found for your requirements is at index {best_idx}.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

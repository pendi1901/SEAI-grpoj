import csv
import random

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-stakes project by sampling 50 rows.
    We prioritize rows with high 'Size' (large projects) and then evaluate
    their goal performance to find the best among them.
    """
    # Identify indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    size_idx = header.index('Size')
    
    # 1. Filter for 'large' projects (Size > 0.75)
    large_indices = [i for i, row in enumerate(rows) if row[size_idx] > 0.75]
    
    # If not enough large projects, fall back to all rows
    candidates = large_indices if len(large_indices) >= 50 else range(len(rows))
    
    # 2. Sample up to 50 candidates
    sample_size = min(50, len(candidates))
    indices_to_sample = random.sample(candidates, sample_size)
    
    best_idx = -1
    best_score = -float('inf')
    
    # 3. Evaluate samples
    for idx in indices_to_sample:
        true_goals = label(idx)
        
        # Calculate aggregate score
        # Normalize: '-' (lower is better), '+' (higher is better)
        # Since we only have 50 samples, we use raw values relative to the sample set
        current_score = 0
        for i, g_idx in enumerate(goal_indices):
            val = true_goals[i]
            if header[g_idx].endswith('-'):
                current_score -= val
            else:
                current_score += val
        
        if current_score > best_score:
            best_score = current_score
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
                rows.append(processed_row)
        
        def label(i):
            return [rows[i][j] for j, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        
        # Mask goals
        goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        masked_rows = []
        for row in rows:
            new_row = list(row)
            for g in goal_indices:
                new_row[g] = "?"
            masked_rows.append(new_row)
            
        best_idx = choose(header, masked_rows, label)
        
        print("Customer Inquiry: Best setup for a large, high-stakes project")
        print("-" * 60)
        print(f"The best row found is at index: {best_idx}")
        print(f"Row data: {rows[best_idx]}")
        print("\nStrategy: Filtered for large-scale projects (Size > 0.75) and")
        print("sampled 50 candidates to identify the most robust configuration.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

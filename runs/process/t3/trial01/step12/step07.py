import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 rows and evaluating them.
    Uses a random sampling strategy to explore the space, then picks the best.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    # We can label at most 50 rows.
    # We will pick 50 random indices to sample.
    n_rows = len(rows)
    sample_size = min(50, n_rows)
    indices_to_sample = random.sample(range(n_rows), sample_size)
    
    best_idx = -1
    best_score = -float('inf')
    
    # Pre-calculate global min/max for normalization based on the 50 samples
    # Since we don't know the full range, we use the samples as our universe.
    sampled_data = []
    for idx in indices_to_sample:
        sampled_data.append(label(idx))
        
    num_goals = len(goal_indices)
    mins = [min(row[i] for row in sampled_data) for i in range(num_goals)]
    maxs = [max(row[i] for row in sampled_data) for i in range(num_goals)]
    
    # Evaluate each sampled row
    for i, idx in enumerate(indices_to_sample):
        goals = sampled_data[i]
        score = 0
        for j in range(num_goals):
            denom = maxs[j] - mins[j]
            val = goals[j]
            norm = (maxs[j] - val) / denom if denom > 0 else 0
            if header[goal_indices[j]].endswith('+'):
                norm = 1.0 - norm
            score += norm
            
        if score > best_score:
            best_score = score
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    
    def load_data(fname):
        with open(fname, 'r') as f:
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
            return header, rows, true_goals

    try:
        header, rows, true_goals = load_data(filename)
        
        # The label function provided to choose()
        called_indices = set()
        def label(i):
            if i not in called_indices:
                if len(called_indices) >= 50:
                    raise Exception("Limit of 50 labels exceeded.")
                called_indices.add(i)
            return true_goals[i]
            
        best_row_idx = choose(header, rows, label)
        
        print("Optimization Result:")
        print("-" * 30)
        print(f"Best row found at index: {best_row_idx}")
        print("Goal values for this row:")
        for i, g_idx in enumerate([i for i, name in enumerate(header) if name.endswith(('-', '+'))]):
            print(f"  {header[g_idx]}: {true_goals[best_row_idx][i]:.4f}")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

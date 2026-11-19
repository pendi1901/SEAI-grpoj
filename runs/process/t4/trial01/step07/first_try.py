import csv
import random
from step01 import remember

def choose(header, rows, label):
    """
    Selects the best row by sampling 50 candidates and evaluating them 
    using the provided label function.
    """
    # Identify indices
    n = len(rows)
    # We can label at most 50 rows.
    # We pick 50 random indices to evaluate.
    indices_to_sample = random.sample(range(n), min(n, 50))
    
    evaluated_data = []
    for idx in indices_to_sample:
        # Get true goals
        true_goals = label(idx)
        
        # Create a full row representation
        full_row = list(rows[idx])
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        for i, g_idx in enumerate(goal_indices):
            full_row[g_idx] = true_goals[i]
            
        evaluated_data.append((idx, full_row))
    
    # Use remember logic to find the best among the 50 evaluated
    # We need to pass the full rows to remember
    best_rows_data = [d[1] for d in evaluated_data]
    best_local_indices = remember(header, best_rows_data)
    
    # Return the original index of the best one found
    best_idx_in_evaluated = best_local_indices[0]
    return evaluated_data[best_idx_in_evaluated][0]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Setup for the harness
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        
        # Create a copy with hidden goals
        masked_rows = []
        for row in rows:
            new_row = list(row)
            for idx in goal_indices:
                new_row[idx] = "?"
            masked_rows.append(new_row)
            
        labeled_count = 0
        def label(i):
            nonlocal labeled_count
            labeled_count += 1
            if labeled_count > 50:
                raise Exception("Limit exceeded")
            return [rows[i][idx] for idx in goal_indices]
            
        best_idx = choose(header, masked_rows, label)
        
        print(f"Analysis complete. Evaluated {labeled_count} setups.")
        print(f"The best row found is at index: {best_idx}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

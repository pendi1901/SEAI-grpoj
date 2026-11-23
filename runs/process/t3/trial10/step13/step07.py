import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling and labeling.
    Uses a simple strategy:
    1. Label 50 random rows.
    2. Return the index of the best one found.
    """
    # Identify goal indices
    goal_indices = [i for i, col in enumerate(header) if col.endswith(('-', '+'))]
    
    # We can label at most 50 rows
    num_samples = min(len(rows), 50)
    indices_to_sample = random.sample(range(len(rows)), num_samples)
    
    best_idx = -1
    best_score = -float('inf')
    
    for idx in indices_to_sample:
        # Get true goal values
        goals = label(idx)
        
        # Calculate score: 
        # For '-', minimize (so negate). For '+', maximize (keep as is).
        # We use a simple sum of normalized goals if possible, 
        # but since we don't have global min/max, we use raw values 
        # assuming they are already in a comparable range [0, 1].
        current_score = 0
        for i, val in enumerate(goals):
            col_name = header[goal_indices[i]]
            if col_name.endswith('-'):
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
                # Keep goals as "?" for the simulation
                processed_row = []
                for i, val in enumerate(row):
                    if header[i].endswith(('-', '+')):
                        processed_row.append("?")
                    else:
                        processed_row.append(float(val))
                rows.append(processed_row)
            
            # Load full data for the label function
            full_data = []
            with open(filename, 'r') as f2:
                reader2 = csv.reader(f2)
                next(reader2)
                for row in reader2:
                    full_data.append([float(x) for x in row])
            
            def label(i):
                goal_indices = [idx for idx, col in enumerate(header) if col.endswith(('-', '+'))]
                return [full_data[i][idx] for idx in goal_indices]
            
            best_index = choose(header, rows, label)
            
            print("Customer Inquiry: Best Setup Selection")
            print(f"After trialing 50 configurations, the best setup found is at index {best_index}.")
            print(f"This configuration has been identified as the most efficient based on your goals.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

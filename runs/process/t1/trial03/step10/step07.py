import csv
import random

def choose(header, rows, label):
    """
    Selects the best row by sampling 50 candidates and evaluating them.
    Uses a random subset to explore the space and returns the index of the best one.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    def get_score(goals):
        # Normalize goals: minimize all. 
        # For '-', lower is better. For '+', higher is better (negate).
        score = 0
        for i, val in enumerate(goals):
            name = header[goal_indices[i]]
            if name.endswith('-'):
                score += val
            else:
                score -= val
        return score

    # We have 800 rows. We can label 50.
    # We pick 50 random indices to evaluate.
    indices = random.sample(range(len(rows)), 50)
    
    best_idx = -1
    best_score = float('inf')
    
    for idx in indices:
        goals = label(idx)
        score = get_score(goals)
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
            # Store full data to simulate the 'label' function
            full_data = []
            for row in reader:
                full_data.append([float(x) for x in row])
        
        # Create masked rows for the choose function
        goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
        masked_rows = []
        for row in full_data:
            new_row = row[:]
            for idx in goal_indices:
                new_row[idx] = "?"
            masked_rows.append(new_row)
            
        def label(i):
            return [full_data[i][idx] for idx in goal_indices]
            
        best_index = choose(header, masked_rows, label)
        
        print(f"Analysis complete.")
        print(f"The best setup found among the 50 trials is at index {best_index}.")
        print("Setup details:")
        print(dict(zip(header, full_data[best_index])))
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

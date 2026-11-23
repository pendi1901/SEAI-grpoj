import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 setups.
    We use a simple random sampling strategy to explore the space,
    then select the best one based on the labeled goal values.
    """
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    def get_score(row_goals):
        score = 0.0
        for i, val in enumerate(row_goals):
            name = header[goal_indices[i]]
            if name.endswith('-'):
                score += val
            else:
                score += (1.0 - val)
        return score

    # We have 800 rows. We can label 50.
    # To get a good spread, we sample 50 indices randomly.
    indices = random.sample(range(len(rows)), 50)
    
    best_idx = -1
    best_score = float('inf')
    
    for i in indices:
        goals = label(i)
        score = get_score(goals)
        if score < best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            # Store full rows to access goals when labeled
            full_rows = []
            for row in reader:
                full_rows.append([float(x) for x in row])
        
        # Mock the label function for the standalone execution
        def label(i):
            goal_indices = [idx for idx, name in enumerate(header) 
                            if name.endswith('-') or name.endswith('+')]
            return [full_rows[i][idx] for idx in goal_indices]
        
        best_index = choose(header, full_rows, label)
        
        print("Customer Inquiry: Best Setup Selection")
        print("-" * 40)
        print(f"After trialing 50 setups, the best configuration")
        print(f"was found at index: {best_index}")
        print(f"Data for this row: {full_rows[best_index]}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

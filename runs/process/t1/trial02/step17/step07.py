import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 setups.
    We use a simple random sampling strategy to explore the space
    and identify the best performing configuration.
    """
    # Identify goal indices
    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

    def score_row(row_values):
        # Calculate a normalized score: lower is better.
        # For '-', we want low values. For '+', we want high values (1-val).
        total = 0.0
        for idx, op in goal_indices:
            val = float(row_values[idx])
            total += val if op == '-' else (1.0 - val)
        return total

    # We have 50 trials. We pick 50 random indices.
    num_rows = len(rows)
    trials = min(50, num_rows)
    indices = random.sample(range(num_rows), trials)
    
    best_idx = -1
    best_score = float('inf')
    
    for i in indices:
        # Get true goal values from the harness
        true_goals = label(i)
        
        # Create a temporary row with true goals to score it
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
            
            # Define the label function for the harness
            def label(i):
                # Return the actual goal values from the row
                return [float(rows[i][j]) for j, name in enumerate(header) 
                        if name.endswith('-') or name.endswith('+')]
            
            # Mask the rows as per instructions
            masked_rows = []
            for row in rows:
                new_row = list(row)
                for i in range(len(header)):
                    if header[i].endswith('-') or header[i].endswith('+'):
                        new_row[i] = "?"
                masked_rows.append(new_row)
            
            best_idx = choose(header, masked_rows, label)
            
            print("Customer Inquiry: Best setup found after 50 trials.")
            print(f"The best configuration is at index: {best_idx}")
            print("This setup was selected based on the lowest aggregate goal score.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

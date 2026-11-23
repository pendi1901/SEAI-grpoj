import csv
import step01
import step06

def choose(header, rows, label):
    """
    Finds the best row by sampling. We use the first 50 rows to label
    and find the best one among them.
    """
    # We have a budget of 50 labels.
    # We will sample the first 50 rows to find the best configuration.
    budget = 50
    best_idx = -1
    best_score = float('inf')
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    for i in range(min(len(rows), budget)):
        # Get true values from the oracle
        true_goals = label(i)
        
        # Update the row with true values
        for j, goal_idx in enumerate(goal_indices):
            rows[i][goal_idx] = true_goals[j]
            
        # Score the row using the logic from step01
        score = 0.0
        for idx, name in enumerate(header):
            if name.endswith('-'):
                score += rows[i][idx]
            elif name.endswith('+'):
                score += (1.0 - rows[i][idx])
        
        if score < best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(x) for x in row])
            
    # Keep a copy of true data for the label function
    true_data = [list(r) for r in rows]
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # Mask rows
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    def label(i):
        return [true_data[i][idx] for idx in goal_indices]
    
    best_row_idx = choose(header, rows, label)
    
    print("Customer Inquiry: Best setup found within 50 trials.")
    print(f"The best configuration was found at index: {best_row_idx}")
    print(f"Data for this row: {true_data[best_row_idx]}")

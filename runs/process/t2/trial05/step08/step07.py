import csv
import step01

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 rows.
    We use a simple strategy: sample 50 rows spread across the dataset,
    label them, and return the index of the one with the best score.
    """
    # Identify goal indices
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    def get_score(row_vals):
        total = 0
        for i, g_idx in enumerate(goal_indices):
            val = float(row_vals[i])
            # Minimize '-' (1-val), Maximize '+' (val)
            total += (1.0 - val) if header[g_idx].endswith('-') else val
        return total

    # We have 800 rows, we can label 50.
    # We pick 50 indices evenly spaced to get a representative view.
    n = len(rows)
    indices = [int(i * (n - 1) / 49) for i in range(50)]
    
    best_idx = -1
    best_score = -1.0
    
    for idx in indices:
        # Get true goal values via the label function
        true_goals = label(idx)
        
        # Create a temporary row with the true goals to calculate score
        temp_row = list(rows[idx])
        for i, g_idx in enumerate(goal_indices):
            temp_row[g_idx] = true_goals[i]
            
        score = get_score([temp_row[g] for g in goal_indices])
        
        if score > best_score:
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
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        # Define the label function for the harness
        def label(i):
            return [rows[i][col] for col, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
        
        best_row_idx = choose(header, rows, label)
        
        print(f"The best setup found after 50 trials is at row index {best_row_idx}.")
        goal_vals = [f"{header[i]}={rows[best_row_idx][i]:.4f}" 
                     for i, name in enumerate(header) 
                     if name.endswith('-') or name.endswith('+')]
        print(f"Performance: {', '.join(goal_vals)}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

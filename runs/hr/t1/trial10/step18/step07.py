import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows, 
    labeling them to get their true goal values, and picking 
    the one that maximizes the goal 'YearsAtCompany+'.
    """
    # Identify goal indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    yac_idx = header.index('YearsAtCompany+')
    
    # We have 800 rows. We can label 50.
    # We will pick 50 random indices to sample.
    indices = list(range(len(rows)))
    sample_indices = random.sample(indices, min(50, len(rows)))
    
    best_idx = -1
    max_yac = -1.0
    
    for i in sample_indices:
        # Label the row to get the true goal values
        true_goals = label(i)
        
        # The goal we care about is 'YearsAtCompany+'
        # We assume the label() returns values in the order of goal_indices
        # Find which index in true_goals corresponds to 'YearsAtCompany+'
        yac_val = 0.0
        for g_idx, col_idx in enumerate(goal_indices):
            if col_idx == yac_idx:
                yac_val = true_goals[g_idx]
                break
        
        if yac_val > max_yac:
            max_yac = yac_val
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Prepare hidden rows
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    hidden_rows = [row[:] for row in rows]
    for row in hidden_rows:
        for g in goal_indices:
            row[g] = "?"
            
    # Define the label function for the harness
    labeled_count = 0
    def label(i):
        global labeled_count
        labeled_count += 1
        if labeled_count > 50:
            raise Exception("Label limit exceeded")
        return [rows[i][g] for g in goal_indices]
    
    best_idx = choose(header, hidden_rows, label)
    
    print(f"Best row found: {best_idx}")
    print(f"Years at company: {rows[best_idx][header.index('YearsAtCompany+')]}")
    print(f"Job Role: {rows[best_idx][header.index('jobRole')]}")

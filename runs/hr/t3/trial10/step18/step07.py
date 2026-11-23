import csv
import random

def choose(header, rows, label):
    """
    Finds the working arrangement that keeps people longest by sampling 50 rows.
    'YearsAtCompany+' is the goal to maximize.
    """
    # Identify the goal column index
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+'))
    
    # Identify input columns that define 'working arrangement'
    work_cols = ['businessTravel', 'department', 'jobRole', 'overTime']
    work_indices = [header.index(c) for c in work_cols]
    
    # Randomly sample 50 indices to label
    sample_size = min(50, len(rows))
    indices_to_sample = random.sample(range(len(rows)), sample_size)
    
    best_val = -1.0
    best_idx = -1
    
    # Track performance by arrangement
    arrangement_performance = {}
    
    for i in indices_to_sample:
        # label(i) returns the full row (as per instructions, 
        # the harness provides the full row including the goal value)
        full_row = label(i)
        val = float(full_row[goal_idx])
        
        # Create a key representing the working arrangement
        arrangement = tuple(rows[i][idx] for idx in work_indices)
        
        if arrangement not in arrangement_performance:
            arrangement_performance[arrangement] = []
        arrangement_performance[arrangement].append(val)
        
        if val > best_val:
            best_val = val
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Keep a copy of original goals to simulate the label function
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+'))
    true_goals = [r[goal_idx] for r in rows]
    
    # Mask the goal column in the rows passed to choose
    for r in rows:
        r[goal_idx] = "?"

    def label(i):
        # Returns the full row with the true goal value restored
        row_copy = rows[i][:]
        row_copy[goal_idx] = true_goals[i]
        return row_copy

    best_idx = choose(header, rows, label)
    
    print(f"Analysis complete. The best working arrangement found is at index {best_idx}.")
    print(f"This employee has stayed for {true_goals[best_idx]} years.")
    print("The strategy sampled 50 random employees to identify the most effective working conditions.")

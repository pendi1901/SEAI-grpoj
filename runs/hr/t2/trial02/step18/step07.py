import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 rows, labeling them,
    and returning the index of the one with the highest 'YearsAtCompany+'.
    """
    # Identify the goal column
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+'):
            goal_idx = i
            break
    
    # We have 800 rows. We can label 50.
    # To find the best, we sample 50 indices.
    indices = list(range(len(rows)))
    sample_indices = random.sample(indices, min(50, len(rows)))
    
    best_idx = -1
    best_val = -float('inf')
    
    for idx in sample_indices:
        # label(i) returns the true goal values for rows[i]
        # The goal is a list of values for the goals in the file
        true_goals = label(idx)
        # Assuming the first goal found is the one we care about
        val = true_goals[0]
        
        if val > best_val:
            best_val = val
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
        
        for row in reader:
            new_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        new_row.append(float(val))
                    except ValueError:
                        new_row.append(0.0)
                else:
                    new_row.append(val)
            rows.append(new_row)
            
    # Define the label function for the harness
    def label(i):
        # Return the values of the goal columns for the given row
        return [rows[i][g] for g in goal_indices]
    
    # Mask the goal columns for the choose function
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for g in goal_indices:
            new_row[g] = "?"
        masked_rows.append(new_row)
        
    best_idx = choose(header, masked_rows, label)
    
    print(f"Analysis complete. After interviewing 50 staff, the best working arrangement "
          f"was found at row {best_idx}.")
    print(f"This employee has a tenure of {rows[best_idx][goal_indices[0]]} years.")

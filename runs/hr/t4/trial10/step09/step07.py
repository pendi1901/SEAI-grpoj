import csv
import random
from step02 import guess

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows, 
    labeling them to find their true goal values, and selecting 
    the one that maximizes 'YearsAtCompany+'.
    """
    # Identify goal columns
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    target_idx = goal_indices[0]
    
    # We have a budget of 50 labels.
    # We will sample 50 random rows to estimate the best arrangement.
    indices = list(range(len(rows)))
    sample_indices = random.sample(indices, min(50, len(rows)))
    
    best_idx = -1
    best_val = -float('inf')
    
    for i in sample_indices:
        # Label the row to get the true goal values
        true_goals = label(i)
        val = true_goals[0] # YearsAtCompany+
        
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

    # Mock label function for the test harness
    def label(i):
        # Return the goal values for the row at index i
        goal_indices = [idx for idx, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
        return [rows[i][idx] for idx in goal_indices]

    # Mask goals
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    best_index = choose(header, rows, label)
    
    print(f"Analysis complete.")
    print(f"The best working arrangement found within the 50-interview budget is at index {best_index}.")
    print(f"This employee has been with the company for {label(best_index)[0]} years.")

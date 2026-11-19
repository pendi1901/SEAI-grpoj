import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows.
    We prioritize 'YearsAtCompany+' (index 31).
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    # We focus on the first goal column: YearsAtCompany+
    target_idx = goal_indices[0]
    
    # Randomly sample 50 indices to query
    num_samples = 50
    indices_to_sample = random.sample(range(len(rows)), min(len(rows), num_samples))
    
    best_idx = -1
    best_val = -float('inf')
    
    for idx in indices_to_sample:
        # Get true values for this row
        true_goals = label(idx)
        val = true_goals[0] # YearsAtCompany+
        
        # Since it's a '+' goal, higher is better
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
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Store true goal values to simulate the label function
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    true_data = [[row[i] for i in goal_indices] for row in rows]
    
    # Mask rows
    for row in rows:
        for i in goal_indices:
            row[i] = "?"
            
    def label(i):
        return true_data[i]
        
    best_idx = choose(header, rows, label)
    
    print(f"Analysis complete.")
    print(f"The best working arrangement found is at row index: {best_idx}")
    print(f"This employee has been with the company for {true_data[best_idx][0]} years.")
    print("Logic: Sampled 50 random employees and selected the one with the highest 'YearsAtCompany+' value.")

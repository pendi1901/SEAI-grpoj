import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 rows, labeling them, and picking the one
    with the highest aggregate score for goal columns.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # We have 800 rows. We can label 50.
    # We pick 50 random indices to evaluate.
    indices_to_label = random.sample(range(len(rows)), 50)
    
    best_idx = -1
    best_score = -float('inf')
    
    for i in indices_to_label:
        # Get true values for this row
        true_goals = label(i)
        
        # Calculate score: 
        # For '+', higher is better. For '-', lower is better.
        # We normalize by assuming a rough range or just summing relative to goals.
        # Since we don't have global min/max, we use the values themselves.
        # To make them comparable, we treat '-' as negative and '+' as positive.
        current_score = 0
        for j, goal_idx in enumerate(goal_indices):
            val = true_goals[j]
            if header[goal_idx].endswith('+'):
                current_score += val
            else:
                current_score -= val
        
        if current_score > best_score:
            best_score = current_score
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

    # Store true goal values to simulate the label() function
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    labeled_data = {i: [row[idx] for idx in goal_indices] for i, row in enumerate(rows)}
    
    def label(i):
        return labeled_data[i]

    # Mask the rows
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    best_idx = choose(header, rows, label)
    
    print(f"The best working arrangement found is at row index {best_idx}.")
    print("This row was selected based on an evaluation of 50 sampled staff members.")

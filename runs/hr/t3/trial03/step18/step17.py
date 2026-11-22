import csv
import random

def choose(header, rows, label):
    """
    Finds the best row for 'Laboratory Technician' staff by sampling 50 rows,
    labeling them, and picking the one with the highest 'YearsAtCompany+' 
    (the primary goal).
    """
    # Identify indices
    try:
        job_idx = header.index('jobRole')
        goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    except (ValueError, StopIteration):
        return 0

    # Filter rows for Laboratory Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[job_idx] == 'Laboratory Technician']
    
    if not lab_indices:
        # Fallback to any row if no lab techs found
        lab_indices = list(range(len(rows)))

    # We have a budget of 50 labels.
    num_samples = min(len(lab_indices), 50)
    sampled_indices = random.sample(lab_indices, num_samples)
    
    best_idx = -1
    best_val = -float('inf')
    
    for i in sampled_indices:
        # label(i) returns the true goal values for the row
        goals = label(i)
        val = goals[0] # Assuming the first goal is the one to maximize
        
        if val > best_val:
            best_val = val
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Identify goal column index
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    
    # Store true values and mask them
    true_goals = [[row[goal_idx]] for row in rows]
    for row in rows:
        row[goal_idx] = "?"

    # Define the label function for the harness
    labeled_count = 0
    labeled_indices = set()
    
    def label(i):
        global labeled_count
        if i not in labeled_indices:
            if labeled_count >= 50:
                raise ValueError("Exceeded 50 labels")
            labeled_indices.add(i)
            labeled_count += 1
        return true_goals[i]

    best_row_idx = choose(header, rows, label)
    
    print(f"Best Laboratory Technician row found at index: {best_row_idx}")
    print(f"YearsAtCompany+ for this row: {true_goals[best_row_idx][0]}")
    print(f"Total interviews conducted: {labeled_count}")

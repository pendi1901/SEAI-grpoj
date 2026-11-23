import csv
import step02
import step07
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff
    by sampling up to 50 rows, labeling them, and using a Random Forest 
    to predict the best row among all candidates.
    """
    # Identify goal columns and jobRole column
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    target_idx = goal_indices[0]
    role_idx = header.index('jobRole')
    
    # Filter rows for Laboratory Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[role_idx] == 'Laboratory Technician']
    
    if not lab_indices:
        return 0
    
    # Select up to 50 random indices from the lab staff to label
    sample_size = min(50, len(lab_indices))
    indices_to_label = random.sample(lab_indices, sample_size)
    
    # Build training set from labeled data
    train_data = []
    for i in indices_to_label:
        row_copy = rows[i][:]
        row_copy[target_idx] = label(i)[0]
        train_data.append(row_copy)
        
    # Predict for all lab rows
    # We use step02.guess to train on our samples and predict the rest
    predictions = step02.guess(header, train_data, rows)
    
    # Find the index among lab staff with the highest predicted value
    best_idx = lab_indices[0]
    max_val = -float('inf')
    for i in lab_indices:
        if predictions[i] > max_val:
            max_val = predictions[i]
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    true_goals = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        goal_idx = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')][0]
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            true_goals.append(processed_row[goal_idx])
            processed_row[goal_idx] = "?"
            rows.append(processed_row)
            
    def label(i):
        return [true_goals[i]]
        
    best_row_idx = choose(header, rows, label)
    
    print(f"Analysis complete for Laboratory Technicians.")
    print(f"The best working arrangement found is at row index: {best_row_idx}")
    print(f"This row has been identified as having the highest potential for long-term retention.")

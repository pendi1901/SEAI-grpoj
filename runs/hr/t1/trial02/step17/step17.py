import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff
    by sampling up to 50 rows, labeling them, and selecting the one 
    with the highest tenure score.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    job_role_idx = header.index('jobRole')
    
    # Filter for Laboratory Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[job_role_idx] == 'Laboratory Technician']
    
    # If we have more than 50, sample 50. If fewer, use all.
    sample_size = min(len(lab_indices), 50)
    sample_indices = random.sample(lab_indices, sample_size)
    
    best_idx = -1
    best_score = -float('inf')
    
    for idx in sample_indices:
        # Get true goal values
        goals = label(idx)
        
        # Calculate score: sum of '+' goals minus sum of '-' goals
        current_score = 0
        for i, g_idx in enumerate(goal_indices):
            val = goals[i]
            if header[g_idx].endswith('+'):
                current_score += val
            else:
                current_score -= val
        
        if current_score > best_score:
            best_score = current_score
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

    # Prepare masked rows
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)

    # Tracking labels
    labeled_count = 0
    def label(i):
        global labeled_count
        labeled_count += 1
        if labeled_count > 50:
            raise Exception("Exceeded 50 labels")
        return [rows[i][idx] for idx in goal_indices]

    best_idx = choose(header, masked_rows, label)
    
    print(f"Analysis complete after {labeled_count} interviews with laboratory staff.")
    print(f"The best working arrangement found for a Laboratory Technician is at row index {best_idx}.")
    
    # Display the details of the best row
    best_row = rows[best_idx]
    print("Details of the best arrangement:")
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            print(f"  {name}: {best_row[i]}")

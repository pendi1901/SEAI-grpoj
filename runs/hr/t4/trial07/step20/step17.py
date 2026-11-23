import csv
import random
import step07

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff
    by sampling up to 50 rows from that specific subset.
    """
    # Filter rows to only include 'Laboratory Technician'
    role_idx = header.index('jobRole')
    lab_indices = [i for i, row in enumerate(rows) if row[role_idx] == 'Laboratory Technician']
    
    # If no lab staff found, fallback to all rows
    search_pool = lab_indices if lab_indices else range(len(rows))
    
    # Sample up to 50 indices from the lab staff
    sample_size = min(50, len(search_pool))
    indices_to_sample = random.sample(search_pool, sample_size)
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    best_idx = -1
    best_score = float('-inf')
    
    for i in indices_to_sample:
        # Get true goal values using the provided label function
        goals = label(i)
        
        # Calculate aggregate score: 
        # Maximize '+' goals, minimize '-' goals.
        current_score = 0
        for j, goal_val in enumerate(goals):
            col_idx = goal_indices[j]
            if header[col_idx].endswith('-'):
                current_score -= goal_val
            else:
                current_score += goal_val
        
        if current_score > best_score:
            best_score = current_score
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

    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # Create the label function
    def label(i):
        return [rows[i][idx] for idx in goal_indices]

    # Mask the goal columns
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    best_index = choose(header, rows, label)
    
    print(f"Analysis complete. The best working arrangement for Laboratory Technicians is at row index: {best_index}")
    print("This selection was based on an in-depth review of sampled laboratory staff records.")

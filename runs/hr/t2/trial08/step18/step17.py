import csv
import random
import step07

def choose(header, rows, label):
    """
    Finds the best working arrangement for laboratory staff only,
    sampling at most 50 rows.
    """
    # Identify laboratory staff
    role_idx = header.index('jobRole')
    lab_indices = [i for i, row in enumerate(rows) if row[role_idx] == 'Laboratory Technician']
    
    # If no lab staff, fallback to all rows
    search_space = lab_indices if lab_indices else range(len(rows))
    
    # Sample up to 50
    sample_size = min(50, len(search_space))
    indices_to_sample = random.sample(search_space, sample_size)
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    best_idx = -1
    best_score = -float('inf')
    
    for i in indices_to_sample:
        true_goals = label(i)
        
        # Calculate score: maximize (+) and minimize (-)
        score = 0
        for j, goal_idx in enumerate(goal_indices):
            val = true_goals[j]
            if header[goal_idx].endswith('+'):
                score += val
            else:
                score -= val
        
        if score > best_score:
            best_score = score
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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def label(i):
        return [rows[i][idx] for idx in goal_indices]
        
    best_idx = choose(header, rows, label)
    
    print(f"Analysis complete for Laboratory Technicians.")
    print(f"The best arrangement found is at row index: {best_idx}")
    print("This selection was made by sampling laboratory staff and optimizing for tenure metrics.")

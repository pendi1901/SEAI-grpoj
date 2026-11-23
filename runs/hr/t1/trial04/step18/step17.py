import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff.
    We filter for this role, sample up to 50 rows, and identify the best
    based on the goal columns.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    role_idx = header.index('jobRole')
    
    # Filter indices for Laboratory Technicians
    lab_indices = [i for i, r in enumerate(rows) if r[role_idx] == 'Laboratory Technician']
    
    # Sample up to 50
    sample_size = min(50, len(lab_indices))
    indices_to_query = random.sample(lab_indices, sample_size)
    
    best_idx = -1
    best_score = -float('inf')
    
    # Pre-calculate global min/max for normalization
    # Since we only have 50 labels, we use the sample to estimate relative performance
    for i in indices_to_query:
        true_goals = label(i)
        
        # Calculate score: Goal+ (higher is better), Goal- (lower is better)
        score = 0.0
        for j, g_idx in enumerate(goal_indices):
            val = true_goals[j]
            if header[g_idx].endswith('-'):
                score -= val
            else:
                score += val
        
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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    # Define the label function
    def label(i):
        return [rows[i][g] for g in goal_indices]

    # Mask the rows
    for row in rows:
        for g in goal_indices:
            row[g] = "?"

    best_row_idx = choose(header, rows, label)
    
    print("Analysis: Best working arrangement for Laboratory Technicians.")
    print(f"The best arrangement found is at row index: {best_row_idx}")
    print("This selection was based on sampling up to 50 laboratory staff members to identify the highest performance on retention-related metrics.")

import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff.
    We filter for this role, then sample up to 50 rows to find the one
    with the highest 'YearsAtCompany+' (a goal to maximize).
    """
    # Identify indices
    role_idx = header.index('jobRole')
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    # Filter for Laboratory Technicians
    # Note: rows passed to choose have '?' in the goal column, 
    # but the row structure remains consistent with the header.
    lab_indices = [i for i, row in enumerate(rows) if row[role_idx] == 'Laboratory Technician']
    
    # We can label at most 50 rows
    num_samples = min(50, len(lab_indices))
    sampled_indices = random.sample(lab_indices, num_samples)
    
    best_val = -float('inf')
    best_idx = -1
    
    # Determine if we are maximizing (+) or minimizing (-)
    is_maximize = header[goal_idx].endswith('+')
    
    for i in sampled_indices:
        # Query the true row data using the provided label function
        full_row = label(i)
        val = full_row[goal_idx]
        
        # Update best based on goal type
        if is_maximize:
            if val > best_val:
                best_val = val
                best_idx = i
        else:
            if best_idx == -1 or val < best_val:
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Mask the goal column for the harness
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    masked_rows = []
    for row in rows:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function
    def label(i):
        return rows[i]
        
    best_idx = choose(header, masked_rows, label)
    
    print("Analysis: Best working arrangement for Laboratory Technicians.")
    print(f"The best row found is at index: {best_idx}")
    print(f"Goal value ({header[goal_idx]}): {rows[best_idx][goal_idx]}")
    print("Strategy: Filtered for Laboratory Technicians and sampled up to 50 records to optimize the goal.")

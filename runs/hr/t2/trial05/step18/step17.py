import csv
import step07

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff
    by sampling up to 50 rows, prioritizing this specific job role.
    """
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    role_idx = header.index('jobRole')
    
    # Filter indices for Laboratory Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[role_idx] == 'Laboratory Technician']
    
    # If no lab techs, fall back to all rows
    if not lab_indices:
        lab_indices = list(range(len(rows)))
        
    # Sample up to 50 lab tech rows
    sample_size = min(50, len(lab_indices))
    # Pick indices spread across the lab tech population
    indices_to_sample = [lab_indices[int(i * (len(lab_indices) / sample_size))] for i in range(sample_size)]
    
    best_val = -1.0
    best_idx = -1
    
    for i in indices_to_sample:
        # Label the row to get the true goal value
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    
    # Create masked rows
    masked_rows = []
    for row in rows:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_rows.append(new_row)
        
    labeled_count = 0
    seen_labels = set()
    
    def label(i):
        global labeled_count
        if i not in seen_labels:
            labeled_count += 1
            if labeled_count > 50:
                raise Exception("Exceeded 50 labels")
            seen_labels.add(i)
        return [rows[i][goal_idx]]

    best_idx = choose(header, masked_rows, label)
    
    print(f"Best arrangement for Laboratory staff found at index {best_idx}.")
    print(f"YearsAtCompany+: {rows[best_idx][goal_idx]}")

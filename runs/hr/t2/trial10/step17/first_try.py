import csv
import step07

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff
    by sampling up to 50 rows.
    """
    # Identify the goal column index
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
    
    # Identify the jobRole column index
    role_idx = header.index('jobRole')
    
    # Filter indices for Laboratory Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[role_idx] == 'Laboratory Technician']
    
    # We can afford 50 interviews. 
    # If there are fewer than 50, sample all. If more, sample 50.
    if len(lab_indices) > 50:
        step = len(lab_indices) // 50
        indices_to_sample = [lab_indices[i * step] for i in range(50)]
    else:
        indices_to_sample = lab_indices
    
    best_idx = -1
    max_val = -float('inf')
    
    for i in indices_to_sample:
        # label(i) returns the full row as a list
        row_data = label(i)
        val = row_data[goal_idx]
        
        if val > max_val:
            max_val = val
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

    # Create a copy of rows with goals masked as '?'
    goal_idx = 31 # YearsAtCompany+
    masked_rows = [row[:] for row in rows]
    for row in masked_rows:
        row[goal_idx] = "?"

    # Define the label function for the harness
    def label(i):
        return rows[i]

    best_row_idx = choose(header, masked_rows, label)
    
    if best_row_idx != -1:
        print(f"After interviewing laboratory staff, the best working arrangement found is at row {best_row_idx}.")
        print(f"Tenure at this position: {rows[best_row_idx][goal_idx]} years.")
    else:
        print("No laboratory staff found to evaluate.")

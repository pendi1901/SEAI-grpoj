import csv

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows.
    'YearsAtCompany+' is a goal to maximize.
    label(i) returns the full row, so we extract the goal value.
    """
    # Identify the goal column index
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
    
    # We can afford 50 interviews. Sample 50 indices.
    # Using a step to sample the 800 rows.
    step = len(rows) // 50
    indices_to_sample = [i * step for i in range(50)]
    
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
    
    print(f"After interviewing 50 staff members, the best working arrangement found is at row {best_row_idx}.")
    print(f"Tenure at this position: {rows[best_row_idx][goal_idx]} years.")

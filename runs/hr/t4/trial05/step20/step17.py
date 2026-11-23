import csv
from step07 import choose as base_choose

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff
    by sampling up to 50 rows from that specific subset.
    """
    job_role_idx = header.index('jobRole')
    lab_indices = [i for i, row in enumerate(rows) if row[job_role_idx] == 'Laboratory Technician']
    
    # If no lab staff found, fallback to all indices
    if not lab_indices:
        lab_indices = list(range(len(rows)))
        
    # We need to select up to 50 indices from the lab_indices
    # We sample evenly to get a good representation
    n = len(lab_indices)
    sample_size = min(n, 50)
    indices_to_check = [lab_indices[int(i * n / sample_size)] for i in range(sample_size)]
    
    best_idx = -1
    max_score = -float('inf')
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    for i in indices_to_check:
        # Get true values using the provided label function
        true_vals = label(i)
        
        # Calculate score: sum of normalized goals (assuming + is better, - is worse)
        score = 0
        for j, g_idx in enumerate(goal_indices):
            val = true_vals[j]
            if header[g_idx].endswith('+'):
                score += val
            else:
                score -= val
        
        if score > max_score:
            max_score = score
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    labeled_data = {}
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]

    def label(i):
        if i not in labeled_data:
            if len(labeled_data) >= 50:
                raise ValueError("Limit of 50 labels exceeded.")
            labeled_data[i] = [rows[i][g] for g in goal_indices]
        return labeled_data[i]

    best_row_idx = choose(header, rows, label)
    
    print("Analysis: Best working arrangement for Laboratory Technicians.")
    print(f"The best row found is at index {best_row_idx}.")
    print(f"Job Role: {rows[best_row_idx][header.index('jobRole')]}")
    print(f"Years at company: {rows[best_row_idx][header.index('YearsAtCompany+')]}")

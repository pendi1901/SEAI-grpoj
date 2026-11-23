import csv
import step02
import step05
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff.
    Filters the dataset, then uses a model-based approach to find the best row
    while respecting the 50-label budget.
    """
    job_idx = header.index('jobRole')
    goal_idx = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
    is_maximize = header[goal_idx].endswith('+')
    
    # Filter for Lab Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[job_idx] == 'Laboratory Technician']
    
    if not lab_indices:
        return 0

    # Budget management
    labeled = {}
    def get_label(i):
        if i not in labeled:
            if len(labeled) >= 50:
                return None
            labeled[i] = label(i)[0]
        return labeled[i]

    # Strategy: Train a model on a small sample, then predict the best
    # Use 20% of lab staff (up to 50) to train
    sample_size = min(len(lab_indices), 20)
    train_indices = random.sample(lab_indices, sample_size)
    
    for i in train_indices:
        get_label(i)
        
    # Prepare training data
    train_data = []
    for i in train_indices:
        r = list(rows[i])
        r[goal_idx] = labeled[i]
        train_data.append(r)
        
    # Predict for all lab staff
    test_data = [rows[i] for i in lab_indices]
    preds = step02.guess(header, train_data, test_data)
    
    # Find best index
    if is_maximize:
        best_local_idx = preds.index(max(preds))
    else:
        best_local_idx = preds.index(min(preds))
        
    return lab_indices[best_local_idx]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)

    goal_idx = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
    
    def label(i):
        return [rows[i][goal_idx]]

    masked_rows = [list(r) for r in rows]
    for r in masked_rows: 
        r[goal_idx] = "?"

    best_idx = choose(header, masked_rows, label)
    
    print("Laboratory Staff Analysis:")
    print(f"The best working arrangement for Laboratory Technicians was found at index {best_idx}.")
    print("This was determined by filtering for lab roles and applying a model-based search strategy.")

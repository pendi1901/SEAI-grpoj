import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement for 'Laboratory Technician' staff
    using at most 50 labels.
    """
    # Filter rows for Laboratory Technician
    idx_role = header.index('jobRole')
    lab_rows = [r for r in rows if r[idx_role] == 'Laboratory Technician']
    
    if not lab_rows:
        return 0

    # Mask the goals in the rows passed to the table
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    def mask(row):
        new_row = list(row)
        for i in goal_indices:
            new_row[i] = "?"
        return new_row

    masked_rows = [mask(r) for r in lab_rows]
    tbl = ezr.Tbl([header] + masked_rows)
    
    # We track original indices relative to the filtered lab_rows list
    indexed_rows = list(enumerate(lab_rows))
    random.shuffle(indexed_rows)
    
    # Budget: 50 labels
    budget = 50
    # Store labeled rows as a list of tuples (index, full_row) to avoid unhashable issues
    labeled_data = [] 
    
    def get_label(idx, row):
        if not any(item[0] == idx for item in labeled_data):
            if len(labeled_data) >= budget:
                return None
            labeled_data.append((idx, label(row)))
        return next(item[1] for item in labeled_data if item[0] == idx)

    # Initial random sample
    start_n = min(len(indexed_rows), 4)
    for _ in range(start_n):
        idx, row = indexed_rows.pop()
        get_label(idx, row)
        
    # Greedy search for the remaining budget
    while len(labeled_data) < budget and indexed_rows:
        # Find the best in current labeled set
        best_idx, best_row = min(labeled_data, key=lambda x: ezr.ydist(tbl, x[1]))
        
        # Find worst in current labeled set to push away from
        worst_idx, worst_row = max(labeled_data, key=lambda x: ezr.ydist(tbl, x[1]))
        
        # Pick the next row that is most like 'best' and least like 'worst'
        sample_size = min(len(indexed_rows), 20)
        candidates = [indexed_rows.pop() for _ in range(sample_size)]
        
        next_idx, next_row = min(candidates, key=lambda x: ezr.xdist(tbl, x[1], best_row) - ezr.xdist(tbl, x[1], worst_row))
        
        get_label(next_idx, next_row)
        
        # Put the others back
        for c in candidates:
            if c[0] != next_idx:
                indexed_rows.append(c)
                
    # Return the index of the best row found
    best_final = min(labeled_data, key=lambda x: ezr.ydist(tbl, x[1]))
    return best_final[0]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    def oracle(row):
        return row

    best_idx = choose(header, rows, oracle)
    
    idx_role = header.index('jobRole')
    lab_rows = [r for r in rows if r[idx_role] == 'Laboratory Technician']
    best_row = lab_rows[best_idx]
    
    print("Optimal Working Arrangement for Laboratory Staff")
    print("-" * 50)
    print(f"Best Laboratory Technician Record Index: {best_idx}")
    print(f"YearsAtCompany+: {best_row[header.index('YearsAtCompany+')]}")
    print(f"YearsInCurrentRole+: {best_row[header.index('YearsInCurrentRole+')]}")
    print("-" * 50)
    print("This arrangement was identified using targeted interviews of lab staff.")

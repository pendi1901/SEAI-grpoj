import ezr
import random

def choose(header, rows, label):
    """
    Finds the best row for 'Laboratory Technician' staff by using a budget 
    of 50 labels and the 'acquire' strategy.
    """
    # 1. Filter for Laboratory Technicians
    job_role_idx = header.index('jobRole')
    # We keep track of the original indices to return the correct one
    indexed_rows = [(i, r) for i, r in enumerate(rows) if r[job_role_idx] == 'Laboratory Technician']
    lab_tech_rows = [r for i, r in indexed_rows]
    
    if not lab_tech_rows:
        return -1
    
    # 2. Setup table and tracking
    tbl = ezr.Tbl([header] + lab_tech_rows)
    # Map original index to labeled row
    labeled_cache = {}

    def oracle_wrapper(row):
        # Find the original index of this row
        # Since rows are passed by reference, we can identify them by identity
        idx = -1
        for i, r in indexed_rows:
            if r is row:
                idx = i
                break
        
        if idx not in labeled_cache:
            if len(labeled_cache) >= 50:
                raise Exception("Budget exceeded")
            labeled_cache[idx] = label(row)
        return labeled_cache[idx]

    # 3. Use acquire to find the best configuration
    # acquire returns a list of rows that have been labeled
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # 4. Find the best row among the labeled ones
    lab_tbl = ezr.Tbl([header] + labeled_rows)
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(lab_tbl, r))
    
    # 5. Return the index of the best row in the original 'rows' list
    for i, r in indexed_rows:
        if r is best_row:
            return i
    return -1

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def label_oracle(row):
        # Simulation: return the original row from the dataset
        for original_row in rows:
            match = True
            for i in range(len(header)):
                if i not in goal_indices and original_row[i] != row[i]:
                    match = False
                    break
            if match:
                return original_row
        return row

    # Prepare masked rows
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    best_idx = choose(header, masked_rows, label_oracle)
    
    print("Analysis: Optimal working arrangement for Laboratory Technicians.")
    print(f"The best configuration found is at record index: {best_idx}")
    print("This was determined by intelligently sampling 50 records to minimize")
    print("the distance to ideal organizational goals.")

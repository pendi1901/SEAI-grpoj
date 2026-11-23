import ezr
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff
    using at most 50 labels.
    """
    # Filter rows for Laboratory Technician
    job_idx = header.index('jobRole')
    lab_indices = [i for i, r in enumerate(rows) if r[job_idx] == 'Laboratory Technician']
    
    if not lab_indices:
        return 0

    # Create a table to manage column definitions and ydist calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Track labeled rows
    labeled_indices = {}
    
    def get_labeled_row(idx):
        if idx not in labeled_indices:
            if len(labeled_indices) >= 50:
                raise Exception("Budget exceeded")
            labeled_indices[idx] = label(rows[idx])
        return labeled_indices[idx]

    # Bootstrap with a few random samples from the lab staff
    sample_size = min(len(lab_indices), ezr.the.Start)
    for i in random.sample(lab_indices, sample_size):
        get_labeled_row(i)
        
    # Iteratively pick the next best row to label
    while len(labeled_indices) < 50 and len(labeled_indices) < len(lab_indices):
        labeled_rows = [labeled_indices[i] for i in labeled_indices]
        lab_tbl = ezr.clone(tbl, labeled_rows)
        rank_fn = ezr.ranker(lab_tbl)
        
        unlabeled = [i for i in lab_indices if i not in labeled_indices]
        if not unlabeled:
            break
        
        # Pick the row that the model thinks is best
        best_unlabeled = min(unlabeled, key=lambda i: rank_fn(rows[i]))
        get_labeled_row(best_unlabeled)
        
    # Return the index of the best row found
    return min(labeled_indices.keys(), key=lambda i: ezr.ydist(tbl, labeled_indices[i]))

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for i in goal_indices:
            new_row[i] = "?"
        masked_rows.append(new_row)
        
    def label(row):
        # Return the original row (ground truth)
        idx = rows.index(row)
        return rows[idx]

    best_idx = choose(header, masked_rows, label)
    
    print("Analysis: Optimal working arrangement for Laboratory Technicians.")
    print("-" * 60)
    print(f"Identified optimal record at index: {best_idx}")
    best_row = rows[best_idx]
    print(f"Role: {best_row[header.index('jobRole')]}")
    print(f"Total Working Years: {best_row[header.index('TotalWorkingYears')]}")
    print(f"Monthly Income: {best_row[header.index('MonthlyIncome')]}")
    print("-" * 60)
    print("This selection was made using an active learning strategy")
    print("targeting only Laboratory Technician staff.")

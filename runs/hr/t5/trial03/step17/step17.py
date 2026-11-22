import ezr
import random

def choose(header, rows, label):
    """
    Finds the best row for 'Laboratory Technician' staff by using the 
    'acquire' strategy from ezr, restricted to that job role.
    """
    # Identify the jobRole column index
    job_role_idx = header.index('jobRole')
    
    # Filter rows to only include Laboratory Technicians
    lab_tech_indices = [i for i, row in enumerate(rows) if row[job_role_idx] == 'Laboratory Technician']
    
    # If no lab techs found, return 0 as a fallback
    if not lab_tech_indices:
        return 0
    
    # Extract the lab tech rows
    lab_tech_rows = [rows[i] for i in lab_tech_indices]
    
    # Create a table object for the lab tech subset
    tbl = ezr.Tbl([header] + lab_tech_rows)
    
    # Set the budget to 50 as per the customer's request
    ezr.the.Stop = 50
    
    # Define the oracle to reveal goals for the original row index
    def oracle_wrapper(row):
        # Find the original index of this row in the full 'rows' list
        # We search by comparing the row content
        idx = -1
        for i in lab_tech_indices:
            if rows[i] == row:
                idx = i
                break
        
        goals = label(idx)
        # Update the row with the revealed goals
        goal_indices = [i for i, name in enumerate(header) 
                        if name.endswith(("+", "-"))]
        for i, g_idx in enumerate(goal_indices):
            row[g_idx] = goals[i]
        return row

    # Acquire labels and get the best rows
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones based on ydist
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the original index of the best row found
    for i in lab_tech_indices:
        if rows[i] == best_row:
            return i
    return lab_tech_indices[0]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Keep a copy of original rows to reveal goals
    original_rows = [list(r) for r in rows]
    
    # Mask goals for the choose function
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    masked_rows = []
    for r in rows:
        new_r = list(r)
        for idx in goal_indices:
            new_r[idx] = "?"
        masked_rows.append(new_r)
        
    # Define the label function for the harness
    def label(i):
        return [original_rows[i][idx] for idx in goal_indices]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label)
    
    print(f"Analysis complete for Laboratory Technician staff.")
    print(f"The best working arrangement found is at row index: {best_idx}")
    print(f"Years at Company for this employee: {original_rows[best_idx][header.index('YearsAtCompany+')]}")
    
    exit(0)

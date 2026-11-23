import ezr
import step07

def choose(header, rows, label):
    """
    Finds the best row for laboratory staff by filtering the dataset
    and using the acquire strategy to find the best arrangement.
    """
    # Identify the jobRole column
    col_map = {name: i for i, name in enumerate(header)}
    role_idx = col_map['jobRole']
    
    # Filter rows for 'Laboratory Technician'
    # We must keep the rows as they are (with '?' in goals)
    lab_staff_indices = [i for i, r in enumerate(rows) if r[role_idx] == 'Laboratory Technician']
    lab_staff_rows = [rows[i] for i in lab_staff_indices]
    
    # The error in step07 was caused by Tbl() trying to process rows with '?'
    # in goal columns. We must provide a table that has valid goal data.
    # Since we can only label 50 rows, we label a small initial set to 
    # initialize the table correctly.
    
    labeled_cache = {}
    def oracle_wrapper(idx):
        if idx not in labeled_cache:
            labeled_cache[idx] = label(idx)
        return labeled_cache[idx]

    # Initialize table with a few labeled rows to define the goal columns
    initial_count = min(len(lab_staff_indices), 5)
    for i in range(initial_count):
        oracle_wrapper(lab_staff_indices[i])
        
    # Create the table using the header and the labeled rows
    labeled_data = [labeled_cache[idx] for idx in lab_staff_indices if idx in labeled_cache]
    tbl = ezr.Tbl([header] + labeled_data)
    
    # Now use acquire to find the best row
    # We need to pass a function that labels the row and updates the table
    def label_func(row):
        # Find original index
        # We search for the row in our subset
        for i, r in enumerate(lab_staff_rows):
            if r is row:
                return oracle_wrapper(lab_staff_indices[i])
        return row

    # Use acquire to select rows to label
    # We pass the table and the oracle
    best_row = min(ezr.acquire(tbl, cap=50, label=label_func), 
                   key=lambda r: ezr.ydist(tbl, r))
    
    # Find the original index of the best row
    for i, r in enumerate(lab_staff_rows):
        if r is best_row:
            return lab_staff_indices[i]
    return lab_staff_indices[0]

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    def label(i):
        return rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label)
    
    # Print result
    print(f"Best laboratory staff arrangement found at index: {best_idx}")
    print("This row was identified using targeted interviews within the lab staff group.")
    print(f"Goal metrics (tenure/role duration) for this row: {rows[best_idx][-4:]}")
    
    exit(0)

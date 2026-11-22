import ezr
import random

def choose(header, rows, label):
    """
    Finds the best row by using the 'acquire' strategy from ezr.
    We are allowed 50 labels. We use the 'acquire' function which 
    intelligently selects rows to label to find the best ones.
    """
    # Create a table object. The rows currently have '?' for goals.
    # The label function will be used to reveal them.
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function in ezr uses the label function to reveal 
    # goal values for a subset of rows (up to the.Stop budget).
    # We set the budget to 50 as per the customer's request.
    ezr.the.Stop = 50
    
    # We need to wrap the provided 'label' function to match the 
    # expected signature of the acquire function.
    def oracle_wrapper(row):
        # Find the index of this row in the original rows list
        # to call the provided label(i) function.
        idx = rows.index(row)
        goals = label(idx)
        # Update the row with the revealed goals
        goal_indices = [i for i, name in enumerate(header) 
                        if name.endswith(("+", "-"))]
        for i, g_idx in enumerate(goal_indices):
            row[g_idx] = goals[i]
        return row

    # Acquire labels and get the best rows
    # 'both' contains the rows that were labeled
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found
    return rows.index(best_row)

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
    
    print(f"Analysis complete.")
    print(f"The best working arrangement found is at row index: {best_idx}")
    print(f"Years at Company for this employee: {original_rows[best_idx][header.index('YearsAtCompany+')]}")
    
    exit(0)

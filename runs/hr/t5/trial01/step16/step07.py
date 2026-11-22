import ezr
import random

def choose(header, rows, label):
    """
    Finds the best row by using a budget of 50 labels.
    We use the 'acquire' strategy from ezr to intelligently sample 
    the most informative rows to build a model, then return the 
    index of the best row found.
    """
    # Create a table structure to manage the data
    tbl = ezr.Tbl([header] + rows)
    
    # We need to track which original index was labeled.
    # Since rows are lists (unhashable), we map them by their memory ID or index.
    # We use a dictionary to store the true row values once labeled.
    labeled_results = {}
    
    def oracle_wrapper(row):
        # Find the original index of this row
        # We use the fact that rows are passed by reference
        idx = -1
        for i, r in enumerate(rows):
            if r is row:
                idx = i
                break
        
        true_row = label(row)
        labeled_results[idx] = true_row
        return true_row

    # Use ezr.acquire to spend the budget of 50 labels.
    # The acquire function will call our oracle_wrapper.
    ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Now we have the true goal values for the sampled rows.
    # We find the best one among these labeled rows.
    best_idx = -1
    best_ydist = 1e30
    
    # Create a temporary table with the labeled data to calculate ydist
    labeled_rows = list(labeled_results.values())
    lab_tbl = ezr.Tbl([header] + labeled_rows)
    
    for idx, row in labeled_results.items():
        d = ezr.ydist(lab_tbl, row)
        if d < best_ydist:
            best_ydist = d
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals for the choose function
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def label_oracle(row):
        # In the real scenario, this returns the full row.
        # We find the original row in the data to return its true values.
        # This is a simulation of the oracle.
        for original_row in rows:
            # Check if this is the row (by comparing non-goal values)
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
        
    # Run the selection
    best_idx = choose(header, masked_rows, label_oracle)
    
    print(f"Analysis complete.")
    print(f"The best working arrangement found is at record index: {best_idx}")
    print("This record was identified as the optimal configuration based on")
    print("the 50-interview budget and goal optimization criteria.")

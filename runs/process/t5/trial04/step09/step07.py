import ezr
import random

def choose(header, rows, label):
    """
    Find the best row by using the acquire strategy to intelligently
    sample the search space within a budget of 50 labels.
    """
    # Create a table structure to manage the data
    # We use the provided rows (which have '?' in goals)
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function in ezr is designed to find the best rows
    # by balancing exploration and exploitation.
    # It returns a list of rows that have been labeled.
    # We set the budget to 50 as requested.
    
    # We need to wrap the label function to track indices
    # because acquire expects an oracle that returns a full row.
    labeled_data = []
    
    def oracle_wrapper(row):
        # Find the index of the row in the original list
        # Since rows are unique in this dataset, we can match by content
        for i, r in enumerate(rows):
            if r == row:
                # Call the provided label function
                true_goals = label(i)
                # Update the row with the true goal values
                new_row = list(row)
                goal_indices = [j for j, name in enumerate(header) 
                                if name.endswith(('-', '+'))]
                for idx, val in zip(goal_indices, true_goals):
                    new_row[idx] = val
                return new_row
        return row

    # Use ezr's acquire to perform the search
    # It will call our oracle_wrapper up to 50 times
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # After labeling, find the best row among the labeled ones
    # ydist measures distance to the ideal goal values (lower is better)
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found
    for i, r in enumerate(rows):
        if r == best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Prepare rows for the choose function (masking goals)
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    def label_func(i):
        # Return the true goal values from the original data
        return [all_rows[i][idx] for idx in goal_indices]
        
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Search complete. Best setup found at index: {best_idx}")
    print("This setup was identified using a 50-label budget strategy.")
    exit(0)

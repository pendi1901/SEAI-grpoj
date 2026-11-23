import ezr
import random

def choose(header, rows, label):
    """
    Find the best row using a budget of 50 labels.
    We use the 'acquire' strategy from ezr to intelligently sample 
    the search space. Since goal cells are '?', we must label them.
    """
    # We need to track the original indices
    indexed_rows = []
    for i, row in enumerate(rows):
        indexed_rows.append([i, row])
    
    # The acquire function needs a TBL. We create one from the rows.
    # Note: ezr.Tbl expects rows to have values. Since our goals are '?',
    # we must label some rows first to initialize the TBL properly.
    
    # 1. Initial random sample to get some data
    start_budget = min(len(rows), ezr.the.Start)
    sampled_indices = random.sample(range(len(rows)), start_budget)
    
    labeled_rows = []
    for i in sampled_indices:
        goals = label(i)
        row = rows[i]
        # Update row with goals
        goal_indices = [j for j, name in enumerate(header) if name.endswith(('-', '+'))]
        for idx, val in zip(goal_indices, goals):
            row[idx] = val
        labeled_rows.append(row)
    
    # 2. Create the TBL with the labeled data
    tbl = ezr.Tbl([header] + labeled_rows)
    
    # 3. Define an oracle that updates the row and the TBL
    def oracle_wrapper(row):
        # Find index of this row
        for i, r in enumerate(rows):
            if r is row:
                # If goals are already filled (from initial sample), return
                if row[header.index("Cost-")] != "?":
                    return row
                # Otherwise, label it
                goals = label(i)
                goal_indices = [j for j, name in enumerate(header) if name.endswith(('-', '+'))]
                for idx, val in zip(goal_indices, goals):
                    row[idx] = val
                ezr.addRow(tbl, row)
                return row
        return row

    # 4. Use ezr.acquire to find the best rows within the budget
    # We pass the tbl which now has some data
    best_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # 5. Find the best row among all labeled rows
    best_row = min(best_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    for i, r in enumerate(rows):
        if r is best_row:
            return i
    return 0

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals as per requirements
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    # Define the label function
    full_data = list(ezr.csv(filename))
    full_rows = full_data[1:]
    
    def label(i):
        return [full_rows[i][idx] for idx in goal_indices]
    
    # Run the choice
    best_idx = choose(header, rows, label)
    
    print(f"Optimization complete.")
    print(f"The best setup found is at index: {best_idx}")
    print(f"Goal values for this setup: {label(best_idx)}")
    
    exit(0)

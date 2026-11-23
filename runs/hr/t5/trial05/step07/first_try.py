import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement using at most 50 labels.
    We use the 'acquire' strategy from ezr to intelligently sample 
    the search space and identify the row with the best goal outcomes.
    """
    # Create a table object. The goal columns are marked with + or -
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function uses the budget (the.Stop=50) to sample
    # rows that are near the best-performing regions of the space.
    # It returns the rows that were labeled.
    labeled_rows = ezr.acquire(tbl, cap=50, label=label)
    
    # After labeling, we want to find the single best row among those labeled.
    # ydist measures how far a row is from the ideal goal values.
    # Lower ydist is better.
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found
    # We find it by matching the row content (EmployeeNumber is unique)
    # or by index if we track the original position.
    # Since we need the index in the original 'rows' list:
    for i, row in enumerate(rows):
        if row == best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # The oracle function that reveals the hidden goal values
    def oracle(row):
        # In this simulation, we know the true values are in the original row
        # We return the full row to the caller
        return row

    # Run the selection process
    best_idx = choose(header, rows, oracle)
    best_row = rows[best_idx]
    
    print("Optimal Working Arrangement Found")
    print("-" * 50)
    print(f"Best Employee Record Index: {best_idx}")
    print(f"YearsAtCompany+: {best_row[header.index('YearsAtCompany+')]}")
    print(f"YearsInCurrentRole+: {best_row[header.index('YearsInCurrentRole+')]}")
    print(f"JobRole: {best_row[header.index('jobRole')]}")
    print("-" * 50)
    print("This arrangement was identified using 50 targeted interviews.")

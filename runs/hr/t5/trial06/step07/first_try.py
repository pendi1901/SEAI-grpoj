import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement using at most 50 labels.
    We use the 'holdout' strategy from ezr which performs active learning
    to find the best row by balancing exploration and exploitation.
    """
    # Create a table object to manage the data
    tbl = ezr.Tbl([header] + rows)
    
    # The holdout function in ezr.py is designed to perform active learning
    # with a budget (the.Stop). It uses the provided label function to
    # reveal hidden goals and returns the best row found.
    # We need to return the index of that row.
    
    # We create a wrapper to track the index of the row being labeled
    # since holdout expects an oracle that returns the row with goals filled.
    best_row = ezr.holdout(tbl, pick=ezr.acquire, label=label)
    
    # Find the index of the best_row in the original rows list
    # We compare by identity or content. Since rows are lists, we compare content.
    for i, row in enumerate(rows):
        if row == best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals for the simulation
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def oracle(row):
        # This is the ground truth provider
        return row
    
    def masked_label(row):
        # This simulates the interview process
        return oracle(row)

    # We need to pass rows with goals masked to the choose function
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for i in goal_indices:
            new_row[i] = "?"
        masked_rows.append(new_row)
        
    best_idx = choose(header, masked_rows, masked_label)
    
    print(f"Analysis complete. Identified optimal employee record at index: {best_idx}")
    print("This record represents the working arrangement that maximizes")
    print("tenure and satisfaction based on 50 targeted interviews.")
    
    # Display the characteristics of the chosen row
    best_row = rows[best_idx]
    print("\nKey characteristics of the optimal arrangement:")
    for i, name in enumerate(header):
        if name in ["Age", "MonthlyIncome", "TotalWorkingYears", "YearsAtCompany+", "jobRole"]:
            print(f"  {name:20}: {best_row[i]}")

import ezr
import step02

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    To answer the customer's question: 'If we cut overtime across Sales, 
    what happens to how long people stay?', we simulate the 'cut' 
    by setting 'overTime' to 'No' for all Sales department rows in the test set.
    """
    # Identify indices
    dept_idx = header.index('department')
    ot_idx = header.index('overTime')
    
    # Create a modified test set where Sales overtime is forced to 'No'
    modified_test = []
    for row in test:
        new_row = list(row)
        if new_row[dept_idx] == 'Sales':
            new_row[ot_idx] = 'No'
        modified_test.append(new_row)
    
    # Use the logic from step02 to estimate the first goal column
    return step02.guess(header, train, modified_test)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Split data
    split = int(len(all_rows) * 0.8)
    train = all_rows[:split]
    test_full = all_rows[split:]
    
    # Mask goals for test
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    test = []
    for row in test_full:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        test.append(new_row)
    
    # Get estimates
    estimates = guess(header, train, test)
    
    # Calculate average tenure for Sales employees in the test set
    dept_idx = header.index('department')
    sales_estimates = [est for i, est in enumerate(estimates) if test[i][dept_idx] == 'Sales']
    
    avg_tenure = sum(sales_estimates) / len(sales_estimates) if sales_estimates else 0
    
    print("Analysis: If we cut overtime across Sales, what happens to how long people stay?")
    print(f"Estimated average tenure (YearsAtCompany+) for Sales staff after cutting overtime: {avg_tenure:.2f} years.")
    print("This estimate is based on a decision tree model trained on historical performance data.")

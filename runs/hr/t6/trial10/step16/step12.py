import ezr
import step02
import step03

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    We simulate the impact of cutting overtime by setting 'overTime' to 'No'
    for all test rows before estimation.
    """
    # Identify indices
    ot_idx = header.index('overTime')
    
    # Modify test rows to simulate "cutting overtime"
    modified_test = []
    for row in test:
        new_row = list(row)
        new_row[ot_idx] = 'No'
        modified_test.append(new_row)
        
    # Use the logic from step02 to estimate the goal
    return step02.guess(header, train, modified_test)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Filter for Sales department
    dept_idx = header.index('department')
    sales_rows = [r for r in rows if r[dept_idx] == 'Sales']
    
    # Split into train and test
    n = int(len(sales_rows) * 0.8)
    train = sales_rows[:n]
    test_full = sales_rows[n:]
    
    # Mask goals for test
    test = []
    for row in test_full:
        new_row = list(row)
        for i, name in enumerate(header):
            if name.endswith("+") or name.endswith("-"):
                new_row[i] = "?"
        test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, test)
    
    print("Analysis: If we cut overtime across Sales, what happens to tenure?")
    print(f"Estimated average 'YearsAtCompany+' for Sales staff (with overtime cut): "
          f"{sum(estimates)/len(estimates):.2f} years.")
    print("Logic: By setting 'overTime' to 'No' for all test records, we observe "
          "the model's prediction for tenure under the new policy.")

import csv
import step02

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    To answer the customer's question: 'If we cut overtime across Sales, 
    what happens to how long people stay?', we simulate the effect by 
    setting 'overTime' to 'No' for all Sales department rows in the test set 
    and using k-NN to estimate the impact based on the training data.
    """
    # Identify the first goal column
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    # Identify indices
    ot_idx = header.index('overTime')
    dept_idx = header.index('department')
    
    # Prepare modified test data: Force 'overTime' to 'No' for 'Sales'
    modified_test = []
    for row in test:
        new_row = list(row)
        if new_row[dept_idx] == 'Sales':
            new_row[ot_idx] = 'No'
        modified_test.append(new_row)
    
    # Use the k-NN logic from step02 to estimate the goal
    return step02.guess(header, train, modified_test)

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # To answer the question, we compare the average 'YearsAtCompany+' 
    # of Sales employees with Overtime vs the estimated average if Overtime was 'No'.
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    ot_idx = header.index('overTime')
    dept_idx = header.index('department')
    
    sales_with_ot = [r[goal_idx] for r in rows if r[dept_idx] == 'Sales' and r[ot_idx] == 'Yes']
    
    # Create a test set of all Sales employees currently working overtime
    test_rows = [r for r in rows if r[dept_idx] == 'Sales' and r[ot_idx] == 'Yes']
    
    # Estimate their stay duration if overtime were removed
    estimates = guess(header, rows, test_rows)
    
    avg_current = sum(sales_with_ot) / len(sales_with_ot) if sales_with_ot else 0
    avg_estimated = sum(estimates) / len(estimates) if estimates else 0
    
    print("Analysis: Impact of cutting overtime in Sales on 'YearsAtCompany+'")
    print(f"Current average stay for Sales employees with overtime: {avg_current:.2f} years")
    print(f"Estimated average stay if overtime is removed: {avg_estimated:.2f} years")
    print("Conclusion: " + ("Removing overtime is projected to increase retention." 
          if avg_estimated > avg_current else "Removing overtime is not projected to increase retention."))

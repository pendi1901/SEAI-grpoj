import ezr
import random
import step02

def guess(header, train, test):
    """
    Estimates the first goal column (YearsAtCompany+) for test rows
    by building a tree on the training data and predicting the mean
    value of the leaf node where the test row lands.
    """
    return step02.guess(header, train, test)

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Identify the first goal column
    col_map = {name: i for i, name in enumerate(header)}
    goal_idx = col_map['YearsAtCompany+']
    dept_idx = col_map['department']
    ot_idx = col_map['overTime']
    
    # Filter for Sales department
    sales_rows = [r for r in rows if r[dept_idx] == 'Sales']
    
    # Create two scenarios: current (keep as is) and intervention (force overTime = 'No')
    # We use the training data to build the model, then predict for the Sales population
    train = rows
    
    # Scenario 1: Baseline (Sales employees)
    test_baseline = [list(r) for r in sales_rows]
    for r in test_baseline:
        for i, name in enumerate(header):
            if name.endswith(('-', '+')): r[i] = "?"
            
    # Scenario 2: Intervention (Sales employees with Overtime set to 'No')
    test_intervention = [list(r) for r in sales_rows]
    for r in test_intervention:
        r[ot_idx] = 'No'
        for i, name in enumerate(header):
            if name.endswith(('-', '+')): r[i] = "?"
            
    # Get predictions
    preds_baseline = guess(header, train, test_baseline)
    preds_intervention = guess(header, train, test_intervention)
    
    avg_baseline = sum(preds_baseline) / len(preds_baseline)
    avg_intervention = sum(preds_intervention) / len(preds_intervention)
    
    print("Analysis: Impact of cutting overtime in the Sales department.")
    print(f"Baseline average tenure: {avg_baseline:.2f} years.")
    print(f"Predicted average tenure if overtime is cut: {avg_intervention:.2f} years.")
    print(f"Estimated change: {avg_intervention - avg_baseline:+.2f} years.")
    
    exit(0)

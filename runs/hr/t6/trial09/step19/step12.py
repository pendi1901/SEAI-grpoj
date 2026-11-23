import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row by finding the 
    nearest neighbor in the training set based on x-columns.
    """
    # Create a table from training data to use ezr's distance functions
    tbl = ezr.Tbl([header] + train)
    
    # Identify the first goal column index
    # Goals are columns ending in '+' or '-'
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    first_goal_idx = goal_indices[0]
    
    results = []
    for t_row in test:
        # Find the row in training data that is closest in x-space
        # xdist uses only the input columns
        best_row = min(train, key=lambda r: ezr.xdist(tbl, t_row, r))
        results.append(best_row[first_goal_idx])
        
    return results

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify indices
    ot_idx = header.index('overTime')
    dept_idx = header.index('department')
    yac_idx = header.index('YearsAtCompany+')
    
    # Filter for Sales department
    sales_rows = [r for r in rows if r[dept_idx] == 'Sales']
    
    # Split into two groups: those with Overtime and those without
    with_ot = [r for r in sales_rows if r[ot_idx] == 'Yes']
    without_ot = [r for r in sales_rows if r[ot_idx] == 'No']
    
    # Calculate average years at company for both
    avg_with = sum(r[yac_idx] for r in with_ot) / len(with_ot)
    avg_without = sum(r[yac_idx] for r in without_ot) / len(without_ot)
    
    print("Analysis: If we cut overtime across Sales, what happens to how long people stay?")
    print(f"Average 'YearsAtCompany+' for Sales (with Overtime): {avg_with:.2f} years.")
    print(f"Average 'YearsAtCompany+' for Sales (without Overtime): {avg_without:.2f} years.")
    
    diff = avg_without - avg_with
    if diff > 0:
        print(f"Conclusion: Cutting overtime in Sales is associated with an increase of {diff:.2f} years in tenure.")
    else:
        print("Conclusion: Cutting overtime in Sales shows no clear increase in tenure.")
        
    exit(0)

import csv
import step02

def guess(header, train, test):
    """
    Estimates the first goal column (YearsAtCompany+) by calculating the 
    average tenure of employees in the 'Sales' department who do not work overtime.
    """
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
            
    dept_idx = header.index('department')
    ot_idx = header.index('overTime')
    
    # Filter training data for Sales employees who do not work overtime
    subset = [r[goal_idx] for r in train 
              if r[dept_idx] == 'Sales' and r[ot_idx] == 'No']
    
    # If no such employees exist, fallback to the global average using step02
    if not subset:
        return step02.guess(header, train, test)
    
    avg_tenure = sum(subset) / len(subset)
    return [float(avg_tenure)] * len(test)

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            new_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        new_row.append(float(val))
                    except ValueError:
                        new_row.append(0.0)
                else:
                    new_row.append(val)
            rows.append(new_row)
            
    # Simulate the scenario: Sales employees who do not work overtime
    # We create a dummy test row to see the estimated tenure
    test_row = [0.0] * len(header)
    test_row[header.index('department')] = 'Sales'
    test_row[header.index('overTime')] = 'No'
    
    goal_idx = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
    test_row[goal_idx] = "?"
    
    prediction = guess(header, rows, [test_row])[0]
    
    print("Analysis: Impact of cutting overtime in Sales on tenure.")
    print(f"Estimated average tenure for Sales staff without overtime: {prediction:.2f} years.")
    print("This suggests that removing overtime requirements in Sales may align "
          "with this average tenure duration.")

import csv

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal metrics without 
    using pay-related levers. We focus on structural and work-life balance 
    levers like 'overTime', 'businessTravel', and 'TrainingTimesLastYear'.
    """
    recommendations = {}
    
    # We explicitly exclude any pay-related columns if they were passed in levers
    # (e.g., PercentSalaryHike, MonthlyIncome)
    pay_keywords = ['Salary', 'Income', 'Stock']
    
    for col, allowed in levers.items():
        # Skip pay-related levers
        if any(k in col for k in pay_keywords):
            continue
            
        idx = header.index(col)
        current_val = row[idx]
        
        if isinstance(allowed, tuple):  # Numeric lever (low, high)
            low, high = allowed
            # If current is low, push towards high to improve engagement
            if current_val < high:
                recommendations[col] = min(current_val + 1.0, high)
        else:  # Symbolic lever (list of options)
            # If current is 'Yes'/'No' or specific travel, try to switch
            if current_val in allowed:
                for option in allowed:
                    if option != current_val:
                        recommendations[col] = option
                        break
    
    # Fallback: if no non-pay levers were provided or found, pick the first available
    if not recommendations:
        for col, allowed in levers.items():
            if any(k in col for k in pay_keywords): continue
            if isinstance(allowed, tuple):
                recommendations[col] = allowed[1]
            else:
                recommendations[col] = allowed[0]
            break
            
    return recommendations

def load_data(filename):
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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    return header, rows

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    header, rows = load_data(filename)
    
    # Define non-monetary levers
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'JobInvolvement': (1.0, 4.0)
    }
    
    # Example: Fix the first row
    bad_row = rows[0]
    changes = fix(header, bad_row, levers)
    
    print("Since budget for pay increases is unavailable, we recommend the following structural adjustments:")
    for col, val in changes.items():
        print(f"- Change '{col}' to {val}")
    
    print("\nStrategy: We prioritize non-monetary levers such as optimizing travel requirements, "
          "reducing overtime, and increasing training opportunities to improve employee retention.")

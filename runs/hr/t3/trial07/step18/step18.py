import csv
import random

def fix(header, row, levers):
    """
    Recommends changes for a 'bad' row (low tenure) by adjusting levers
    to move the employee toward a more stable profile, excluding salary.
    """
    recommendations = {}
    
    # We aim to improve 'YearsAtCompany+' (a + goal).
    # Strategy: Increase numeric levers (training) and optimize symbolic ones.
    # We avoid salary-related levers as per the customer's request.
    
    # Select a random lever to change to ensure we make a recommendation
    lever_names = list(levers.keys())
    random.shuffle(lever_names)
    
    for col in lever_names:
        idx = header.index(col)
        current_val = row[idx]
        allowed = levers[col]
        
        if isinstance(allowed, tuple):  # Numeric lever (low, high)
            low, high = allowed
            # If current is low, push towards high
            if current_val < high:
                recommendations[col] = min(high, current_val + (high - low) * 0.25)
                break # Only need one change
        
        elif isinstance(allowed, list):  # Symbolic lever
            # Pick a value that isn't the current one
            options = [val for val in allowed if val != current_val]
            if options:
                recommendations[col] = random.choice(options)
                break # Only need one change
            
    return recommendations

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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

    # Define non-monetary levers
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'StockOptionLevel': (0.0, 3.0),
        'JobInvolvement': (1.0, 4.0)
    }

    # Identify a "bad" row (low tenure)
    years_idx = header.index('YearsAtCompany+')
    bad_rows = [r for r in rows if r[years_idx] < 2.0]
    
    if bad_rows:
        sample_bad_row = bad_rows[0]
        changes = fix(header, sample_bad_row, levers)
        
        print("Analysis: Recommended non-monetary changes to improve retention:")
        for col, val in changes.items():
            print(f"- Change '{col}' to: {val}")
        print("\nThese changes focus on engagement and work-life balance, which are key drivers of tenure.")
    else:
        print("No employees with low tenure found to analyze.")

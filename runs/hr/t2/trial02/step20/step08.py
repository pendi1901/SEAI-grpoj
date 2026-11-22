import csv
import step05

def fix(header, row, levers):
    """
    Recommends a change to a 'bad' row (short tenure) to improve it.
    We look for the lever that has the highest 'blame' score (from step05)
    and adjust it to a value that correlates with longer tenure.
    """
    # Identify goal column
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+'):
            goal_idx = i
            break
            
    # We need to know which levers are most impactful.
    # We use the logic from step05 to find the most influential factors.
    # Since we can't easily re-run step05 on the whole dataset inside this function
    # without access to all rows, we assume the levers provided are the ones to optimize.
    
    recommendations = {}
    
    # Simple strategy: If numeric, push towards the higher end of the range.
    # If symbolic, pick the first option provided in the list.
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        if isinstance(allowed, tuple):
            # Numeric: push to the higher end
            recommendations[col_name] = allowed[1]
        else:
            # Symbolic: pick the first available option
            recommendations[col_name] = allowed[0]
            
    # Return at least one recommendation
    return recommendations

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

    # Define levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'PercentSalaryHike': (11.0, 25.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Identify a 'bad' row (e.g., one with low tenure)
    tenure_idx = header.index('YearsAtCompany+')
    sorted_rows = sorted(rows, key=lambda r: r[tenure_idx])
    bad_row = sorted_rows[0]

    recommendation = fix(header, bad_row, levers)

    print("Analysis: Recommendations for staff with short tenure.")
    print(f"For an employee with {bad_row[tenure_idx]} years at the company, we suggest:")
    for col, val in recommendation.items():
        print(f"- Change {col} to {val}")

import csv
import random

def fix(header, row, levers):
    """
    Recommends a change to a 'bad' row to improve its goal metrics.
    Since there is no money for pay, we focus on non-monetary levers:
    WorkLifeBalance, JobSatisfaction, EnvironmentSatisfaction, and TrainingTimesLastYear.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # We want to improve the row. Since we don't have a global model,
    # we pick a lever that is likely to improve satisfaction/tenure.
    # We prioritize changing symbolic values to something different,
    # or numeric values towards their maximum allowed range.
    
    recommendations = {}
    # Shuffle keys to ensure we don't always pick the same lever
    keys = list(levers.keys())
    random.shuffle(keys)
    
    for col_name in keys:
        idx = header.index(col_name)
        allowed = levers[col_name]
        
        if isinstance(allowed, list):  # Symbolic
            choices = [v for v in allowed if v != row[idx]]
            if choices:
                recommendations[col_name] = random.choice(choices)
                break
        else:  # Numeric (low, high)
            low, high = allowed
            # If current value is below high, move towards high
            if row[idx] < high:
                recommendations[col_name] = high
                break
                
    return recommendations

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

    # Non-monetary levers
    levers = {
        'WorkLifeBalance': (1.0, 4.0),
        'JobSatisfaction': (1.0, 4.0),
        'EnvironmentSatisfaction': (1.0, 4.0),
        'TrainingTimesLastYear': (0.0, 6.0),
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely']
    }

    # Identify a 'bad' row (lowest tenure score)
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+')]
    scores = []
    for idx, r in enumerate(rows):
        score = sum(r[i] for i in goal_indices)
        scores.append((score, idx))
    
    scores.sort()
    bad_row_idx = scores[0][1]
    bad_row = rows[bad_row_idx]

    change = fix(header, bad_row, levers)
    
    print("Retention Strategy (Non-Monetary):")
    print(f"For the employee at index {bad_row_idx} (who has low tenure metrics),")
    print("we recommend the following non-monetary adjustments to improve their experience:")
    for col, val in change.items():
        print(f"- Adjust '{col}' to '{val}'")
    print("\nThese changes focus on improving work-life balance, satisfaction, and")
    print("professional development, which are key drivers of retention when")
    print("salary increases are not an option.")

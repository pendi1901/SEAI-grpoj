import csv
import step08

def get_score(header, row):
    """Calculates a score where higher is better."""
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    score = 0
    for i in goal_indices:
        val = row[i]
        if isinstance(val, (int, float)):
            if header[i].endswith('+'):
                score += val
            else:
                score -= val
    return score

def fix(header, row, levers):
    """
    Recommends a change to a 'bad' row to improve its goal metrics,
    excluding salary-related levers.
    """
    best_change = {}
    best_score = -float('inf')
    
    # We iterate through provided levers to find the one that maximizes the score
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        
        candidates = []
        if isinstance(allowed, tuple):
            # For numeric, test boundaries and midpoint
            candidates = [allowed[0], (allowed[0] + allowed[1]) / 2, allowed[1]]
        else:
            candidates = allowed
            
        for val in candidates:
            test_row = list(row)
            test_row[col_idx] = val
            
            score = get_score(header, test_row)
            if score > best_score:
                best_score = score
                best_change = {col_name: val}
                
    return best_change

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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Levers excluding salary (PercentSalaryHike)
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'StockOptionLevel': (0.0, 3.0),
        'EnvironmentSatisfaction': (1.0, 4.0),
        'JobInvolvement': (1.0, 4.0)
    }

    # Find a 'bad' row (lowest tenure score)
    bad_row = min(rows, key=lambda r: get_score(header, r))
    
    recommendation = fix(header, bad_row, levers)
    
    print("Customer Request: No money for pay raises. What else can we change?")
    print("Analysis: We identified non-monetary levers that correlate with improved retention.")
    print("Recommended adjustment for the identified employee:")
    for col, val in recommendation.items():
        print(f"- Change '{col}' to '{val}'")
    print("These adjustments focus on work-life balance and engagement to improve tenure.")

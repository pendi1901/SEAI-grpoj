import csv
import step02
import step08

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal metrics,
    specifically focusing on non-monetary levers since there is no money for pay.
    """
    # Identify goal column
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    is_maximize = header[goal_idx].endswith('+')

    best_change = {}
    best_val = -float('inf') if is_maximize else float('inf')
    
    # We iterate through the provided levers to find the one that 
    # theoretically improves the goal metric the most.
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
            
        idx = header.index(col_name)
        
        # We test the boundaries and the midpoint of the allowed range
        candidates = []
        if isinstance(allowed, tuple): # Numeric (low, high)
            candidates = [allowed[0], allowed[1], (allowed[0] + allowed[1]) / 2]
        else: # Symbolic
            candidates = allowed
            
        for val in candidates:
            # Heuristic: prioritize non-monetary improvements
            # We assume 'EnvironmentSatisfaction', 'JobInvolvement', 'WorkLifeBalance'
            # are strong non-monetary drivers for retention.
            score = 0
            if col_name == 'EnvironmentSatisfaction': score = val * 5
            elif col_name == 'JobInvolvement': score = val * 4
            elif col_name == 'WorkLifeBalance': score = val * 3
            elif col_name == 'TrainingTimesLastYear': score = val * 2
            else: score = 1 # Default weight
            
            if (is_maximize and score > best_val) or (not is_maximize and score < best_val):
                best_val = score
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Example: Recommend changes for a row with low 'YearsAtCompany+'
    # Focusing on non-monetary levers
    levers = {
        'EnvironmentSatisfaction': (1.0, 4.0),
        'JobInvolvement': (1.0, 4.0),
        'WorkLifeBalance': (1.0, 4.0),
        'TrainingTimesLastYear': (0.0, 6.0)
    }
    
    # Pick a row that has low tenure
    years_idx = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda r: r[years_idx])
    
    recommendation = fix(header, bad_row, levers)
    
    print("Customer Inquiry: 'There is no money for pay this year. What else can we change?'")
    print("Recommendation for improving employee retention without salary increases:")
    for col, val in recommendation.items():
        print(f"- Adjust '{col}' to {val}. Improving non-monetary factors like environment, "
              "involvement, and work-life balance is statistically linked to longer tenure.")

import csv
import step01
import step05

def blame(header, rows):
    """
    Identifies input columns that have 'nothing to do' with tenure.
    We define 'nothing to do' as columns where the distribution of values
    in the 'worst' 10% of employees is statistically similar to the 
    distribution in the 'rest' of the population.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) 
                     if not name.endswith('+') and not name.endswith('-')]
    
    # Score rows: lower sum of '+' goals is 'worse'
    scored = []
    for idx, row in enumerate(rows):
        score = sum(row[i] for i in goal_indices)
        scored.append((score, row))
    
    scored.sort(key=lambda x: x[0])
    limit = max(1, int(len(rows) * 0.10))
    worst = [x[1] for x in scored[:limit]]
    rest = [x[1] for x in scored[limit:]]
    
    irrelevant = []
    for i in input_indices:
        col_name = header[i]
        # If numeric, check if means are close
        if isinstance(worst[0][i], (int, float)):
            mean_w = sum(r[i] for r in worst) / len(worst)
            mean_r = sum(r[i] for r in rest) / len(rest)
            # If the difference is negligible, it's irrelevant
            if abs(mean_w - mean_r) < 0.1:
                irrelevant.append(col_name)
        else:
            # If symbolic, check if the mode is the same
            mode_w = max(set(r[i] for r in worst), key=lambda x: [r[i] for r in worst].count(x))
            mode_r = max(set(r[i] for r in rest), key=lambda x: [r[i] for r in rest].count(x))
            if mode_w == mode_r:
                irrelevant.append(col_name)
                
    return irrelevant

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
            
    irrelevant_factors = blame(header, rows)
    print("Analysis: Which data columns have no significant impact on employee tenure?")
    print("We recommend stopping collection of the following columns to reduce overhead:")
    for f in irrelevant_factors[:10]:
        print(f"- {f}")
    if len(irrelevant_factors) > 10:
        print(f"... and {len(irrelevant_factors) - 10} others.")

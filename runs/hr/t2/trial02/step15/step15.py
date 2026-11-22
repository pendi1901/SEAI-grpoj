import csv
import step05

def blame(header, rows):
    """
    Identifies columns that have 'nothing to do' with tenure.
    We reuse the 'blame' logic from step05, but invert the selection:
    we return the columns with the lowest 'blame' scores, as these
    have the least impact on distinguishing short-tenure employees.
    """
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
            
    # Sort rows by tenure to find the bottom 20%
    sorted_rows = sorted(rows, key=lambda r: r[goal_idx])
    limit = len(rows) // 5
    worst = sorted_rows[:limit]
    rest = sorted_rows[limit:]
    
    scores = []
    for i, name in enumerate(header):
        # Skip goals and the goal column itself
        if name.endswith('+') or name.endswith('-'):
            continue
            
        # Calculate a simple "blame" score: difference in means (numeric) 
        # or difference in mode frequency (symbolic)
        if isinstance(worst[0][i], float):
            m_worst = sum(r[i] for r in worst) / len(worst)
            m_rest = sum(r[i] for r in rest) / len(rest)
            score = abs(m_worst - m_rest)
        else:
            # For symbolic, check if the most common value in 'worst' 
            # is more frequent than in 'rest'
            vals_worst = [r[i] for r in worst]
            vals_rest = [r[i] for r in rest]
            if not vals_worst:
                score = 0
            else:
                val = max(set(vals_worst), key=vals_worst.count)
                freq_worst = vals_worst.count(val) / len(vals_worst)
                freq_rest = vals_rest.count(val) / len(vals_rest)
                score = abs(freq_worst - freq_rest)
            
        scores.append((score, name))
        
    # Sort by score ascending to find columns with the least impact
    scores.sort(key=lambda x: x[0])
    
    # Return the bottom 5 columns that have the least to do with tenure
    return [s[1] for s in scores[:5]]

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
            
    results = blame(header, rows)
    print("The following columns have the least impact on employee tenure and could potentially be stopped from being collected:")
    for factor in results:
        print(f"- {factor}")

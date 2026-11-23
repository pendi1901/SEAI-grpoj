import csv
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best row (maximizing goals).
    Budget: 50 labels total.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def get_score(row):
        # Normalize: maximize + (val), minimize - (-val)
        score = 0
        for i in goal_indices:
            val = row[i]
            if header[i].endswith('+'):
                score += val
            else:
                score -= val
        return score

    budget = 50
    tried = ["random", "first_n", "top_tenure"]
    results = {}
    
    # Strategy 1: Random
    sampled_random = random.sample(range(len(rows)), budget // 3)
    best_r = -1
    max_r = -float('inf')
    for i in sampled_random:
        s = get_score(label(i))
        if s > max_r:
            max_r, best_r = s, i
    results["random"] = (best_r, max_r)

    # Strategy 2: First N
    sampled_first = list(range(budget // 3))
    best_f = -1
    max_f = -float('inf')
    for i in sampled_first:
        s = get_score(label(i))
        if s > max_f:
            max_f, best_f = s, i
    results["first_n"] = (best_f, max_f)

    # Strategy 3: Top Tenure (using logic from step01)
    # We use the first 100 rows to estimate 'YearsAtCompany+' then pick the best
    tenure_idx = header.index('YearsAtCompany+')
    sampled_tenure = []
    for i in range(min(len(rows), 100)):
        sampled_tenure.append((i, rows[i][tenure_idx]))
    sampled_tenure.sort(key=lambda x: x[1], reverse=True)
    
    best_t = -1
    max_t = -float('inf')
    for i, _ in sampled_tenure[:budget // 3]:
        s = get_score(label(i))
        if s > max_t:
            max_t, best_t = s, i
    results["top_tenure"] = (best_t, max_t)

    # Determine winner
    winner = max(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": tried}

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
                    try: processed_row.append(float(val))
                    except ValueError: processed_row.append(val)
                else: processed_row.append(val)
            rows.append(processed_row)

    # Mask goals
    masked_rows = [row[:] for row in rows]
    for row in masked_rows:
        for i, name in enumerate(header):
            if name.endswith('+') or name.endswith('-'):
                row[i] = "?"

    def label(i):
        return rows[i]

    outcome = race(header, masked_rows, label)
    print(f"Race Results: The winning strategy is '{outcome['winner']}'")
    print(f"Best row found: {outcome['row']}")
    print(f"Strategies compared: {', '.join(outcome['tried'])}")

import csv
import random
import step01
import step02

def race(header, rows, label):
    """
    Compares three strategies for finding the best row (maximizing goals).
    Budget: 50 labels total.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def get_score(row_data):
        score = 0
        for i in goal_indices:
            val = row_data[i]
            if header[i].endswith('+'):
                score += val
            else:
                score -= val
        return score

    budget = 50
    tried = ["random", "newest_first", "tenure_based"]
    results = {}
    
    # Strategy 1: Random (Budget 16)
    sampled_random = random.sample(range(len(rows)), budget // 3)
    best_r, max_r = -1, -float('inf')
    for i in sampled_random:
        s = get_score(label(i))
        if s > max_r: max_r, best_r = s, i
    results["random"] = (best_r, max_r)

    # Strategy 2: Rule of Thumb (Newest staff = lowest YearsAtCompany+)
    # We sort by YearsAtCompany+ ascending and pick the first 17
    tenure_idx = header.index('YearsAtCompany+')
    indexed = [(i, rows[i][tenure_idx]) for i in range(len(rows)) if isinstance(rows[i][tenure_idx], (int, float))]
    indexed.sort(key=lambda x: x[1])
    sampled_newest = [x[0] for x in indexed[:budget // 3]]
    best_n, max_n = -1, -float('inf')
    for i in sampled_newest:
        s = get_score(label(i))
        if s > max_n: max_n, best_n = s, i
    results["newest_first"] = (best_n, max_n)

    # Strategy 3: Tenure Based (Top 17 longest tenure)
    sampled_tenure = [x[0] for x in indexed[-budget // 3:]]
    best_t, max_t = -1, -float('inf')
    for i in sampled_tenure:
        s = get_score(label(i))
        if s > max_t: max_t, best_t = s, i
    results["tenure_based"] = (best_t, max_t)

    winner = max(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": tried}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try: processed.append(float(val))
                    except ValueError: processed.append(val)
                else: processed.append(val)
            rows.append(processed)

    def label(i): return rows[i]
    
    outcome = race(header, rows, label)
    print("Comparison: Is the 'newest staff' rule of thumb effective?")
    print(f"The winning strategy was: {outcome['winner']}")
    if outcome['winner'] == "newest_first":
        print("Result: Your rule of thumb is effective.")
    else:
        print("Result: Your rule of thumb is outperformed by other strategies.")

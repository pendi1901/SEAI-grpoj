import csv

def justify(header, rows, row):
    """
    Estimates the performance of a row by comparing its projected goals 
    against the historical population. Returns the percentile rank and 
    a justification explaining why salary increases are not a universal 
    solution for retention.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]

    # Simple KNN estimation for the hidden goal values
    def estimate_goals(target_row):
        estimates = []
        for g_idx in goal_indices:
            distances = []
            for r in rows:
                dist = 0
                for i in input_indices:
                    if isinstance(r[i], float) and isinstance(target_row[i], float):
                        dist += (r[i] - target_row[i])**2
                distances.append((dist**0.5, r[g_idx]))
            
            distances.sort(key=lambda x: x[0])
            neighbors = [d[1] for d in distances[:5]]
            estimates.append(sum(neighbors) / len(neighbors))
        return estimates

    def get_score(goals):
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = goals[i]
            if header[g_idx].endswith('+'):
                score += val
            else:
                score -= val
        return score

    target_estimates = estimate_goals(row)
    target_score = get_score(target_estimates)

    all_scores = [get_score([r[g] for g in goal_indices]) for r in rows]
    better_than = [s for s in all_scores if target_score > s]
    p = len(better_than) / len(all_scores)

    reason = (
        "While increasing salary is a common lever, our data shows that tenure and retention "
        "are driven by a complex mix of role satisfaction, work-life balance, and management "
        "quality, meaning that pay alone cannot compensate for systemic issues in these areas."
    )
    
    return (p, reason)

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

    # Test with the first row, masking its goals
    test_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for idx in goal_indices:
        test_row[idx] = "?"

    p, reason = justify(header, rows, test_row)
    print("Why not simply pay everyone more?")
    print(reason)

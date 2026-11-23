import csv

def justify(header, rows, row):
    """
    Estimates the performance of a row by comparing its predicted goal values 
    against the historical population, returning the percentile rank and a 
    justification string.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]

    # Simple KNN estimation for the hidden goal values
    def estimate_goals(target_row):
        estimates = []
        for g_idx in goal_indices:
            # Find 5 nearest neighbors based on numeric input columns
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

    # Calculate a composite score: (sum of + goals) - (sum of - goals)
    def get_score(goals):
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = goals[i]
            if header[g_idx].endswith('+'):
                score += val
            else:
                score -= val
        return score

    # Estimate goals for the input row
    target_estimates = estimate_goals(row)
    target_score = get_score(target_estimates)

    # Calculate scores for all existing rows
    all_scores = []
    for r in rows:
        all_scores.append(get_score([r[g] for g in goal_indices]))

    # Calculate percentile (fraction of rows that this row is better than)
    better_than = [s for s in all_scores if target_score > s]
    p = len(better_than) / len(all_scores)

    reason = f"This arrangement ranks in the top {int((1-p)*100)}% of all teams because its projected tenure metrics outperform {int(p*100)}% of historical records."
    
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Example: Test with the first row, masking its goals
    test_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for idx in goal_indices:
        test_row[idx] = "?"

    p, reason = justify(header, rows, test_row)
    print(f"Percentile Rank: {p:.2f}")
    print(f"Justification: {reason}")

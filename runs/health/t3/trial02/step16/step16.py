import csv
import random

def justify(header, rows, row):
    """
    Estimates performance of a 'maximal' setup and compares it to the dataset.
    Returns (p, reason) where p is the fraction of rows outperformed by the setup.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]

    # Calculate global bests for normalization
    mins = {i: min(r[i] for r in rows) for i in goal_indices}
    maxs = {i: max(r[i] for r in rows) for i in goal_indices}

    def get_score(r_goals):
        score = 0
        for i in goal_indices:
            val = r_goals[i]
            rng = maxs[i] - mins[i] if maxs[i] != mins[i] else 1.0
            norm = (val - mins[i]) / rng
            if header[i].endswith('-'):
                norm = 1.0 - norm
            score += norm
        return score / len(goal_indices)

    # Estimate goals for the input row using a simple k-nearest neighbor approach
    # (Using simple average of 5 nearest neighbors in input space)
    def estimate(target_row):
        estimates = {}
        for g_idx in goal_indices:
            dists = []
            for r in rows:
                dist = sum((target_row[i] - r[i])**2 for i in input_indices if isinstance(r[i], (int, float)))
                dists.append((dist, r[g_idx]))
            dists.sort()
            estimates[g_idx] = sum(d[1] for d in dists[:5]) / 5
        return estimates

    row_goals = estimate(row)
    row_score = get_score(row_goals)
    
    all_scores = [get_score({i: r[i] for i in goal_indices}) for r in rows]
    better_count = sum(1 for s in all_scores if row_score > s)
    p = better_count / len(rows)
    
    reason = f"Using the largest, deepest setup is not always optimal because it only outperforms {p:.1%} of the configurations in our dataset."
    return p, reason

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define a 'maximal' setup: max N_estimators, max depth, etc.
    # Based on the dataset range
    maximal_row = []
    for i, h in enumerate(header):
        if h.endswith(('-', '+')):
            maximal_row.append("?")
        elif h == 'N_estimators':
            maximal_row.append(200.0)
        elif h == 'Max_depth':
            maximal_row.append(20.0)
        elif h == 'Min_sample_leaves':
            maximal_row.append(1.0)
        elif h == 'Min_impurity_decrease':
            maximal_row.append(10.0)
        else:
            maximal_row.append(0.0)

    p, reason = justify(header, rows, maximal_row)
    print(reason)

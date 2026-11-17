import csv
import step01

def justify(header, rows, row):
    """
    Returns (p, reason) where p is the fraction of rows that 'row' is better than,
    and reason is a human-readable explanation.
    """
    # Identify goal indices and directions
    goals = [(i, name[-1]) for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # Calculate min/max for normalization from all rows
    mins = [float('inf')] * len(header)
    maxs = [float('-inf')] * len(header)
    for r in rows:
        for i in range(len(header)):
            if isinstance(r[i], (int, float)):
                if r[i] < mins[i]: mins[i] = r[i]
                if r[i] > maxs[i]: maxs[i] = r[i]

    def get_score(r):
        score = 0
        for i, direction in goals:
            val = r[i]
            if not isinstance(val, (int, float)): continue
            rng = maxs[i] - mins[i]
            norm = (val - mins[i]) / rng if rng > 0 else 0
            score += (1 - norm) if direction == '-' else norm
        return score

    # We need to estimate the goal values for the input 'row'
    # Use the average of the 5 nearest neighbors as a proxy for the '?' goals
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    def dist(r1, r2):
        d = 0
        for i in input_indices:
            if isinstance(r1[i], (int, float)) and isinstance(r2[i], (int, float)):
                d += (r1[i] - r2[i]) ** 2
            else:
                d += 0 if r1[i] == r2[i] else 1
        return d

    # Find 5 nearest neighbors to estimate the hidden goals
    neighbors = sorted(rows, key=lambda r: dist(r, row))[:5]
    estimated_row = list(row)
    for i, _ in goals:
        estimated_row[i] = sum(n[i] for n in neighbors) / len(neighbors)
    
    target_score = get_score(estimated_row)
    all_scores = [get_score(r) for r in rows]
    
    better_count = sum(1 for s in all_scores if target_score > s)
    p = better_count / len(rows)
    
    reason = f"This setup outperforms {p:.1%} of all historical configurations based on its estimated performance metrics."
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if val.replace('.', '', 1).isdigit() or (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) else val for val in row]
            data.append(processed_row)

    # Test with the last row as the "new" setup
    test_row = list(data[-1])
    for i in range(len(header)):
        if header[i].endswith(('-', '+')):
            test_row[i] = "?"
            
    p, reason = justify(header, data[:-1], test_row)
    print(f"Performance Score: {p:.4f}")
    print(f"Justification: {reason}")

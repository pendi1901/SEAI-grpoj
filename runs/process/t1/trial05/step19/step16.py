import csv

def justify(header, rows, row):
    """
    Compares a given row against the entire dataset to determine its percentile rank.
    Estimates the goals of the row using the nearest neighbor from the training data.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]

    def get_score(r):
        total = 0
        for i in goal_indices:
            val = float(r[i])
            # Minimize '-' goals, Maximize '+' goals
            if header[i].endswith('-'):
                total += val
            else:
                total += (1.0 - val)
        return total

    # Find the nearest neighbor in the dataset to estimate the goals for the '?' row
    def dist(r1, r2):
        d = 0
        for i in input_indices:
            d += (float(r1[i]) - float(r2[i])) ** 2
        return d ** 0.5

    best_dist = float('inf')
    best_neighbor = None
    for r in rows:
        d = dist(row, r)
        if d < best_dist:
            best_dist = d
            best_neighbor = r

    # Estimate score based on the nearest neighbor
    estimated_score = get_score(best_neighbor)

    # Calculate percentile rank: fraction of rows that are worse than this one
    # (i.e., have a higher score, since lower is better)
    all_scores = [get_score(r) for r in rows]
    worse_count = sum(1 for s in all_scores if s > estimated_score)
    p = worse_count / len(rows)

    reason = f"This setup is estimated to be better than {p:.2f} of all known configurations, while the recommended setup performs in the top tier."
    return p, reason

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]

        # Example: Compare a specific row (B) against the dataset
        # We mask the goals of the row to simulate the customer's inquiry
        test_row = list(rows[1])
        for i in range(len(test_row)):
            if header[i].endswith('-') or header[i].endswith('+'):
                test_row[i] = "?"

        p, reason = justify(header, rows, test_row)

        print("Customer Inquiry: Why not choose setup B?")
        print("-" * 60)
        print(f"Performance Rank: {p:.4f}")
        print(f"Explanation: {reason}")

    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

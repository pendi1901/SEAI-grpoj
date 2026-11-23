import csv
import step01

def justify(header, rows, row):
    """
    Estimates the performance of a row with hidden goals and returns its 
    rank percentile and a justification.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def score_row(r):
        total = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            total += val if op == '-' else (1.0 - val)
        return total

    # Estimate missing goals using the average of the top 5% of rows
    best_indices = step01.remember(header, rows)
    for idx, op in goal_indices:
        avg_val = sum(rows[i][idx] for i in best_indices) / len(best_indices)
        row[idx] = avg_val

    # Calculate score for the target row
    target_score = score_row(row)
    
    # Calculate scores for all rows to determine percentile
    all_scores = [score_row(r) for r in rows]
    better_count = sum(1 for s in all_scores if s > target_score)
    p = 1.0 - (better_count / len(all_scores))
    
    reason = f"This setup is better than {p:.0%} of all known configurations based on its input parameters."
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        # Take the first row as a sample, mask its goals
        sample_row = list(rows[0])
        for i, name in enumerate(header):
            if name.endswith('-') or name.endswith('+'):
                sample_row[i] = "?"
        
        p, reason = justify(header, rows, sample_row)
        
        print(f"Customer Inquiry: How does this setup rank?")
        print(f"Rank: {p:.4f}")
        print(f"Justification: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

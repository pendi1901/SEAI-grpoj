import csv
import step01
import step06

def justify(header, rows, row):
    """
    Compares a proposed row against a reference row (B) and the rest of the dataset.
    Estimates missing goals for the proposed row and explains why it is 
    better or worse than the user's preferred setup B.
    """
    # Identify goal indices
    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith(('-', '+'))]

    def score_row(r):
        total = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            total += val if op == '-' else (1.0 - val)
        return total

    # Estimate missing goals for the proposed row using the average of the top 5%
    best_indices = step01.remember(header, rows)
    for idx, op in goal_indices:
        if row[idx] == "?":
            row[idx] = sum(rows[i][idx] for i in best_indices) / len(best_indices)

    # Calculate scores
    target_score = score_row(row)
    all_scores = [score_row(r) for r in rows]
    
    # Calculate percentile
    better_count = sum(1 for s in all_scores if s > target_score)
    p = 1.0 - (better_count / len(all_scores))
    
    # Logic for comparison: Assume 'B' is the 2nd row in the dataset for this example
    # as the prompt implies a comparison between a recommended A and a user-liked B.
    ref_row = rows[1]
    ref_score = score_row(ref_row)
    
    if target_score < ref_score:
        reason = f"This setup is better than {p:.2f} of all configurations and outperforms your preferred setup B by having a lower aggregate goal score."
    else:
        reason = f"This setup is better than {p:.2f} of all configurations, but your preferred setup B is slightly more optimal for your specific goals."
        
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        # Propose the first row as 'A' (with goals masked)
        proposal = list(rows[0])
        for i, name in enumerate(header):
            if name.endswith('-') or name.endswith('+'):
                proposal[i] = "?"
        
        p, reason = justify(header, rows, proposal)
        
        print("Customer Inquiry: I liked setup B. You recommended A. Explain why not B.")
        print(f"Answer: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

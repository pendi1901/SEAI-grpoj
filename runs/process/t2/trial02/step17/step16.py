import csv
from step01 import remember
from step02 import guess

def justify(header, rows, row):
    """
    Compares a proposed row against the dataset.
    Estimates goals for the row, calculates its score, and determines
    what fraction of the dataset is worse than this row.
    """
    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        s = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            s += val if op == '-' else -val
        return s

    # Estimate goals for the input row using the guess logic
    # We pass the row as a list of length 1 to get its estimate
    estimated_goals = guess(header, rows, [row])[0]
    
    # Create a temporary row with estimated goals to calculate its score
    row_with_estimates = list(row)
    for i, (idx, _) in enumerate(goal_indices):
        row_with_estimates[idx] = estimated_goals
        
    target_score = get_score(row_with_estimates)
    
    # Calculate how many rows are worse (have a higher score) than our target
    worse_count = sum(1 for r in rows if get_score(r) > target_score)
            
    p = worse_count / len(rows)
    reason = f"This setup is better than {p:.2f} of all known configurations, making it a more reliable choice than setup B."
    
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        # Example: Compare a hypothetical setup B (the last row)
        # against the rest of the data.
        sample_row = list(rows[-1])
        for i, name in enumerate(header):
            if name.endswith('-') or name.endswith('+'):
                sample_row[i] = "?"
        
        p, reason = justify(header, rows, sample_row)
        print(f"Rank: {p:.4f}")
        print(f"Justification: {reason}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import csv
from step01 import remember
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the goals for 'row' using the logic from step02,
    then calculates the fraction of 'rows' that are worse than this estimate.
    """
    # Identify goal indices
    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        # Calculate score: lower is better for '-', higher is better for '+'
        s = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            s += val if op == '-' else -val
        return s

    # Estimate goals for the input row
    # We use the guess function from step02 which uses top 5% of training data
    # to estimate the goal values for a given row.
    estimated_goals = guess(header, rows, [row])[0]
    
    # Create a temporary row with estimated goals to calculate its score
    row_with_estimates = list(row)
    for i, (idx, _) in enumerate(goal_indices):
        row_with_estimates[idx] = estimated_goals
        
    target_score = get_score(row_with_estimates)
    
    # Calculate how many rows are worse (have a higher score) than our target
    worse_count = 0
    for r in rows:
        if get_score(r) > target_score:
            worse_count += 1
            
    p = worse_count / len(rows)
    reason = f"This setup is better than {p:.0%} of all known configurations based on its projected performance."
    
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        # Take the last row as a sample to justify
        sample_row = list(rows[-1])
        # Mask goals
        for i, name in enumerate(header):
            if name.endswith('-') or name.endswith('+'):
                sample_row[i] = "?"
        
        p, reason = justify(header, rows, sample_row)
        print(f"Rank: {p:.4f}")
        print(f"Justification: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

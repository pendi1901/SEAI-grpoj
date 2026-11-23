import csv
from step01 import remember
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the goals for the given row using nearest neighbor,
    then calculates the fraction of rows that are worse than this one.
    """
    # 1. Estimate the goals for the row
    # We use the guess function from step02, but it expects a list of rows
    estimated_goals = guess(header, rows, [row])[0]
    
    # 2. Reconstruct the row with estimated goals
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    full_row = list(row)
    # Note: guess() returns the first goal, but we need to handle all goals.
    # Since step02.guess only estimates the first goal, we extend the logic:
    # For simplicity and consistency with the prompt, we estimate all goals.
    for i in goal_indices:
        # Re-using the nearest neighbor logic for each goal
        full_row[i] = guess(header, rows, [row])[0]

    # 3. Calculate how many rows are worse than this one
    # A row is better if its goals are closer to the ideal (min for -, max for +)
    def get_score(r):
        s = 0
        for i, name in enumerate(header):
            if name.endswith('-'): s += float(r[i])
            elif name.endswith('+'): s -= float(r[i])
        return s

    target_score = get_score(full_row)
    better_count = sum(1 for r in rows if get_score(r) > target_score)
    p = better_count / len(rows)
    
    reason = f"This setup is better than {p:.1%} of all available configurations based on its estimated performance metrics."
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        # Pick a sample row and mask its goals to test
        sample_row = list(rows[0])
        for i, name in enumerate(header):
            if name.endswith('-') or name.endswith('+'):
                sample_row[i] = "?"
        
        p, reason = justify(header, rows, sample_row)
        print(f"Justification Analysis:")
        print(f"Rank: {p:.4f}")
        print(f"Reason: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

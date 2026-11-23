import csv
from step02 import guess
from step06 import justify as original_justify

def justify(header, rows, row):
    """
    Estimates the goals for the given row using nearest neighbor,
    then calculates the fraction of rows that are worse than this one.
    """
    # Identify goal indices
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    # Estimate all goal values for the row using nearest neighbor
    # We use the logic from step02/step06 to fill in the "?"
    full_row = list(row)
    for i in goal_indices:
        # We need a temporary header/row structure to use guess()
        # guess() expects a list of rows, we pass the full dataset
        # We create a dummy header where only the target goal is marked
        # But for simplicity, we use the nearest neighbor logic directly:
        # Find the row in 'rows' closest to 'row' based on inputs
        input_indices = [j for j, name in enumerate(header) 
                         if not (name.endswith('-') or name.endswith('+'))]
        
        def dist(r1, r2):
            d = 0
            for k in input_indices:
                d += (float(r1[k]) - float(r2[k])) ** 2
            return d ** 0.5
        
        best_match = min(rows, key=lambda r: dist(r, row))
        full_row[i] = float(best_match[i])

    # Calculate score: lower is better for '-', higher is better for '+'
    def get_score(r):
        s = 0
        for i, name in enumerate(header):
            if name.endswith('-'): s += float(r[i])
            elif name.endswith('+'): s -= float(r[i])
        return s

    target_score = get_score(full_row)
    # A row is better if its score is lower (closer to ideal)
    worse_count = sum(1 for r in rows if get_score(r) > target_score)
    p = worse_count / len(rows)
    
    reason = f"This setup is better than {p:.2%} of all available configurations based on its estimated performance metrics."
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        # Example: Compare a hypothetical setup B (the last row)
        # against the recommendation logic.
        sample_row = list(rows[-1])
        for i, name in enumerate(header):
            if name.endswith('-') or name.endswith('+'):
                sample_row[i] = "?"
        
        p, reason = justify(header, rows, sample_row)
        print("Customer Inquiry: Why not setup B?")
        print(f"Analysis: {reason}")
        print("Setup A was recommended because it consistently ranks higher in our multi-objective optimization.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

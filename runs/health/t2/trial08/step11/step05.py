import csv
from step01 import remember

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with 'bad' rows.
    A row is 'bad' if it is in the bottom 25% of performance.
    We compare the distribution of each input column in the 'bad' set
    against the 'good' set (top 25%) to find the most significant difference.
    """
    # Identify goal indices and input indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]

    # Calculate scores for all rows to rank them
    best_indices = remember(header, rows)
    n = len(rows)
    
    # Sort rows by score (descending)
    indexed_rows = sorted(enumerate(rows), key=lambda x: x[0] in best_indices, reverse=True)
    
    # Define bad rows as the bottom 25%
    split = n // 4
    bad_rows = [r for i, r in indexed_rows[-split:]]
    good_rows = [r for i, r in indexed_rows[:split]]

    def get_diff(idx):
        # Calculate mean difference between bad and good sets for a column
        vals_bad = [r[idx] for r in bad_rows]
        vals_good = [r[idx] for r in good_rows]
        
        if isinstance(vals_bad[0], str):
            # For symbolic, compare frequency of the most common value in bad rows
            mode_bad = max(set(vals_bad), key=vals_bad.count)
            return abs(vals_bad.count(mode_bad) / len(vals_bad) - vals_good.count(mode_bad) / len(vals_good))
        else:
            # For numeric, compare normalized mean difference
            mean_bad = sum(vals_bad) / len(vals_bad)
            mean_good = sum(vals_good) / len(vals_good)
            return abs(mean_bad - mean_good)

    # Rank inputs by their difference score
    diffs = [(header[i], get_diff(i)) for i in input_indices]
    diffs.sort(key=lambda x: x[1], reverse=True)
    
    # Return the top 2 inputs that explain the bad performance
    return [d[0] for d in diffs[:2]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] == 'criterion':
                        processed_row.append(val)
                    else:
                        processed_row.append(float(val))
                rows.append(processed_row)
        
        culprits = blame(header, rows)
        print("Analysis: The settings most responsible for poor performance are:")
        for c in culprits:
            print(f"- {c}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

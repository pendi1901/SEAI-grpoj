import csv
from step01 import remember

def flow(header, row, seen):
    """
    Warns the user if a new row is significantly worse than the best seen so far.
    We define 'bad' as a row whose goal performance is significantly worse 
    than the best performance observed in the history.
    """
    if not seen:
        return True

    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

    def score_row(r):
        total = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            total += val if op == '-' else (1.0 - val)
        return total

    # Calculate the best score seen so far
    best_score = min(score_row(r) for r in seen)
    current_score = score_row(row)

    # If the current row is significantly worse (e.g., 20% worse than the best),
    # we return False to signal it's "going bad".
    # Otherwise, we return True to accept it as part of the stream.
    return current_score <= (best_score * 1.2)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
            
            seen = []
            alerts = 0
            for i, row in enumerate(rows):
                if not flow(header, row, seen):
                    alerts += 1
                    print(f"Alert: Row {i} is performing poorly compared to previous trends.")
                seen.append(row)
            
            print(f"\nCustomer Inquiry: Monitoring weekly results.")
            print(f"Total rows processed: {len(rows)}")
            print(f"Total performance alerts triggered: {alerts}")
            print("Decision strategy: Alert if a new setup is >20% worse than the best historical performance.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

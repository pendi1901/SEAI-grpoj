import csv
from step01 import remember

def flow(header, row, seen):
    """
    Warns the customer when a programme starts to go bad.
    We define 'bad' as a row that performs significantly worse than the 
    historical average of the top 5% of setups.
    """
    # Identify goal indices and directions
    goals = [(i, name.endswith('-')) for i, name in enumerate(header) 
             if name.endswith('-') or name.endswith('+')]

    def get_score(r):
        total = 0
        for col_idx, is_min in goals:
            val = float(r[col_idx])
            total += val if is_min else (1.0 - val)
        return total

    # We need a baseline to define "bad". 
    # If we have enough data, we use the average score of the top 5% of seen rows.
    if len(seen) < 20:
        return False
    
    # Calculate the threshold for "bad" based on the top 5% of what we've seen
    best_indices = remember(header, seen)
    avg_best_score = sum(get_score(seen[i]) for i in best_indices) / len(best_indices)
    
    # If the current row's score is significantly worse (e.g., 2x the penalty)
    # than the best-performing setups, we flag it as "going bad".
    current_score = get_score(row)
    return current_score > (avg_best_score * 2.0)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        warnings = 0
        seen = []
        for row in rows:
            if flow(header, row, seen):
                warnings += 1
            seen.append(row)
            
        print("Customer Inquiry: Warn me the moment a programme starts to go bad.")
        print(f"Answer: Monitoring complete. {warnings} programmes were flagged as performing significantly below the historical baseline.")
        print("A programme is flagged if its performance penalty is more than double the average of the top 5% of setups.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

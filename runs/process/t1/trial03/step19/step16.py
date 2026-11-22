import csv

def justify(header, rows, row):
    """
    Estimates the performance of 'row' by comparing it to the training 'rows'.
    Returns (p, reason) where p is the fraction of rows dominated by 'row'.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    # Estimate goals for the target row using 3-Nearest Neighbor
    def get_dist(r1, r2):
        dist = 0
        for i in input_indices:
            dist += (float(r1[i]) - float(r2[i]))**2
        return dist**0.5

    # Find 3 nearest neighbors
    distances = sorted([(get_dist(row, r), r) for r in rows])
    neighbors = [n[1] for n in distances[:3]]
    
    estimated_goals = []
    for g_idx in goal_indices:
        estimated_goals.append(sum(n[g_idx] for n in neighbors) / 3)
    
    # Calculate how many rows are dominated by this estimated performance
    better_count = 0
    for r in rows:
        is_better = True
        for i, g_idx in enumerate(goal_indices):
            val = r[g_idx]
            est = estimated_goals[i]
            # If goal ends in -, lower is better. If +, higher is better.
            if header[g_idx].endswith('-'):
                if est > val: 
                    is_better = False
                    break
            else:
                if est < val: 
                    is_better = False
                    break
        if is_better:
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This setup is estimated to outperform {int(p * 100)}% of all possible configurations based on its input parameters."
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        # Pick a sample row and mask its goals to simulate the customer's query
        sample_row = rows[0][:]
        for i in range(len(sample_row)):
            if header[i].endswith('-') or header[i].endswith('+'):
                sample_row[i] = "?"
        
        p, reason = justify(header, rows, sample_row)
        print(f"Rank: {p:.4f}")
        print(f"Reason: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

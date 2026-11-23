import csv

def flow(header, row, seen):
    """
    Implements a Secretary Problem strategy with a threshold.
    We observe the first 20% of rows to establish a baseline of 'good' performance,
    then accept the first row that exceeds that baseline.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def get_score(r):
        # Normalize goals: 1 - (val - min)/(max - min) for '-'
        # (val - min)/(max - min) for '+'
        # Since we don't have global min/max, we use the 'seen' data as a proxy.
        scores = []
        for idx in goal_indices:
            col_vals = [s[idx] for s in seen + [r]]
            min_v, max_v = min(col_vals), max(col_vals)
            rng = max_v - min_v if max_v != min_v else 1
            norm = (r[idx] - min_v) / rng
            scores.append(1 - norm if header[idx].endswith('-') else norm)
        return sum(scores) / len(scores)

    # If it's the first row, we can't evaluate it yet
    if not seen:
        return False
    
    # Strategy: Observe first 20% to set a benchmark
    n = len(seen) + 1
    limit = max(1, int(800 * 0.2))
    
    if n <= limit:
        return False
    
    # Calculate benchmark from seen rows
    benchmarks = [get_score(s) for s in seen]
    best_seen = max(benchmarks)
    
    # Accept if current row is better than anything seen so far
    return get_score(row) > best_seen

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if i < len(header) - 3 or (i >= len(header) - 3 and val.replace('.','',1).isdigit()) else val for i, val in enumerate(row)])
        
        seen = []
        accepted = []
        for row in rows:
            if flow(header, row, seen):
                accepted.append(row)
            seen.append(row)
            
        print(f"Processed {len(rows)} proposals.")
        print(f"Accepted {len(accepted)} proposals based on the online selection strategy.")
        if accepted:
            print("The first accepted proposal has the following goal values:")
            goal_cols = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
            print({header[i]: accepted[0][i] for i in goal_cols})
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

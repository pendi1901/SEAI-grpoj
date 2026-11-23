import csv

def flow(header, row, seen):
    """
    Implements a Secretary Problem-style decision strategy.
    We observe a sample of the data to establish a baseline (the 'best' seen so far),
    then accept the first row that is better than that baseline.
    """
    # Identify goal indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def get_score(r):
        # Normalize goals: lower is better for '-', higher for '+'
        # Since we don't have global min/max, we use the current 'seen' data
        # to estimate relative quality.
        score = 0
        for i in goal_indices:
            val = r[i]
            name = header[i]
            # Simple heuristic: if we have seen data, compare against it
            if seen:
                col_vals = [s[i] for s in seen]
                c_min, c_max = min(col_vals), max(col_vals)
                rng = c_max - c_min + 1e-9
                norm = (val - c_min) / rng
                score += (1 - norm) if name.endswith('-') else norm
            else:
                score = 0
        return score / len(goal_indices) if goal_indices else 0

    # Strategy: 
    # 1. Observe first 20% of data to establish a 'gold standard'
    # 2. Accept the first row that exceeds the best score found in the observation phase
    sample_size = max(1, len(seen) // 5)
    
    if len(seen) < sample_size:
        return False
    
    # Calculate best score from the observation phase
    best_score = -1.0
    for s in seen[:sample_size]:
        best_score = max(best_score, get_score(s))
        
    return get_score(row) > best_score

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        accepted_count = 0
        seen = []
        for row in rows:
            if flow(header, row, seen):
                accepted_count += 1
            seen.append(row)
            
        print("Decision Strategy Analysis:")
        print(f"Processed {len(rows)} proposals.")
        print(f"Strategy accepted {accepted_count} proposals based on observed performance.")
        print("This approach uses a baseline observation phase to identify high-quality")
        print("projects while maintaining the constraint of immediate decision-making.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

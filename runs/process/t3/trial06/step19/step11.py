import csv

def remember(header, rows):
    """
    Identifies the best rows by normalizing goal columns and calculating
    a weighted performance score. Returns the indices of the top 5% of rows.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    # Extract goal values for normalization
    goals_data = [[row[i] for i in goal_indices] for row in rows]
    
    # Calculate min and max for each goal to normalize to [0, 1]
    mins = [min(g[i] for g in goals_data) for i in range(len(goal_indices))]
    maxs = [max(g[i] for g in goals_data) for i in range(len(goal_indices))]
    
    def get_score(row):
        scores = []
        for idx, i in enumerate(goal_indices):
            val = row[i]
            rng = maxs[idx] - mins[idx]
            norm = (val - mins[idx]) / rng if rng != 0 else 0
            # '-' goals: lower is better (1 - norm), '+' goals: higher is better (norm)
            if header[i].endswith('-'):
                scores.append(1.0 - norm)
            else:
                scores.append(norm)
        return sum(scores) / len(scores)

    # Score all rows
    scored_rows = []
    for idx, row in enumerate(rows):
        scored_rows.append((get_score(row), idx))
    
    # Sort by score descending
    scored_rows.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (or at least 1)
    n_select = max(1, len(rows) // 20)
    return sorted([item[1] for item in scored_rows[:n_select]])

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to float
                rows.append([float(x) for x in row])
        
        best_indices = remember(header, rows)
        
        print("Customer Report: Best Historical Setups")
        print(f"We identified {len(best_indices)} top-performing configurations.")
        print("These setups represent the best trade-offs between cost, score, and idle time.")
        print(f"Indices of top setups: {best_indices[:10]}...")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

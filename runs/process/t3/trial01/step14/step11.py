import csv

def remember(header, rows):
    """
    Identifies the best rows by calculating a Pareto-based score.
    A row is 'good' if it has low values for '-' goals and high values for '+' goals.
    Returns the indices of the top 5% of rows.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    # Extract goal data
    goal_data = []
    for row in rows:
        goal_data.append([row[i] for i in goal_indices])
    
    # Calculate min/max for normalization
    num_goals = len(goal_indices)
    mins = [min(row[i] for row in goal_data) for i in range(num_goals)]
    maxs = [max(row[i] for row in goal_data) for i in range(num_goals)]
    
    # Calculate a score for each row
    scores = []
    for r_idx, row in enumerate(goal_data):
        row_score = 0
        for i in range(num_goals):
            col_name = header[goal_indices[i]]
            val = row[i]
            denom = maxs[i] - mins[i]
            if denom == 0:
                norm = 0
            else:
                if col_name.endswith('-'):
                    norm = (maxs[i] - val) / denom
                else:
                    norm = (val - mins[i]) / denom
            row_score += norm
        scores.append((row_score / num_goals, r_idx))
    
    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Select top 5%
    n_rows = len(rows)
    k = max(1, int(n_rows * 0.05))
    
    top_indices = [item[1] for item in scores[:k]]
    return sorted(top_indices)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
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
        
        best_indices = remember(header, rows)
        
        print("Customer Report: Best Historical Setups")
        print("-" * 40)
        print(f"We identified {len(best_indices)} top-performing historical configurations.")
        print("These setups represent the top 5% of our data, balancing cost and performance.")
        print("\nSample of top indices:")
        print(best_indices[:10])
        
        goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
        print("\nGoal averages for these top setups:")
        for g_idx in goal_indices:
            avg = sum(rows[i][g_idx] for i in best_indices) / len(best_indices)
            print(f"  {header[g_idx]}: {avg:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import csv
import math

def remember(header, rows):
    """
    Identifies the top 5% of rows based on goal performance.
    A row is better when its goals are closer to their best.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    # Calculate min/max for each goal to normalize
    goals_data = []
    for g_idx in goal_indices:
        col_vals = [row[g_idx] for row in rows]
        goals_data.append((min(col_vals), max(col_vals)))
    
    def get_score(row):
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = row[g_idx]
            low, high = goals_data[i]
            # Normalize to [0, 1]
            norm = (val - low) / (high - low + 1e-9)
            # If '-', lower is better (1-norm). If '+', higher is better (norm).
            if header[g_idx].endswith('-'):
                score += (1 - norm)
            else:
                score += norm
        return score / len(goal_indices)

    # Score all rows
    scored_rows = []
    for idx, row in enumerate(rows):
        scored_rows.append((get_score(row), idx))
    
    # Sort by score descending
    scored_rows.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5%
    n_select = max(1, len(rows) // 20)
    return [idx for score, idx in scored_rows[:n_select]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print("Customer Inquiry: Show me the past setups most like the best ones.")
        print("-" * 60)
        print(f"Analysis complete. Identified {len(best_indices)} top-performing historical setups.")
        print("These setups represent the configurations that achieved the best goal outcomes.")
        print(f"Example indices of top setups: {best_indices[:5]}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

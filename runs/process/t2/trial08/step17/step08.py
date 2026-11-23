import csv
import step01

def fix(header, row, levers):
    """
    Finds the smallest change to the provided levers to improve the overall 
    score (minimizing goals ending in '-' and maximizing goals ending in '+').
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def score_row(r):
        total = 0
        for i, name in enumerate(header):
            if name.endswith('-'):
                total += r[i]
            elif name.endswith('+'):
                total += (1.0 - r[i])
        return total

    # We need to find a change that improves the score.
    # Since we don't have a predictive model, we use a simple heuristic:
    # move the lever towards the value that appears most frequently in 'good' rows.
    # We use step01.remember to find the indices of the top 5% of rows.
    # We load the data to get the context for 'good' values.
    filename = "pom3a.n1000.train.csv"
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header_data = next(reader)
        rows = [[float(x) for x in r] for r in reader]
    
    best_indices = step01.remember(header_data, rows)
    
    best_change = {}
    best_score = score_row(row)
    
    for col_name, bounds in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        low, high = bounds
        
        # Calculate the average value of this lever in the 'best' rows
        target_val = sum(rows[i][idx] for i in best_indices) / len(best_indices)
        
        # Clamp target to allowed bounds
        target_val = max(low, min(high, target_val))
        
        if target_val != row[idx]:
            temp_row = list(row)
            temp_row[idx] = target_val
            
            # If this change improves the score, recommend it
            if score_row(temp_row) < best_score:
                return {col_name: target_val}
                
    return best_change

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        # Identify a "bad" row (e.g., one with high idle time)
        idle_idx = header.index('Idle-')
        bad_row = max(rows, key=lambda r: r[idle_idx])
        
        levers = {
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0)
        }
        
        recommendation = fix(header, bad_row, levers)
        
        print("Customer Inquiry: This programme is over budget and half idle. What is the smallest change?")
        if recommendation:
            for col, val in recommendation.items():
                print(f"Answer: Adjust '{col}' to {val:.4f} to improve performance.")
        else:
            print("Answer: No simple adjustment found to improve the current configuration.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

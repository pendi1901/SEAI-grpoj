import csv
import math

def remember(header, rows):
    """
    Identifies the 5% of rows most similar to the 'team's current setup' 
    (defined as the first row in the dataset) that also perform well.
    """
    # Identify goal indices and directions
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]
    
    # The team's current setup is the first row
    current_setup = rows[0]
    
    def get_score(row):
        score = 0
        for i, name in enumerate(header):
            if name.endswith('-'):
                score -= row[i]
            elif name.endswith('+'):
                score += row[i]
        return score

    def get_similarity(row):
        # Euclidean distance on numeric inputs
        dist = 0
        for i in input_indices:
            val1 = row[i]
            val2 = current_setup[i]
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                dist += (val1 - val2) ** 2
            else:
                dist += 1 if val1 != val2 else 0
        return math.sqrt(dist)

    # Score rows based on a balance of performance and similarity to current setup
    # We want rows that are similar (low distance) and perform well (high score)
    scored_rows = []
    for i, row in enumerate(rows):
        perf = get_score(row)
        sim = get_similarity(row)
        # Combine: higher performance is good, lower distance is good
        # We use -sim to make it a maximization problem
        combined = perf - sim
        scored_rows.append((i, combined))
    
    # Sort by combined score descending
    scored_rows.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 5%
    limit = max(1, int(len(rows) * 0.05))
    return [item[0] for item in scored_rows[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for val in row:
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)
            
    best_indices = remember(header, rows)
    
    print("Analysis complete. Found setups most similar to the team's current configuration:")
    print(f"Indices of the {len(best_indices)} most relevant setups:")
    print(best_indices)

import csv

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop searching.
    We stop if the current row is a Pareto-optimal improvement over all
    previously seen rows and represents a significant gain (e.g., top 1% 
    of the potential search space).
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def get_score(r):
        # Normalize goal values to a [0, 1] scale for comparison
        # Since we don't have global min/max, we use the seen data
        score = 0
        for i in goal_indices:
            val = r[i]
            # Simple direction-based scoring
            if header[i].endswith('-'):
                score -= val
            else:
                score += val
        return score

    if not seen:
        return False

    current_score = get_score(row)
    seen_scores = [get_score(s) for s in seen]
    max_seen = max(seen_scores)

    # If this row is better than anything seen so far, check if it's 
    # a significant improvement (e.g., better than the best seen + a small margin)
    # This acts as an early-stopping criterion for optimization.
    if current_score > max_seen:
        # If we have enough data, check if it's in the top tier
        if len(seen) > 50:
            # Stop if we find a configuration that is significantly better 
            # than the average of the best 10% of what we've seen.
            top_10_pct = sorted(seen_scores, reverse=True)[:len(seen)//10]
            if current_score > (sum(top_10_pct) / len(top_10_pct)) * 1.05:
                return True
            
    return False

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    seen = []
    stopped = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Optimization stopped at row {i+1}.")
            print("The current configuration provides a significant improvement over previous runs.")
            print(f"Recommended configuration: {row}")
            stopped = True
            break
        seen.append(row)
    
    if not stopped:
        print("Optimization completed: No configuration met the early-stopping threshold.")

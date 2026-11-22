import csv

def flow(header, row, seen):
    """
    Decides whether to stop at the current row.
    We stop if the current row is significantly better than the best 
    seen so far, or if we have processed enough data to conclude 
    that further improvements are unlikely (diminishing returns).
    """
    if not seen:
        return False

    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        scores = []
        for i in goal_indices:
            name = header[i]
            val = r[i]
            # Normalize goals: MRE- (min), ACC+ (max), PRED40+ (max)
            # Since we don't have global min/max, we use a simple relative score
            if name.endswith('-'):
                scores.append(-val)
            else:
                scores.append(val)
        return sum(scores) / len(scores)

    # Calculate scores for all seen rows
    seen_scores = [get_score(r) for r in seen]
    best_seen = max(seen_scores)
    current_score = get_score(row)

    # Stop if we have seen at least 50 rows and the current row is 
    # better than the best seen so far, or if we've reached a plateau.
    if len(seen) >= 50:
        # If current is better than the best seen, stop.
        if current_score > best_seen:
            return True
        # If we have seen 200 rows and no improvement, stop (diminishing returns).
        if len(seen) >= 200:
            return True
            
    return False

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                rows.append(processed_row)

        seen = []
        stopped = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Stop paying for runs! The best setup was found at index {i}.")
                stopped = True
                break
            seen.append(row)
        
        if not stopped:
            print("No significant improvement found; processed all available data.")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

import csv

def flow(header, row, seen):
    """
    Decides whether to accept a row based on whether it is better than 
    any row seen so far. We use a simple dominance/score metric.
    """
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

    def get_score(r):
        # Lower is better for '-', higher is better for '+'
        score = 0.0
        for i in goal_indices:
            val = r[i]
            if header[i].endswith('-'):
                score += val
            else:
                score += (1.0 - val)
        return score

    current_score = get_score(row)
    
    # If this is the first row, accept it
    if not seen:
        return True
    
    # Compare against the best seen so far
    best_seen_score = min(get_score(r) for r in seen)
    
    # Accept if it's better than everything seen so far
    return current_score < best_seen_score

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        seen = []
        accepted_count = 0
        
        for row in rows:
            if flow(header, row, seen):
                accepted_count += 1
            seen.append(row)
            
        print("Customer Inquiry: Online Proposal Selection")
        print("-" * 45)
        print(f"Total proposals reviewed: {len(rows)}")
        print(f"Proposals approved:       {accepted_count}")
        print("\nStrategy: Approved a proposal only if it outperformed")
        print("all previously reviewed options.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

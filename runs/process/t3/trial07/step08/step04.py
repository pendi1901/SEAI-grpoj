import csv

def flow(header, row, seen):
    """
    Implements a Secretary Problem-style strategy.
    We observe a sample to establish a baseline of 'good' performance,
    then accept the first row that exceeds that baseline.
    """
    # Identify goal columns
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    
    def get_score(r):
        # Normalize goals: 1 - (val - min)/(max - min) for '-'
        # and (val - min)/(max - min) for '+'
        # Since we don't have global min/max, we use the current 'seen' data
        # to estimate relative quality.
        scores = []
        for i in goal_indices:
            col = [s[i] for s in seen + [r]]
            min_v, max_v = min(col), max(col)
            val = r[i]
            norm = (val - min_v) / (max_v - min_v + 1e-9)
            scores.append(1 - norm if header[i].endswith('-') else norm)
        return sum(scores) / len(scores)

    # Strategy: Observe 20% of the data to set a threshold, then pick the first
    # row that is better than the best seen so far.
    if len(seen) < 160:  # 20% of 800
        return False
    
    current_score = get_score(row)
    best_seen_score = max([get_score(s) for s in seen])
    
    return current_score > best_seen_score

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        seen = []
        accepted = []
        for row in rows:
            if flow(header, row, seen):
                accepted.append(row)
            seen.append(row)
            
        print(f"Processed {len(rows)} proposals.")
        print(f"Strategy accepted {len(accepted)} proposals.")
        if accepted:
            print("The first accepted proposal had the following goals:")
            for i, h in enumerate(header):
                if h.endswith(('-', '+')):
                    print(f"  {h}: {accepted[0][i]:.4f}")
        else:
            print("No proposals met the criteria.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
